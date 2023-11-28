"""
Top-level entrypoint for the command line interface.
"""
from __future__ import annotations

import typer

import module_qc_tools
from module_qc_tools.cli.ADC_CALIBRATION import main as adc_calibration
from module_qc_tools.cli.ANALOG_READBACK import main as analog_readback
from module_qc_tools.cli.DATA_TRANSMISSION import main as data_transmission
from module_qc_tools.cli.globals import CONTEXT_SETTINGS
from module_qc_tools.cli.hardware_emulator import (
    app as app_emulator,
)
from module_qc_tools.cli.INJECTION_CAPACITANCE import main as injection_capacitance
from module_qc_tools.cli.IV_MEASURE import main as iv_measure
from module_qc_tools.cli.LP_MODE import main as lp_mode
from module_qc_tools.cli.OVERVOLTAGE_PROTECTION import main as overvoltage_protection
from module_qc_tools.cli.SLDO import main as sldo
from module_qc_tools.cli.UNDERSHUNT_PROTECTION import main as undershunt_protection
from module_qc_tools.cli.upload_localdb import main as upload_localdb
from module_qc_tools.cli.VCAL_CALIBRATION import main as vcal_calibration

# subcommands
app = typer.Typer(context_settings=CONTEXT_SETTINGS)
app_measurement = typer.Typer(context_settings=CONTEXT_SETTINGS)

app.add_typer(app_emulator, name="emulator")
app.add_typer(app_measurement, name="measurement")


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Print the current version."),
    prefix: bool = typer.Option(
        False, "--prefix", help="Print the path prefix for data files."
    ),
) -> None:
    """
    Manage top-level options
    """
    if version:
        typer.echo(f"module-qc-tools v{module_qc_tools.__version__}")
        raise typer.Exit()
    if prefix:
        typer.echo(module_qc_tools.data.resolve())
        raise typer.Exit()


app_measurement.command("adc-calibration")(adc_calibration)
app_measurement.command("analog-readback")(analog_readback)
app_measurement.command("data-transmission")(data_transmission)
app_measurement.command("sldo")(sldo)
app_measurement.command("vcal-calibration")(vcal_calibration)
app_measurement.command("injection-capacitance")(injection_capacitance)
app_measurement.command("lp-mode")(lp_mode)
app_measurement.command("overvoltage-protection")(overvoltage_protection)
app_measurement.command("undershunt-protection")(undershunt_protection)
app_measurement.command("iv-measure")(iv_measure)

app.command("upload")(upload_localdb)

# for generating documentation using mkdocs-click
typer_click_object = typer.main.get_command(app)
