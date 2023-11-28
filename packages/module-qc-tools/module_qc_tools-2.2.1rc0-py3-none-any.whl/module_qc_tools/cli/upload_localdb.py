#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import requests
import typer

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_tools.utils.misc import bcolors

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("upload")
app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    measurement_path: Path = OPTIONS["measurement_path"],
    host: str = OPTIONS["host"],
    port: int = OPTIONS["port"],
    dry_run: bool = OPTIONS["dry_run"],
    output_path: Path = OPTIONS["output_path"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    """
    Walk through the specified directory (recursively) and attempt to submit all json files to LocalDB as the QC measurement

    Args:
        path (str or pathlib.Path): root directory to walk through
        host (str): localDB server host
        port (int): localDB server port
        out  (str): analysis output result json file path to save in the local host

    Returns:
        None: The files are uploaded to localDB.
    """

    log.setLevel(verbosity.value)
    log.info("Searching candidate RAW json files...")

    # Allow user to submit single file or directory
    if measurement_path.is_dir():
        flist = list(measurement_path.glob("*.json"))
    elif measurement_path.is_file():
        if measurement_path.suffix == ".json":
            flist = [measurement_path]
        else:
            log.error(
                bcolors.BADRED
                + f"The file you are trying to upload ({measurement_path}) is not a json file! Please upload the measurement json output file, or a path to the directory containing the measurement output json files."
                + bcolors.ENDC
            )
            return
    else:
        log.error(
            bcolors.BADRED
            + f"Input measurement path ({measurement_path}) is not recognized as a json file or path to directory containing json file - please check!"
            + bcolors.ENDC
        )
        return

    pack = []
    for path in flist:
        log.info(f"  - {path}")
        with path.open(encoding="utf-8") as fpointer:
            meas_data = json.load(fpointer)

            # Perform some basic checks on data before uploading

            if len(meas_data) == 0:
                log.warning(
                    bcolors.WARNING + f"{path} is empty - please check!" + bcolors.ENDC
                )
                continue

            if type(meas_data[0]) is not list:
                log.error(
                    bcolors.BADRED
                    + f"Measurements read from {path} are ill-formatted - please check that you are uploading measurement results and not analysis results!"
                    + bcolors.ENDC
                )
                continue
            pack.extend(meas_data)

    log.info(f"Extracted {len(pack)} tests from {len(flist)} input files.")
    log.info("==> Submitting RAW results pack...")

    protocol = "http" if port != 443 else "https"

    if not dry_run:
        try:
            response = requests.post(
                f"{protocol}://{host}:{port}/localdb/qc_uploader_post",
                json=pack,
            )
            response.raise_for_status()

            data = response.json()

            log.info(data)

        except Exception as err:
            log.error("failure in uploading!")
            log.error(err)
            raise typer.Exit(1) from err

        log.info(
            f"\nDone! LocalDB has accepted the following {len(data)} TestRun results"
        )
        for testRun in data:
            if testRun is None:
                log.info("A test run is already uploaded and will be skipped.")
                continue

            log.info(
                f'SerialNumber: {testRun["serialNumber"]}, Stage: {testRun["stage"]}, TestType: {testRun["testType"]}, QC-passed: {testRun["passed"]}'
            )

        try:
            with output_path.open("w") as f:
                json.dump(data, f, indent=4)
                log.info(f"Saved the output TestRun to {output_path}")

        except Exception:
            log.warning(
                bcolors.WARNING
                + f"Failed to saved the output TestRun to {output_path}"
                + bcolors.ENDC
            )
            altFilePath = f"/var/tmp/module-qc-tools-record-{int(time.time())}.json"

            try:
                with Path(altFilePath).open("w") as f:
                    json.dump(data, f, indent=4)
                log.info(f"Saved the output TestRun to {altFilePath}")

            except Exception:
                log.warning(
                    bcolors.WARNING
                    + f"Failed to saved the output TestRun to {altFilePath}"
                    + bcolors.ENDC
                )
                pass


if __name__ == "__main__":
    typer.run(main)
