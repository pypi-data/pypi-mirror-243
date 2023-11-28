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


def run(data, inj_cap_config, ps, yr, meter, layer):
    """The function which does the injection capacitance measurement.

    Args:
        data (list): data[chip_id].
        inj_cap_config (dict): An subdict dumped from json including the task information.
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        meter (Class meter): An instance of Class meter. Used to control the multimeter to measure voltages.

    Returns:
        None: The measurements are recorded in `data`.
    """
    if yr.running_emulator():
        ps.on(
            inj_cap_config["v_max"], inj_cap_config["i_config"][layer]
        )  # Only for emulator do the emulation of power on/off
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    # This sends global pulse
    status = yr.configure()
    assert status >= 0

    for _i in range(inj_cap_config["n_meas"]):
        v_mea = [{} for _ in range(yr._number_of_chips)]

        for chip in range(yr._number_of_chips):
            if chip in yr._disabled_chip_positions:
                continue

            # Disable both capmeasure and parasitic circuits
            yr.write_register("CapMeasEn", 0, chip)
            yr.write_register("CapMeasEnPar", 0, chip)

            for vmux_value in inj_cap_config["v_mux"]:
                yr.set_mux(
                    chip_position=chip,
                    v_mux=vmux_value,
                    reset_other_chips=inj_cap_config["share_vmux"],
                )
                mea, status = meter.measure_dcv(
                    channel=inj_cap_config["v_mux_channels"][chip]
                )
                v_mea[chip][f"Vmux{vmux_value}"] = [mea]

            for imux_value in inj_cap_config["i_mux"]:
                if imux_value == 10:
                    # Enable capmeasure circuit
                    yr.write_register("CapMeasEn", 1, chip)
                    yr.write_register("CapMeasEnPar", 0, chip)
                elif imux_value == 11:
                    # Enable capmeasure circuit
                    yr.write_register("CapMeasEn", 0, chip)
                    yr.write_register("CapMeasEnPar", 1, chip)
                else:
                    # Disable both
                    yr.write_register("CapMeasEn", 0, chip)
                    yr.write_register("CapMeasEnPar", 0, chip)

                yr.set_mux(
                    chip_position=chip,
                    i_mux=imux_value,
                    reset_other_chips=inj_cap_config["share_vmux"],
                )
                mea, status = meter.measure_dcv(
                    channel=inj_cap_config["v_mux_channels"][chip]
                )
                v_mea[chip][f"Imux{imux_value}"] = [mea]

            data[chip].add_data(v_mea[chip])

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

    log.info("[run_inj_capacitance] Start injection capacitance measurement!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_inj_capacitance] TimeStart: {timestart}")

    with resources.as_file(Path(config_path)) as path:
        config = json.loads(path.read_text())

    check_meas_config(config, config_path)

    if module_connectivity:
        config["yarr"]["connectivity"] = module_connectivity

    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    if "emulator" not in str(config_path) and not module_connectivity:
        typer.echo("must supply path to connectivity file [-m --module-connectivity]")
        raise typer.Exit(2)

    inj_cap_config = config["tasks"]["GENERAL"]
    inj_cap_config.update(config["tasks"]["INJECTION_CAPACITANCE"])

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

    ps.set(v=inj_cap_config["v_max"], i=inj_cap_config["i_config"][layer])

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
            columns=[f"Vmux{v_mux}" for v_mux in inj_cap_config["v_mux"]]
            + [f"Imux{i_mux}" for i_mux in inj_cap_config["i_mux"]],
            units=["V" for v_mux in inj_cap_config["v_mux"]]
            + ["V" for i_mux in inj_cap_config["i_mux"]],
        )
        for input_file in input_files
    ]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].add_property(
            test_type + "_MEASUREMENT_VERSION",
            pkg_resources.get_distribution("module-qc-tools").version,
        )
        data[chip]._meta_data = get_identifiers(yr.get_config(chip))
        data[chip].add_meta_data("Institution", institution)
        data[chip].add_meta_data("ModuleSN", module_serial)
        data[chip].add_meta_data("TimeStart", round(datetime.timestamp(datetime.now())))
        data[chip]._meta_data.update(get_meta_data(yr.get_config(chip)))

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        run(data, inj_cap_config, ps, yr, meter, layer)
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        yr.remove_tmp_connectivity()
    except Exception as err:
        logger.exception(err)
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err

    log.info(
        "==================================Summary=================================="
    )
    alloutput = []
    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        chip_name = data[chip]._meta_data["Name"]
        data[chip].add_meta_data("TimeEnd", round(datetime.timestamp(datetime.now())))
        log.info("data[chip]: ")
        log.info(data[chip])
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
    log.info("[run_inj_capacitance] Done!")
    log.info(
        f"[run_inj_capacitance] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()


if __name__ == "__main__":
    typer.run(main)
