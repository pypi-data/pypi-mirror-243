from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from module_qc_tools import data

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


OPTIONS = {}

OPTIONS["config"]: Path = typer.Option(
    str(data / "configs/example_merged_vmux.json"),
    "-c",
    "--config",
    help="Config file",
    exists=True,
    file_okay=True,
    readable=True,
    resolve_path=True,
)
OPTIONS["output_dir"]: Path = typer.Option(
    "outputs",
    "-o",
    "--output-dir",
    help="output directory",
    exists=False,
    writable=True,
)
OPTIONS["module_connectivity"]: Optional[Path] = typer.Option(
    None,
    "-m",
    "--module-connectivity",
    help="path to the module connectivity. Used also to identify the module SN, and to set the default output directory",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["verbosity"]: LogLevel = typer.Option(
    LogLevel.info,
    "-v",
    "--verbosity",
    help="Log level [options: DEBUG, INFO (default) WARNING, ERROR]",
)
OPTIONS["perchip"]: bool = typer.Option(
    False, help="Store results in one file per chip (default: one file per module)"
)
OPTIONS["use_pixel_config"]: bool = typer.Option(
    False,
    help="Use original chip configs; do not create temporary chip configs excluding Pixel Config",
)
OPTIONS["measurement_path"]: Path = typer.Option(
    "Measurement/",
    "-p",
    "--path",
    help="Path to directory with output measurement files",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)

OPTIONS["site"]: str = typer.Option(
    "",
    "--site",
    help='Your testing site. Required when submitting results to the database. Please use institute codes defined on production DB, i.e. "LBNL_PIXEL_MODULES" for LBNL, "IRFU" for Paris-Saclay, ...',
)

OPTIONS["host"]: str = typer.Option("localhost", "--host", help="localDB server")
OPTIONS["port"]: int = typer.Option(
    5000,
    "--port",
    help="localDB port",
)
OPTIONS["dry_run"]: bool = typer.Option(
    False,
    "-n",
    "--dry-run",
    help="Dry-run, do not submit to localDB or update controller config.",
)
OPTIONS["output_path"]: Path = typer.Option(
    "tmp.json",
    "--out",
    "--output-path",
    help="Analysis output result json file path to save in the local host",
    exists=False,
    writable=True,
)
OPTIONS["emulator_controller"]: Path = typer.Option(
    data / "emulator" / "configs/controller/specCfg-rd53b-16x1.json",
    "-r",
    "--controller",
    help="Controller",
    # exists=True,  # NB: enable when fixed for emulator (does not check for valid paths)
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["emulator_connectivity"]: Path = typer.Option(
    data / "emulator" / "configs/connectivity/20UPGXM1234567_Lx_dummy.json",
    "-c",
    "--connectivity",
    help="Connectivity",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["emulator_chip_position"]: int = typer.Option(
    0, "-i", "--chipPosition", help="chip position"
)
OPTIONS["depl_volt"]: float = typer.Option(
    None,
    "--vdepl",
    help="Depletion voltage from production database",
)
OPTIONS["skip_config"]: bool = typer.Option(
    False,
    "-s",
    "--skip-config",
    help="Skip configuring the chip when running eye diagram.",
)
OPTIONS["test_size"]: int = typer.Option(
    None,
    "-t",
    "--test-size",
    help="Test size for eye diagram.",
)
