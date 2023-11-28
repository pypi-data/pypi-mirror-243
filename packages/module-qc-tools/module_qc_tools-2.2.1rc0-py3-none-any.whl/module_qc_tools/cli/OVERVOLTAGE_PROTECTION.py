import copy
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


def run(data, OVP_config, NOMINAL_config, ps, yr, meter, nt, layer):
    # turn off power supply before switching low power mode on
    ps.off()
    # turn on low power mode
    yr.switchLPM("on")
    # turn on power supply and configure all chips
    if yr.running_emulator():
        ps.on(v=OVP_config["v_max"], i=OVP_config["i_config"][layer])
    else:
        ps.set(v=OVP_config["v_max"], i=OVP_config["i_config"][layer])
        ps.on()

    # Run an eye diagram
    log.info("[run_Undershunt] Running eye diagram at the start of scan")
    eye, status = yr.eyeDiagram(skipconfig=False)

    status = yr.configure()

    # Increase current to trigger OVP
    ps.set(v=OVP_config["v_max"], i=OVP_config["i_ovp"][layer])

    # measure current for power supply
    i = OVP_config["i_config"][layer]
    current, status = ps.measI()
    i_mea = [{} for _ in range(yr._number_of_chips)]
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        i_mea[chip]["SetCurrent"] = [i]
        i_mea[chip]["Current"] = [current]
        # measure temperature from NTC
        temp, status = nt.read()
        i_mea[chip]["Temperature"] = [temp]
        # measure v_mux
        for v_mux in OVP_config["v_mux"]:
            yr.set_mux(
                chip_position=chip,
                v_mux=v_mux,
                reset_other_chips=OVP_config["share_vmux"],
            )
            mea, status = meter.measure_dcv(channel=OVP_config["v_mux_channels"][chip])
            i_mea[chip][f"Vmux{v_mux}"] = [mea]
        # measure i_mux
        for i_mux in OVP_config["i_mux"]:
            yr.set_mux(
                chip_position=chip,
                i_mux=i_mux,
                reset_other_chips=OVP_config["share_vmux"],
            )
            mea, status = meter.measure_dcv(channel=OVP_config["v_mux_channels"][chip])
            i_mea[chip][f"Imux{i_mux}"] = [mea]
        data[chip].add_data(i_mea[chip])
        log.info(
            "--------------------------------------------------------------------------"
        )
        log.info(f"Chip-{chip+1}")
        log.info(tabulate(i_mea[chip], headers="keys", floatfmt=".3f"))

    # turn off power supply before switching low power mode off
    ps.off()
    # turn off low power mode
    yr.switchLPM("off")
    # Return to initial state
    if yr.running_emulator():
        ps.on(v=NOMINAL_config["v_max"], i=NOMINAL_config["i_config"][layer])
    else:
        ps.set(v=NOMINAL_config["v_max"], i=NOMINAL_config["i_config"][layer])
        ps.on()

    # Run an eye diagram
    log.info("[run_Undershunt] Running eye diagram at the end of scan")
    eye, status = yr.eyeDiagram(skipconfig=False)


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
    log.setLevel(verbosity.value)

    log.info("[run_OVP] Start OVP test!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_OVP] TimeStart: {timestart}")

    with resources.as_file(Path(config_path)) as path:
        config = json.loads(path.read_text())

    check_meas_config(config, config_path)

    # Need to pass module connectivity path to yarr class (except in case we are running the emulator)
    if module_connectivity:
        config["yarr"]["connectivity"] = module_connectivity

    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    if "emulator" not in str(config_path) and not module_connectivity:
        typer.echo("must supply path to connectivity file [-m --module-connectivity]")
        raise typer.Exit(2)

    if module_connectivity and "LP" not in str(module_connectivity):
        log.warning(
            bcolors.WARNING
            + f"You supplied a module connectivity ({module_connectivity}) which does not have 'LP' (low-power) in the name. Are you sure this is the connectivity file for low-power configuration? If not, chip will fail to configure."
            + bcolors.ENDC
        )

    NOMINAL_config = config["tasks"]["GENERAL"]
    OVP_config = copy.deepcopy(config["tasks"]["GENERAL"])
    OVP_config.update(config["tasks"]["OVERVOLTAGE_PROTECTION"])
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
            columns=["Temperature", "SetCurrent", "Current"]
            + [f"Vmux{v_mux}" for v_mux in OVP_config["v_mux"]]
            + [f"Imux{i_mux}" for i_mux in OVP_config["i_mux"]],
            units=["C", "A", "A"]
            + ["V" for v_mux in OVP_config["v_mux"]]
            + ["V" for i_mux in OVP_config["i_mux"]],
        )
        for input_file in input_files
    ]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].set_x("Current", True)
        data[chip]._meta_data = get_identifiers(yr.get_config(chip))
        data[chip].add_meta_data("Institution", institution)
        data[chip].add_meta_data("ModuleSN", module_serial)
        data[chip].add_meta_data("TimeStart", round(datetime.timestamp(datetime.now())))
        data[chip]._meta_data.update(get_meta_data(yr.get_config(chip)))
        data[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )

    try:
        run(data, OVP_config, NOMINAL_config, ps, yr, meter, nt, layer)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        log.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].add_meta_data("TimeEnd", round(datetime.timestamp(datetime.now())))
        data[chip].add_meta_data(
            "AverageTemperature", np.average(data[chip]["Temperature"])
        )

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
        chip_name = data[chip]._meta_data["Name"]
        outputDF = outputDataFrame()
        outputDF.set_test_type(test_type)
        outputDF.set_results(data[chip])
        if perchip:
            save_dict_list(
                output_dir.joinpath(f"{chip_name}.json"),
                [outputDF.to_dict()],
            )
        else:
            alloutput += [outputDF.to_dict()]
    if not perchip:
        save_dict_list(
            output_dir.joinpath(f"{module_serial}.json"),
            alloutput,
        )

    log.info(f"Writing output measurements in {output_dir}")
    log.info("[run_OVP] Done!")
    log.info(f"[run_OVP] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}")

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()


if __name__ == "__main__":
    typer.run(main)
