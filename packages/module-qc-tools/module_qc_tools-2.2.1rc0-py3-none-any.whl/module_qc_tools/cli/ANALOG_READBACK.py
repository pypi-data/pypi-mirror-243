import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

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
from tabulate import tabulate

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
from module_qc_tools.utils.ntc import ntc
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


def run_vmeas(data, analog_readback_config, ps, yr, meter, layer):
    """
    This function measures given internal voltages by going through all VMUX and IMUX settings provided in the config.

    Args:
        data (list): data[chip_id][vmux/imux_type].
        analog_readback_config (dict): An subdict dumped from json including the task information.
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        meter (Class meter): An instance of Class meter. Used to control the multimeter to measure voltages.

    Returns:
        None: The measurements are recorded in `data`.
    """
    log.info("[run_AnalogReadBack] Start V scan!")
    log.info(
        f"[run_AnalogReadBack] TimeStart: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )

    if yr.running_emulator():
        ps.on(
            analog_readback_config["v_max"],
            analog_readback_config["i_config"][layer],
        )  # Only for emulator do the emulation of power on/off.
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    # Reset other chips
    reset = analog_readback_config["share_vmux"]

    # Set and measure current for power supply
    i_mea = [{} for _ in range(yr._number_of_chips)]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue

        # measure v_mux
        for v_mux in analog_readback_config["v_mux"]:
            yr.set_mux(chip_position=chip, v_mux=v_mux, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip][f"Vmux{v_mux}"] = [mea]

        # Measure i_mux
        for i_mux in analog_readback_config["i_mux"]:
            yr.set_mux(chip_position=chip, i_mux=i_mux, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip][f"Imux{i_mux}"] = [mea]

        data[chip].add_data(i_mea[chip])

        log.info(
            "--------------------------------------------------------------------------"
        )
        log.info(f"Chip-{chip+1}")
        log.info(tabulate(i_mea[chip], headers="keys", floatfmt=".3f"))

    log.info("[run_AnalogReadBack] V scan done!")
    log.info(
        f"[run_AnalogReadBack] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )


def run_tmeas(data, analog_readback_config, ps, yr, meter, nt, layer):
    """
    This function measures temperature of the NTC nad MOS sensor though VMUX and IMUX settings provided in the config.

    Args:
        data (list): data[chip_id][vmux/imux_type or bias/dem].
        analog_readback_config (dict): An subdict dumped from json including the task information.
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        meter (Class meter): An instance of Class meter. Used to control the multimeter to measure voltages.

    Returns:
        None: The measurements are recorded in `data`.
    """
    log.info("[run_AnalogReadBack] Start T measurement!")
    log.info(
        f"[run_AnalogReadBack] TimeStart: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )

    if yr.running_emulator():
        ps.on(
            analog_readback_config["v_max"],
            analog_readback_config["i_config"][layer],
        )  # Only for emulator do the emulation of power on/off.
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    # Reset other chips
    reset = analog_readback_config["share_vmux"]

    # Chip config mapping
    bias_maps = {
        14: "MonSensSldoAnaSelBias",
        16: "MonSensSldoDigSelBias",
        18: "MonSensAcbSelBias",
    }
    dem_maps = {
        14: "MonSensSldoAnaDem",
        16: "MonSensSldoDigDem",
        18: "MonSensAcbDem",
    }

    # Measure external external NTC
    mea_ntc, status = nt.read()

    i_mea = [{} for _ in range(yr._number_of_chips)]
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue

        # Measure v_mux_tempmeas
        for v_mux in analog_readback_config["v_mux_tempsens"]:
            yr.set_mux(chip_position=chip, v_mux=v_mux, reset_other_chips=reset)
            yr.enable_tempsens(chip_position=chip, v_mux=v_mux, reset_other_chips=reset)
            for bias in analog_readback_config[bias_maps[v_mux]]:
                yr.set_tempsens_bias(
                    chip_position=chip, v_mux=v_mux, bias=bias, reset_other_chips=reset
                )
                for dem in analog_readback_config[dem_maps[v_mux]]:
                    yr.set_tempsens_dem(
                        chip_position=chip,
                        v_mux=v_mux,
                        dem=dem,
                        reset_other_chips=reset,
                    )
                    mea, status = meter.measure_dcv(
                        channel=analog_readback_config["v_mux_channels"][chip]
                    )
                    # Reset i_mea[chip]
                    i_mea[chip] = {}
                    # Record vmux, bias, and dem.
                    i_mea[chip][f"Vmux{v_mux}"] = [mea]
                    i_mea[chip][bias_maps[v_mux]] = [bias]
                    i_mea[chip][dem_maps[v_mux]] = [dem]

                    data[chip].add_data(i_mea[chip])
        yr.reset_tempsens(chip)

        # Mwasure v_mux_ntc 32 times.
        max_n_measure = len(data[chip]["Vmux14"])
        n_measure = 0
        while n_measure < max_n_measure:
            i_mea[chip] = {}
            yr.set_mux(chip_position=chip, v_mux=2, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip]["Vmux2"] = [mea]
            yr.set_mux(chip_position=chip, v_mux=30, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip]["Vmux30"] = [mea]
            yr.set_mux(chip_position=chip, i_mux=9, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip]["Imux9"] = [mea]
            yr.set_mux(chip_position=chip, i_mux=63, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip]["Imux63"] = [mea]
            i_mea[chip]["TExtExtNTC"] = [mea_ntc]
            data[chip].add_data(i_mea[chip])
            n_measure += 1

        log.info(
            "--------------------------------------------------------------------------"
        )
        log.info(f"Chip-{chip+1}")
        log.info(tabulate(i_mea[chip], headers="keys", floatfmt=".3f"))

    log.info("[run_AnalogReadBack] T measurement done!")
    log.info(
        f"[run_AnalogReadBack] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )


def run_vdda_vddd_vs_trim(data, analog_readback_config, ps, yr, meter, layer):
    """
    This function measures how VDDA and VDDD changes with Trim.

    Args:
        data (list): data[chip_id][vmux/imux_type or bias/dem].
        analog_readback_config (dict): An subdict dumped from json including the task information.
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        meter (Class meter): An instance of Class meter. Used to control the multimeter to measure voltages.

    Returns:
        None: The measurements are recorded in `data`.
    """
    log.info("[run_AnalogReadBack] Start VDD vs Trim measurement!")
    log.info(
        f"[run_AnalogReadBack] TimeStart: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )

    if yr.running_emulator():
        ps.on(
            analog_readback_config["v_max"],
            analog_readback_config["i_config"][layer],
        )  # Only for emulator do the emulation of power on/off.
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    # Reset other chips
    reset = analog_readback_config["share_vmux"]

    # Trim to Vmux mapping
    vmux_to_trim = {
        34: "SldoTrimA",
        38: "SldoTrimD",
    }

    i_mea = [{} for _ in range(yr._number_of_chips)]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue

        # Measure VDDA/VDDD vs SldoTrimA/SldoTrimD
        for v_mux in vmux_to_trim:
            yr.set_mux(chip_position=chip, v_mux=v_mux, reset_other_chips=reset)

            # Read initial Trim in chip config
            config_trim, status = yr.read_register(
                name=vmux_to_trim[v_mux], chip_position=chip
            )

            for trim in analog_readback_config[vmux_to_trim[v_mux]]:
                # Set Trim
                yr.write_register(
                    name=vmux_to_trim[v_mux], value=trim, chip_position=chip
                )

                # Run eye-diagram and update the delay in the controller config according to new trim values
                log.info(
                    f"[run_AnalogReadBack] Running eye diagram for VMUX{v_mux}={trim}"
                )
                eye, status = yr.eyeDiagram(skipconfig=True, testsize=100000)

                mea, status = meter.measure_dcv(
                    channel=analog_readback_config["v_mux_channels"][chip]
                )
                # Reset i_mea[chip]
                i_mea[chip] = {}

                # Record vmux and trim.
                i_mea[chip][f"Vmux{v_mux}"] = [mea]
                i_mea[chip][vmux_to_trim[v_mux]] = [trim]

                # Read ROSC vs trim
                if v_mux == 38:
                    mea, status = yr.read_ringosc(chip_position=chip)
                    rosc_mea = [float(num) for num in mea.split()]
                    for i in range(len(rosc_mea)):
                        i_mea[chip][f"ROSC{i}"] = [rosc_mea[i]]

                # Update output dataframe
                data[chip].add_data(i_mea[chip])

            # Reset Trim to value in config and restore delay settings via eye diagram
            log.info(
                f"[run_AnalogReadBack] Set VMUX{v_mux} back to default and re-running \U0001F441  diagram."
            )
            yr.write_register(
                name=vmux_to_trim[v_mux], value=config_trim, chip_position=chip
            )
            eye, status = yr.eyeDiagram(skipconfig=True)

        # Mwasure ground 16 times.
        max_n_measure = len(data[chip]["Vmux34"])
        n_measure = 0
        while n_measure < max_n_measure:
            i_mea[chip] = {}
            yr.set_mux(chip_position=chip, v_mux=30, reset_other_chips=reset)
            mea, status = meter.measure_dcv(
                channel=analog_readback_config["v_mux_channels"][chip]
            )
            i_mea[chip]["Vmux30"] = [mea]
            data[chip].add_data(i_mea[chip])
            n_measure += 1

        log.info(
            "--------------------------------------------------------------------------"
        )
        log.info(f"Chip-{chip+1}")
        log.info(tabulate(i_mea[chip], headers="keys", floatfmt=".3f"))

    log.info("[run_AnalogReadBack] VDDA/VDDD measurement done!")
    log.info(
        f"[run_AnalogReadBack] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )


def add_identifier_metadata(data, yr, module_serial, institution):
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip]._meta_data = get_identifiers(yr.get_config(chip))
        data[chip].add_meta_data("Institution", institution)
        data[chip].add_meta_data("ModuleSN", module_serial)
        data[chip].add_meta_data("TimeStart", round(datetime.timestamp(datetime.now())))
        data[chip]._meta_data.update(get_meta_data(yr.get_config(chip)))


def add_time_end_identifier(yr, data):
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].add_meta_data("TimeEnd", round(datetime.timestamp(datetime.now())))


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
    """
    main() creates the qcDataFrame and pass it to the run() where the measurements are stored in the qcDataFrame.
    """

    log.setLevel(verbosity.value)

    log.info("[run_AnalogReadBack] Starting analog readback!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_AnalogReadBack] TimeStart: {timestart}")

    with resources.as_file(Path(config_path)) as path:
        config = json.loads(path.read_text())

    check_meas_config(config, config_path)

    if module_connectivity:
        config["yarr"]["connectivity"] = module_connectivity

    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    if "emulator" not in str(config_path) and not module_connectivity:
        typer.echo("must supply path to connectivity file [-m --module-connectivity]")
        raise typer.Exit(2)

    analog_readback_config = config["tasks"]["GENERAL"]
    analog_readback_config.update(config["tasks"]["ANALOG_READBACK"])

    ps = power_supply(config["power_supply"])
    yr = yarr(config["yarr"])
    meter = multimeter(config["multimeter"])
    nt = ntc(config["ntc"])

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

    ps.set(
        v=analog_readback_config["v_max"], i=analog_readback_config["i_config"][layer]
    )
    yr.configure()

    # if -o option used, overwrite the default output directory
    output_dir = module_connectivity.parent if module_connectivity else base_output_dir

    if base_output_dir != Path("outputs"):
        output_dir = base_output_dir

    output_dir = output_dir.joinpath("Measurements", test_type, timestart)
    # Make output directory and start log file
    output_dir.mkdir(parents=True, exist_ok=True)
    log.addHandler(logging.FileHandler(output_dir.joinpath("output.log")))

    input_files = [None] * yr._number_of_chips

    data = [
        qcDataFrame(
            columns=[f"Vmux{v_mux}" for v_mux in analog_readback_config["v_mux"]]
            + [f"Imux{i_mux}" for i_mux in analog_readback_config["i_mux"]],
            units=["V" for v_mux in analog_readback_config["v_mux"]]
            + ["V" for i_mux in analog_readback_config["i_mux"]],
        )
        for input_file in input_files
    ]

    data_tempmeas = [
        qcDataFrame(
            columns=[f"Vmux{v_mux}" for v_mux in analog_readback_config["v_mux_ntc"]]
            + [f"Imux{i_mux}" for i_mux in analog_readback_config["i_mux_ntc"]]
            + [f"Vmux{v_mux}" for v_mux in analog_readback_config["v_mux_tempsens"]]
            + ["MonSensSldoAnaSelBias"]
            + ["MonSensSldoDigSelBias"]
            + ["MonSensAcbSelBias"]
            + ["MonSensSldoAnaDem"]
            + ["MonSensSldoDigDem"]
            + ["MonSensAcbDem"]
            + ["TExtExtNTC"],
            units=["V" for v_mux in analog_readback_config["v_mux_ntc"]]
            + ["V" for i_mux in analog_readback_config["i_mux_ntc"]]
            + ["V" for v_mux in analog_readback_config["v_mux_tempsens"]]
            + ["-"]
            + ["-"]
            + ["-"]
            + ["-"]
            + ["-"]
            + ["-"]
            + ["C"],
        )
        for input_file in input_files
    ]

    data_vdda_vddd_vs_trim = [
        qcDataFrame(
            columns=["Vmux34"]
            + ["Vmux38"]
            + ["Vmux30"]
            + ["SldoTrimA"]
            + ["SldoTrimD"]
            + [f"ROSC{i}" for i in range(42)],
            units=["V"] + ["V"] + ["V"] + ["-"] + ["-"] + ["MHz" for i in range(42)],
        )
        for input_file in input_files
    ]

    # Measure internal vmux
    add_identifier_metadata(data, yr, module_serial, institution)
    try:
        run_vmeas(data, analog_readback_config, ps, yr, meter, layer)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        log.info("Error in measuring all vmux values.")
        log.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err
    add_time_end_identifier(yr, data)

    # Measure temperature
    add_identifier_metadata(data_tempmeas, yr, module_serial, institution)
    try:
        run_tmeas(data_tempmeas, analog_readback_config, ps, yr, meter, nt, layer)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        log.info("Error in measuring temperature.")
        log.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err
    add_time_end_identifier(yr, data_tempmeas)

    # Measure vdda/vddd vs trim
    add_identifier_metadata(data_vdda_vddd_vs_trim, yr, module_serial, institution)
    try:
        run_vdda_vddd_vs_trim(
            data_vdda_vddd_vs_trim, analog_readback_config, ps, yr, meter, layer
        )
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        log.info("Error in measuring VDDA/VDDD vs trim.")
        log.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err
    add_time_end_identifier(yr, data_vdda_vddd_vs_trim)

    # save results in json
    log.info(
        "==================================Summary=================================="
    )
    alloutput = []
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        log.info(f"Chip-{chip+1}")
        log.info(data[chip])
        log.info(data_tempmeas[chip])
        chip_name = data[chip]._meta_data["Name"]
        data[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )
        data_tempmeas[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )
        data_vdda_vddd_vs_trim[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )
        # Add TimeEnd identifier
        data[chip].add_meta_data("TimeEnd", round(datetime.timestamp(datetime.now())))
        data_tempmeas[chip].add_meta_data(
            "TimeEnd", round(datetime.timestamp(datetime.now()))
        )
        data_vdda_vddd_vs_trim[chip].add_meta_data(
            "TimeEnd", round(datetime.timestamp(datetime.now()))
        )
        # Save to an output json file
        outputDF = outputDataFrame()
        outputDF.set_test_type(test_type)
        outputDF.set_subtest_type("AR_VMEAS")
        outputDF.set_results(data[chip])

        outputDF_tempmeas = outputDataFrame()
        outputDF_tempmeas.set_test_type(test_type)
        outputDF_tempmeas.set_subtest_type("AR_TEMP")
        outputDF_tempmeas.set_results(data_tempmeas[chip])

        outputDF_vdda_vddd_vs_trim = outputDataFrame()
        outputDF_vdda_vddd_vs_trim.set_test_type(test_type)
        outputDF_vdda_vddd_vs_trim.set_subtest_type("AR_VDD")
        outputDF_vdda_vddd_vs_trim.set_results(data_vdda_vddd_vs_trim[chip])
        if perchip:
            save_dict_list(
                output_dir.joinpath(f"{chip_name}.json"),
                [
                    outputDF.to_dict(),
                    outputDF_tempmeas.to_dict(),
                    outputDF_vdda_vddd_vs_trim.to_dict(),
                ],
            )
        else:
            alloutput += [
                outputDF.to_dict(),
                outputDF_tempmeas.to_dict(),
                outputDF_vdda_vddd_vs_trim.to_dict(),
            ]

    if not perchip:
        save_dict_list(
            output_dir.joinpath(f"{module_serial}.json"),
            alloutput,
        )

    log.info(f"Writing output measurements in {output_dir}")

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()


if __name__ == "__main__":
    typer.run(main)
