import json
import logging
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import pkg_resources
import typer
from module_qc_data_tools import (
    get_env,
    get_nlanes_from_sn,
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
from module_qc_tools.utils.ntc import ntc
from module_qc_tools.utils.yarr import yarr

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


def run(data, metadata, DT_config, yr, nt, log_file, dryrun, n_lanes_per_chip):
    status = yr.configure()
    meas = [{} for _ in range(yr._number_of_chips)]

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        for value in DT_config["MonitorV"]:
            yr.set_mux(
                chip_position=chip,
                v_mux=value,
                reset_other_chips=False,
            )

        # measure temperature from NTC
        temp, status = nt.read()
        metadata[chip]["Temperature"] = [temp]

    log.info("Running eye-diagram scan... ")
    log.info("\n" + yr.eyeDiagram(dryrun=dryrun)[0])

    with Path(log_file).open() as f:
        yarr_output = f.readlines()

    eye_output = ""
    delay_setting = {}
    eye_width = {}

    for line in yarr_output:
        if line.count("|") >= 16:
            eye_output += (
                line.replace("\033[32m", "")
                .replace("\033[0m", "")
                .replace("| \n", "\n")
            )
        if "[  info  ][  eyeDiagram   ]" in line and "lane" in line:
            lane = line.split("lane ")[1].split(" ")[0].replace("\n", "")
            if "Delay setting" in line:
                values = line.split("eye width ")[1].replace("\n", "")
                eye_width[lane] = int(float(values.split(": ")[0]))
                delay_setting[lane] = int(float(values.split(": ")[1]))
            else:
                eye_width[lane] = 0
                delay_setting[lane] = 0

    colnames = ["Delay"] + [f"lane{i}" for i in range(16)]
    testdata = pd.read_csv(
        StringIO(eye_output), sep="|", names=colnames, header=None, index_col=False
    )

    # TODO: maybe use this info ? [16:24:49:371][  info  ][    SpecRx     ][31126]: Active Rx channels: 0x8

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        meas[chip]["Delay"] = testdata["Delay"]
        metadata[chip]["Rx"] = [yr._chip_rx[chip]]
        for i in range(n_lanes_per_chip):
            if n_lanes_per_chip > 1:
                meas[chip][f"EyeOpening{i}"] = testdata[
                    f"lane{yr._chip_rx[chip]*chip+i}"
                ]
                metadata[chip][f"EyeWidth{i}"] = eye_width[
                    str(yr._chip_rx[chip] * chip + i)
                ]
                metadata[chip][f"DelaySetting{i}"] = delay_setting[
                    str(yr._chip_rx[chip] * chip + i)
                ]
            else:
                meas[chip][f"EyeOpening{i}"] = testdata[f"lane{yr._chip_rx[chip]}"]
                try:
                    metadata[chip][f"EyeWidth{i}"] = [eye_width[str(yr._chip_rx[chip])]]
                    metadata[chip][f"DelaySetting{i}"] = [
                        delay_setting[str(yr._chip_rx[chip])]
                    ]
                except Exception:
                    log.warning(
                        bcolors.WARNING
                        + f"No good delay setting found for lane {yr._chip_rx[chip]} \U0001F937"
                        + bcolors.ENDC
                    )

        data[chip].add_data(meas[chip])


@app.command()
def main(
    config_path: Path = OPTIONS["config"],
    base_output_dir: Path = OPTIONS["output_dir"],
    module_connectivity: Optional[Path] = OPTIONS["module_connectivity"],
    verbosity: LogLevel = OPTIONS["verbosity"],
    perchip: bool = OPTIONS["perchip"],
    use_pixel_config: bool = OPTIONS["use_pixel_config"],
    site: str = OPTIONS["site"],
    dryrun: bool = OPTIONS["dry_run"],
):
    log.setLevel(verbosity.value)

    log.info("[run_DATA_TRANSMISSION] Start DATA TRANSMISSION scan!")
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log.info(f"[run_DATA_TRANSMISSION] TimeStart: {timestart}")

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

    DT_config = config["tasks"]["GENERAL"]
    DT_config.update(config["tasks"]["DATA_TRANSMISSION"])
    yr = yarr(config["yarr"])

    nt = ntc(config["ntc"])

    if not use_pixel_config:
        yr.omit_pixel_config("tmp")

    # Define identifires for the output files.
    # Taking the module SN from YARR path to config in the connectivity file.
    # Taking the test-type from the script name which is the test-code in ProdDB.
    module_serial = get_sn_from_connectivity(config["yarr"]["connectivity"])
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

    # # if -o option used, overwrite the default output directory
    output_dir = module_connectivity.parent if module_connectivity else base_output_dir

    if base_output_dir != Path("outputs"):
        output_dir = base_output_dir

    output_dir = output_dir.joinpath("Measurements", test_type, timestart)
    # Make output directory and start log file
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = output_dir.joinpath("output.log")
    log.addHandler(logging.FileHandler(log_file))
    input_files = [None] * yr._number_of_chips
    data = []
    n_lanes_per_chip = get_nlanes_from_sn(module_serial)

    data = []
    metadata = []

    for _input_file in input_files:
        data += [
            qcDataFrame(
                columns=["Delay"] + [f"EyeOpening{i}" for i in range(n_lanes_per_chip)],
                units=[""] + n_lanes_per_chip * [""],
            )
        ]

        metadata += [{"Temperature": [], "Rx": []}]
        for i in range(n_lanes_per_chip):
            metadata[-1][f"EyeWidth{i}"] = []
            metadata[-1][f"DelaySetting{i}"] = []

    for chip in range(yr._number_of_chips):
        if chip in yr._disabled_chip_positions:
            continue
        data[chip].set_x("Delay", True)
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
        run(
            data,
            metadata,
            DT_config,
            yr,
            nt,
            log_file,
            dryrun,
            n_lanes_per_chip,
        )
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
            "AverageTemperature", np.average(metadata[chip].pop("Temperature"))
        )
        for key, value in metadata[chip].items():
            data[chip].add_meta_data(key, value)

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

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()

    log.info("[run_DATA_TRANSMISSION] Done!")
    log.info(
        f"[run_DATA_TRANSMISSION] TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    )


if __name__ == "__main__":
    typer.run(main)
