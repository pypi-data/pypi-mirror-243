import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pkg_resources
import typer
from module_qc_data_tools import (
    get_env,
    get_layer_from_sn,
    get_sn_from_connectivity,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_tools.utils.misc import (
    bcolors,
    check_meas_config,
    get_identifiers,
    get_meta_data,
)
from module_qc_tools.utils.multimeter import multimeter
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


def run(data, vcal_calib_config, ps, yr, meter, layer):
    """The function which does the VCal calibration for VCal_Med and VCal_Hi in both large and small range.

    Args:
        data (list): data[chip_id][vcal_type]. 4 vcal_type in total.
        vcal_calib_config (dict): An subdict dumped from json including the task information.
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        meter (Class meter): An instance of Class meter. Used to control the multimeter to measure voltages.

    Returns:
        None: The measurements are recorded in `data`.
    """
    if yr.running_emulator():
        ps.on(
            vcal_calib_config["v_max"], vcal_calib_config["i_config"][layer]
        )  # Only for emulator do the emulation of power on/off
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    status = (
        yr.configure()
    )  # Should always be 0. Essentially it calls send_command() in the hardware_control_base where protection is added.
    assert status >= 0

    InjVcalRange = vcal_calib_config["InjVcalRange"]
    MonitorV = vcal_calib_config["MonitorV"]

    Large_Range = [
        vcal_calib_config["Large_Range"]["start"],
        vcal_calib_config["Large_Range"]["stop"],
        vcal_calib_config["Large_Range"]["step"],
    ]
    Small_Range = [
        vcal_calib_config["Small_Range"]["start"],
        vcal_calib_config["Small_Range"]["stop"],
        vcal_calib_config["Small_Range"]["step"],
    ]
    vmux_value_GNDA = vcal_calib_config["MonitorV_GND"]
    Ranges = [Large_Range, Small_Range]

    Ranges_maps = {"1": "LargeRange", "0": "SmallRange"}
    RegisterNames_maps = {"8": "InjVcalMed", "7": "InjVcalHigh"}

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        cal_count = 0
        for i, vmux_value in enumerate(MonitorV):
            for j, vcalrange in enumerate(InjVcalRange):
                log.info(
                    f"[run_VCal_calib]     Start {RegisterNames_maps[str(vmux_value)]}, {Ranges_maps[str(vcalrange)]} for chip {data[chip][cal_count]._meta_data['Name']}"
                )
                data[chip][cal_count].add_meta_data(
                    "TimeStart", round(datetime.timestamp(datetime.now()))
                )

                DACs = np.arange(
                    start=Ranges[j][0], stop=Ranges[j][1], step=Ranges[j][2]
                )
                meased_voltages = -9999.0 * np.ones(len(DACs))
                x_label = "DACs_input"
                y_label = "Vmux" + str(MonitorV[i])

                yr.set_mux(
                    chip_position=chip,
                    v_mux=vmux_value_GNDA,
                    reset_other_chips=vcal_calib_config["share_vmux"],
                )
                meased_voltage_gnd, status = meter.measure_dcv(
                    channel=vcal_calib_config["v_mux_channels"][chip]
                )  # Measure the GND with VMUX selection from config MonitorV_GND
                meased_voltages_gnd = np.repeat(
                    meased_voltage_gnd, repeats=len(DACs)
                )  # the GND doesn't change a lot, repeat it

                yr.write_register("InjVcalRange", vcalrange, chip)

                yr.set_mux(
                    chip_position=chip,
                    v_mux=MonitorV[i],
                    reset_other_chips=vcal_calib_config["share_vmux"],
                )
                for k, DAC in enumerate(DACs):
                    yr.write_register(
                        RegisterNames_maps[str(vmux_value)], DAC, chip
                    )  # write DAC values
                    mea, status = meter.measure_dcv(
                        channel=vcal_calib_config["v_mux_channels"][chip]
                    )
                    meased_voltages[k] = mea  # measure the voltage at a given DAC value

                data[chip][cal_count].add_data(
                    dict(
                        {
                            x_label: DACs.tolist(),
                            y_label: meased_voltages,
                            f"Vmux{vmux_value_GNDA}": meased_voltages_gnd.tolist(),
                        }
                    )
                )
                data[chip][cal_count].add_meta_data(
                    "TimeEnd", round(datetime.timestamp(datetime.now()))
                )
                cal_count += 1

    if yr.running_emulator():
        ps.off()


@app.command()
def main(
    config_path: Path = OPTIONS["config"],
    base_output_dir: Path = OPTIONS["output_dir"],
    module_connectivity: Optional[Path] = OPTIONS["module_connectivity"],
    verbosity: LogLevel = OPTIONS["verbosity"],
    perchip: bool = OPTIONS["perchip"],
    use_pixel_config: bool = OPTIONS["use_pixel_config"],
    site: str = OPTIONS["site"],
):
    """main() creates the qcDataFrame and pass it to the run() where the measurements are stored in the qcDataFrame."""

    log.setLevel(verbosity.value)

    log.info("[run_VCal_calib] Start VCal calibration!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_VCal_calib] TimeStart: {timestart}")

    with resources.as_file(Path(config_path)) as path:
        config = json.loads(path.read_text())

    check_meas_config(config, config_path)

    if module_connectivity:
        config["yarr"]["connectivity"] = module_connectivity

    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    if "emulator" not in str(config_path) and not module_connectivity:
        typer.echo("must supply path to connectivity file [-m --module-connectivity]")
        raise typer.Exit(2)

    vcal_calib_config = config["tasks"]["GENERAL"]
    vcal_calib_config.update(config["tasks"]["VCAL_CALIBRATION"])

    ps = power_supply(config["power_supply"])
    yr = yarr(config["yarr"])
    meter = multimeter(config["multimeter"])

    if not use_pixel_config:
        yr.omit_pixel_config("tmp")

    # Define identifires for the output files.
    # Taking the module SN from YARR path to config in the connectivity file.
    # Taking the test-type from the script name which is the test-code in ProdDB.
    module_serial = get_sn_from_connectivity(config["yarr"]["connectivity"])
    layer = get_layer_from_sn(module_serial)
    test_type = Path(__file__).stem
    institution = get_env("INSTITUTION")
    if site and institution is not None:
        log.warning(
            bcolors.WARNING
            + " Overwriting default institution {} with manual input {}!".format(
                institution, site
            )
            + bcolors.ENDC
        )
        institution = site
    elif site:
        institution = site

    if not institution:
        log.error(
            bcolors.ERROR
            + 'No institution found. Please specify your testing site as an environmental variable "INSTITUTION" or specify with the --site option. '
            + bcolors.ENDC
        )
        return

    ps.set(v=vcal_calib_config["v_max"], i=vcal_calib_config["i_config"][layer])

    MonitorV = vcal_calib_config["MonitorV"]
    InjVcalRange = vcal_calib_config["InjVcalRange"]
    vmux_value_GNDA = vcal_calib_config["MonitorV_GND"]

    # if -o option used, overwrite the default output directory
    output_dir = module_connectivity.parent if module_connectivity else base_output_dir

    if base_output_dir != Path("outputs"):
        output_dir = base_output_dir

    output_dir = output_dir.joinpath("Measurements", test_type, timestart)
    # Make output directory and start log file
    output_dir.mkdir(parents=True, exist_ok=True)
    log.addHandler(logging.FileHandler(output_dir.joinpath("output.log")))

    chip_data = []
    for chip in range(yr._number_of_chips):
        # if chip in yr._disabled_chip_positions:
        # continue
        qcdata_list = []
        for i, _vmux_value in enumerate(MonitorV):
            for _j, vcalrange in enumerate(InjVcalRange):
                x_label = "DACs_input"
                y_label = "Vmux" + str(MonitorV[i])
                data = qcDataFrame(
                    columns=[x_label, y_label, f"Vmux{vmux_value_GNDA}"],
                    units=["Count", "V", "V"],
                )
                data.add_property(
                    test_type + "_MEASUREMENT_VERSION",
                    pkg_resources.get_distribution("module-qc-tools").version,
                )

                data.set_x(x_label, True)
                data._meta_data = get_identifiers(yr.get_config(chip))
                data.add_meta_data("Institution", institution)
                data.add_meta_data("ModuleSN", module_serial)
                data._meta_data.update(get_meta_data(yr.get_config(chip)))

                data._meta_data["ChipConfigs"]["RD53B"]["GlobalConfig"][
                    "MonitorEnable"
                ] = 1
                data._meta_data["ChipConfigs"]["RD53B"]["GlobalConfig"][
                    "MonitorV"
                ] = MonitorV[i]
                data._meta_data["ChipConfigs"]["RD53B"]["GlobalConfig"][
                    "InjVcalRange"
                ] = vcalrange

                qcdata_list.append(data)
        chip_data.append(qcdata_list)

    try:
        run(chip_data, vcal_calib_config, ps, yr, meter, layer)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        log.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err

    log.info(
        "==================================Summary=================================="
    )
    alloutput = []
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        log.info(f"Chip-{chip+1}")
        alltests = []
        for i in range(len(chip_data[chip])):
            log.info(chip_data[chip][i])
            chip_name = chip_data[chip][i]._meta_data["Name"]
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)

            # Determine subtest type
            monitorV = chip_data[chip][i]._meta_data["ChipConfigs"]["RD53B"][
                "GlobalConfig"
            ]["MonitorV"]
            injVcalRange = chip_data[chip][i]._meta_data["ChipConfigs"]["RD53B"][
                "GlobalConfig"
            ]["InjVcalRange"]
            sub_test_type = "Unknown"
            if monitorV == 7 and injVcalRange == 1:
                sub_test_type = "VCAL_HIGH"
            elif monitorV == 7 and injVcalRange == 0:
                sub_test_type = "VCAL_HIGH_SMALL_RANGE"
            elif monitorV == 8 and injVcalRange == 1:
                sub_test_type = "VCAL_MED"
            elif monitorV == 8 and injVcalRange == 0:
                sub_test_type = "VCAL_MED_SMALL_RANGE"
            outputDF.set_subtest_type(sub_test_type)

            outputDF.set_results(chip_data[chip][i])
            alltests += [outputDF.to_dict()]
        if not perchip:
            alloutput += alltests
        else:
            save_dict_list(
                output_dir.joinpath(f"{chip_name}.json"),
                alltests,
            )
    if not perchip:
        save_dict_list(
            output_dir.joinpath(f"{module_serial}.json"),
            alloutput,
        )

    log.info(f"Writing output measurements in {output_dir}")
    log.info("[run_VCal_calib] Done!")
    log.info(f"[run_VCal_calib] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}")

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()


if __name__ == "__main__":
    typer.run(main)
