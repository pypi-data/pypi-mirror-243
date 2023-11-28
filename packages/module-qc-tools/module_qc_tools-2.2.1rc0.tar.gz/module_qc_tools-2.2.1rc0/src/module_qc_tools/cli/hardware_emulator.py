import json
import logging
import shutil
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np
import typer

from module_qc_tools import data
from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

rng = np.random.default_rng(42)
log = logging.getLogger("emulator")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


class PSAction(str, Enum):
    on = "on"
    off = "off"
    getV = "getV"
    getI = "getI"
    measV = "measV"
    measI = "measI"


_MODULE_STATE_FILE = data / "emulator" / "module_state.json"


@app.callback()
def main(verbosity: LogLevel = OPTIONS["verbosity"]):
    log.setLevel(verbosity.value)


def initialize_module_state():
    with resources.as_file(data / "emulator/module_state_template.json") as path:
        shutil.copyfile(path, _MODULE_STATE_FILE)


def get_module_state():
    # Copy module state from template if not existing
    if not _MODULE_STATE_FILE.is_file():
        initialize_module_state()

    with _MODULE_STATE_FILE.open() as serialized:
        return json.load(serialized)


def update_module_state(state):
    with _MODULE_STATE_FILE.open("w") as serialized:
        json.dump(state, serialized, indent=4)


def update_Vmux(chip_state):
    """
    This function updates the Vmux voltage values to the corresponding channel.
    Currently emulates MonitorV = 1, 30, 33, 37, 34, 38, 36, 32, and
    MonitorI = 0, 28, 29, 30, 31, 63.
    For other MonitorV and MonitorI channels, return a random number between 0 and 2.
    One needs to write a new if statement for a new MonitorV or MonitorI.
    Note that all grounds are assumed to be perfect (0V). R_Imux is assumed to be 10kohm.
    Also updates the internal ADC based on MonitorV/I setting
    """
    if chip_state["MonitorV"] == 0:
        chip_state["Vmux"] = 0.0
    elif chip_state["MonitorV"] == 1:
        if chip_state["MonitorI"] == 0:
            chip_state["Vmux"] = chip_state["Iref"] * 10000.0
        elif chip_state["MonitorI"] == 28:
            chip_state["Vmux"] = chip_state["IinA"] * 10000.0 / 21000.0
        elif chip_state["MonitorI"] == 29:
            chip_state["Vmux"] = chip_state["IshuntA"] * 10000.0 / 26000.0
        elif chip_state["MonitorI"] == 30:
            chip_state["Vmux"] = chip_state["IinD"] * 10000.0 / 21000.0
        elif chip_state["MonitorI"] == 31:
            chip_state["Vmux"] = chip_state["IshuntD"] * 10000.0 / 26000.0
        elif chip_state["MonitorI"] == 9:
            # Typical Imux9 value for NTC pad current.
            chip_state["Vmux"] = 0.054
        elif (
            (chip_state["MonitorI"] <= 63 and chip_state["MonitorI"] >= 32)
            or (chip_state["MonitorI"] == 26)
            or (chip_state["MonitorI"] == 27)
        ):
            chip_state["Vmux"] = 0.0
        else:
            # If non of the above MonitorI settings are satisfied, return a random number between 0 and 2.
            chip_state["Vmux"] = 2 * rng.random()
    elif chip_state["MonitorV"] == 30:
        chip_state["Vmux"] = 0
    elif chip_state["MonitorV"] == 33:
        chip_state["Vmux"] = chip_state["VinA"] / 4.0
    elif chip_state["MonitorV"] == 37:
        chip_state["Vmux"] = chip_state["VinD"] / 4.0
    elif chip_state["MonitorV"] == 34:
        chip_state["Vmux"] = chip_state["VDDA"] / 2.0
    elif chip_state["MonitorV"] == 38:
        chip_state["Vmux"] = chip_state["VDDD"] / 2.0
    elif chip_state["MonitorV"] == 36:
        chip_state["Vmux"] = chip_state["Vofs"] / 4.0
    elif chip_state["MonitorV"] == 32:
        chip_state["Vmux"] = chip_state["VrefOVP"] / 3.33
    elif chip_state["MonitorV"] == 8:
        # When measuring voltage for VcalMed or VCalHigh, it's essentially computing a liner equation plus/minus
        # a random number. The random number is generated within (-0.005, 0.005). The seed is set global so it's
        # deterministic and reproducible.
        if chip_state["InjVcalRange"] == 1:
            chip_state["Vmux"] = chip_state["InjVcalMed"] / 4096 * 0.8 + 0.005 * (
                2 * rng.random() - 1
            )
        elif chip_state["InjVcalRange"] == 0:
            chip_state["Vmux"] = chip_state["InjVcalMed"] / 4096 * 0.4 + 0.005 * (
                2 * rng.random() - 1
            )
    elif chip_state["MonitorV"] == 7:
        if chip_state["InjVcalRange"] == 1:
            chip_state["Vmux"] = chip_state["InjVcalHigh"] / 4096 * 0.8 + 0.005 * (
                2 * rng.random() - 1
            )
        elif chip_state["InjVcalRange"] == 0:
            chip_state["Vmux"] = chip_state["InjVcalHigh"] / 4096 * 0.4 + 0.005 * (
                2 * rng.random() - 1
            )
    elif chip_state["MonitorV"] == 2:
        # Typical Vmux value for NTC pad voltage.
        chip_state["Vmux"] = 0.084
    elif chip_state["MonitorV"] == 63:
        chip_state["Vmux"] = 0.0
    else:
        # If non of the above MonitorV settings are satisfied, return a random number between 0 and 2.
        chip_state["Vmux"] = 2 * rng.random()

    if chip_state["MonitorV"] == 30:
        chip_state["MonitoringDataAdc"] = 0
    else:
        if chip_state.get("ADCcalOffset") and chip_state.get("ADCcalSlope"):
            chip_state["MonitoringDataAdc"] = round(
                (chip_state["Vmux"] - chip_state["ADCcalOffset"])
                / chip_state["ADCcalSlope"]
            )
        else:
            chip_state["MonitoringDataAdc"] = 0

    return chip_state


@app.command()
def scanConsole(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    scan: Optional[Path] = typer.Option(
        None,
        "-s",
        "--scan",
        help="Scan config",
        # exists=True,  # NB: enable when fixed for emulator (does not check for valid paths)
        file_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
    ),
    _num_threads: int = typer.Option(
        1,
        "-n",
        "--nThreads",
        help="Number of threads",
    ),
    _output_dir: Path = typer.Option(
        "./",
        "-o",
        "--output-dir",
        help="output directory",
        exists=False,
        writable=True,
    ),
    _skip_reset: bool = typer.Option(
        False,
        "--skip-reset",
        help="skip reset",
    ),
):
    """
    This function emulates the effect of running YARR scanConsole to configure chips
    """

    module_state = get_module_state()

    with connectivity.open() as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    for chip in range(nChips):
        config_path = spec_connectivity["chips"][chip]["config"]
        with connectivity.parent.joinpath(config_path).open() as path:
            spec = json.load(path)
        GlobalConfig = spec["RD53B"]["GlobalConfig"]
        Parameter = spec["RD53B"]["Parameter"]
        # VDDA/D should be trimmed to 1.2 after chip configuring
        module_state[f"Chip{chip+1}"]["VDDA"] = min(1.2, module_state["Vin"])
        module_state[f"Chip{chip+1}"]["VDDD"] = min(1.2, module_state["Vin"])
        # MonitorI and V set according to chip configs
        module_state[f"Chip{chip+1}"]["MonitorI"] = GlobalConfig.get("MonitorI", 0)
        module_state[f"Chip{chip+1}"]["MonitorV"] = GlobalConfig.get("MonitorV", 0)
        # set InjVcalMed, InjVcalHigh and InjVcalRange based on the chip configs
        module_state[f"Chip{chip+1}"]["InjVcalMed"] = GlobalConfig.get("InjVcalMed", 0)
        module_state[f"Chip{chip+1}"]["InjVcalHigh"] = GlobalConfig.get(
            "InjVcalHigh", 0
        )
        module_state[f"Chip{chip+1}"]["InjVcalRange"] = GlobalConfig.get(
            "InjVcalRange", 0
        )
        module_state[f"Chip{chip+1}"]["MonitoringDataAdc"] = GlobalConfig.get(
            "MonitoringDataAdc", 0
        )
        ADCcalPar = Parameter.get("ADCcalPar", [0, 0, 0])
        module_state[f"Chip{chip+1}"]["ADCcalOffset"] = ADCcalPar[0] * 0.001
        module_state[f"Chip{chip+1}"]["ADCcalSlope"] = ADCcalPar[1] * 0.001

        # Update Vmux
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    update_module_state(module_state)

    # YARR returns 0 when scan is run
    if scan is not None:
        raise typer.Exit(0)
    raise typer.Exit(1)


@app.command()
def write_register(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    name: str = typer.Argument(),
    value: str = typer.Argument(),
):
    """
    This function emulates the effect of running YARR write-register
    Currently only emulates register MonitorI, MonitorV. One needs to add a new if statement for a new register name.
    """
    module_state = get_module_state()

    with connectivity.open() as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    log.info("%s, %s", name, value)

    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue
        if name == "MonitorI":
            module_state[f"Chip{chip+1}"]["MonitorI"] = value
        elif name == "MonitorV":
            module_state[f"Chip{chip+1}"]["MonitorV"] = value
        elif name == "InjVcalMed":
            module_state[f"Chip{chip+1}"]["InjVcalMed"] = value
        elif name == "InjVcalHigh":
            module_state[f"Chip{chip+1}"]["InjVcalHigh"] = value
        elif name == "InjVcalRange":
            module_state[f"Chip{chip+1}"]["InjVcalRange"] = value
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    update_module_state(module_state)


@app.command()
def read_register(
    name: str,
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
):
    """
    This function emulates the effect of running YARR read-register
    Currently only emulates register SldoTrimA and SldoTrimD. One needs to add a new if statement for a new register name.
    """

    with connectivity.open() as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue
        if name == "SldoTimA" or name == "SldoTrimD":
            sys.stdout.write("8")
            raise typer.Exit(0)

        sys.stdout.write("0")
        raise typer.Exit(0)


@app.command()
def control_PS(
    action: PSAction = typer.Option(
        ...,
        "-a",
        "--action",
        help="Action to PS",
    ),
    voltage: float = typer.Option(
        None,
        "-v",
        "--voltage",
        help="Set voltage",
    ),
    current: float = typer.Option(
        None,
        "-i",
        "--current",
        help="Set current",
    ),
):
    """
    This function emulates the effect of powering the module
    """
    if action == "off":
        # Turning off the power simply means module states go back to initial states. Thus copy the initial states from the template
        initialize_module_state()
        raise typer.Exit(0)

    module_state = get_module_state()

    if action == "getV" or action == "measV":
        # measure Vin
        v = module_state["Vin"]
        sys.stdout.write(f"{v}")
        raise typer.Exit(0)

    if action == "getI" or action == "measI":
        # measure Iin
        i = module_state["Iin"]
        sys.stdout.write(f"{i}")
        raise typer.Exit(0)

    if action == "on":
        if current is None or voltage is None:
            typer.echo(
                f"Must set LV voltage and current. (voltage: {voltage}, current: {current}"
            )
            raise typer.Exit(2)

        nChips = module_state["nChips"]

        # check if the module has already been powered on
        already_power = module_state["Vin"] > 0

        #### TODO: LV is off for for IV_MEASURE, do this??
        # if not already_power:
        # module_state["Vin"] = 0
        # module_state["Iin"] = 0

        # Calculate Vin based on the prediction (slope and offset), as well as the voltage and the current set to the power supply
        module_state["Vin"] = min(0.348293 / nChips * current + 1, voltage, 2.0)
        # Calculate Iin from the calculated Vin
        module_state["Iin"] = (module_state["Vin"] - 1) * nChips / 0.348293
        # Assume temperature increases linearly with Iin
        module_state["temperature"] = 25.0 + module_state["Iin"] * 2.0
        for chip in range(nChips):  # loop over all the chips
            # VinA = VinD = Vin
            module_state[f"Chip{chip+1}"]["VinA"] = module_state["Vin"]
            module_state[f"Chip{chip+1}"]["VinD"] = module_state["Vin"]
            # Fun assumption: VDDA/D = 1.1 before configuring; otherwise stay the same values
            module_state[f"Chip{chip+1}"]["VDDA"] = min(
                1.1 if not already_power else module_state[f"Chip{chip+1}"]["VDDA"],
                module_state["Vin"],
            )
            module_state[f"Chip{chip+1}"]["VDDD"] = min(
                1.1 if not already_power else module_state[f"Chip{chip+1}"]["VDDD"],
                module_state["Vin"],
            )
            module_state[f"Chip{chip+1}"]["Vofs"] = min(
                1.0, module_state["Vin"]
            )  # VOFS = 1V
            module_state[f"Chip{chip+1}"]["VrefOVP"] = 2.0  # VrefOVP = 2V
            module_state[f"Chip{chip+1}"]["IinA"] = (
                module_state["Iin"] / nChips / 2
            )  # IinA = Iin/nChips/2
            module_state[f"Chip{chip+1}"]["IinD"] = (
                module_state["Iin"] / nChips / 2
            )  # IinD = Iin/nChips/2
            module_state[f"Chip{chip+1}"]["IcoreA"] = min(
                0.2, module_state["Iin"] / nChips / 2
            )  # ICoreA assumed to be 0.2A
            module_state[f"Chip{chip+1}"]["IcoreD"] = min(
                0.2, module_state["Iin"] / nChips / 2
            )  # ICoreD assumed to be 0.2A
            module_state[f"Chip{chip+1}"]["IshuntA"] = (
                module_state[f"Chip{chip+1}"]["IinA"]
                - module_state[f"Chip{chip+1}"]["IcoreA"]
            )  # IShunt = Iin - Icore
            module_state[f"Chip{chip+1}"]["IshuntD"] = (
                module_state[f"Chip{chip+1}"]["IinD"]
                - module_state[f"Chip{chip+1}"]["IcoreD"]
            )
            module_state[f"Chip{chip+1}"]["Iref"] = 4e-6  # Iref = 4 uA
            if not already_power:
                module_state[f"Chip{chip+1}"]["MonitorI"] = 0  # default minitorI = 0
            if not already_power:
                module_state[f"Chip{chip+1}"]["MonitorV"] = 0  # default minitorV = 0
            module_state[f"Chip{chip+1}"] = update_Vmux(
                module_state[f"Chip{chip+1}"]
            )  # update Vmux voltage

        update_module_state(module_state)


@app.command()
def control_HV(
    action: PSAction = typer.Option(
        ...,
        "-a",
        "--action",
        help="Action to HV PS",
    ),
    voltage: float = typer.Option(
        0.0,
        "-v",
        "--voltage",
        help="Set voltage",
    ),
    current: float = typer.Option(
        0.0,
        "-i",
        "--current",
        help="Set current",
    ),
):
    """
    This function emulates the effect of powering the module
    """
    if action == "off":
        # Turning off the power simply means module states go back to initial states. Thus copy the initial states from the template
        initialize_module_state()
        raise typer.Exit(0)

    module_state = get_module_state()

    if action == "getV":
        # measure the bias voltage
        v = module_state["Vbias"]
        sys.stdout.write(f"{v}")
        raise typer.Exit(0)

    if action == "getI":
        # measure the leakage current
        i = module_state["Ileak"]
        sys.stdout.write(f"{i}")
        raise typer.Exit(0)

    if action == "on":
        if current is None or voltage is None:
            typer.echo("HV: Must set voltage and current.")
            raise typer.Exit(2)

        module_state["time"] += 2
        module_state["Vbias"] = voltage

        # Calculate Ileak from the Vbias (fit from 20UPIS25300160)
        # Don't use theoretical calc because basically constant
        a = -9.04601528e-14
        b = 9.99999999e-01
        module_state["Ileak"] = a * (np.exp(b * voltage) - 1)

        # Assume temperature increases linearly with Iin
        module_state["temperature"] = round(np.random.uniform(22.0, 24.0), 3)

        update_module_state(module_state)


@app.command()
def measureV():
    """
    This function emulates the effect of multimeter (measuring the Vmux)
    """
    module_state = get_module_state()

    nChips = module_state["nChips"]

    v = 0
    for chip in range(nChips):
        v += module_state[f"Chip{chip+1}"]["Vmux"]
    sys.stdout.write(f"{v}")
    raise typer.Exit(0)


@app.command()
def read_adc(
    vmux: int,
    _controller: Path = OPTIONS["emulator_controller"],
    _connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    read_current: bool = typer.Option(
        False,
        "-I",
        "--readCurrent",
        help="Read current instead of voltage",
    ),
    read_raw: bool = typer.Option(
        False,
        "-R",
        "--rawCounts",
        help="Read raw ADC counts",
    ),
):
    """
    This function emulates the effect of ADC reading
    R_Imux is assumed to be 10kohm.
    """
    module_state = get_module_state()

    nChips = module_state["nChips"]

    # Update Vmux settings first
    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue
        if read_current:
            module_state[f"Chip{chip+1}"]["MonitorV"] = 1
            module_state[f"Chip{chip+1}"]["MonitorI"] = vmux
        else:
            module_state[f"Chip{chip+1}"]["MonitorV"] = vmux
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    # Then read ADC
    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue
        if read_raw:
            v = module_state[f"Chip{chip+1}"]["MonitoringDataAdc"]
            u = ""
        elif read_current:
            v = (module_state[f"Chip{chip+1}"]["Vmux"] / 10000.0) / 1e-6
            u = "uA"
        else:
            v = module_state[f"Chip{chip+1}"]["Vmux"]
            u = "V"
        sys.stdout.write(f"{v} {u}")
    raise typer.Exit(0)


@app.command()
def read_ringosc(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
):
    """
    This function emulates the effect of ROSC reading
    """

    with connectivity.open() as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue

        rosc_freq = "500 " * 42
        sys.stdout.write(rosc_freq)
    raise typer.Exit(0)


@app.command()
def eye_diagram(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    dryrun: bool = OPTIONS["dry_run"],
    skipconfig: bool = OPTIONS["skip_config"],
    testsize: int = OPTIONS["test_size"],
):
    """
    This function emulates the effect of EYE DIAGRAM
    """

    with connectivity.open() as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    testdata = {}
    testdata["Delay"] = []
    for d in range(32):
        testdata["Delay"] += [d]

    for lane in range(16):
        testdata[f"lane{lane}"] = 32 * [0.0]

    for chip in range(nChips):
        if chip_position is not None and chip is not chip_position:
            continue

        testdata[f"lane{chip_position}"] = rng.random(32)

    string = ""
    for i in testdata["Delay"]:
        for key in testdata:
            string += str(round(testdata[key][i], 2)) + " | "
        string += "\n"

    for lane in range(len(testdata) - 1):
        if chip_position is not None and lane is not chip_position:
            string += (
                f"[  info  ][  eyeDiagram   ]: No good delay setting for lane {lane}"
            )
        else:
            eyewidth = round(31 * rng.random(), 0)
            delay = round(31 * rng.random(), 0)
            string += f"[  info  ][  eyeDiagram   ]: Delay setting for lane {lane} with eye width {eyewidth}: {delay}"
        string += "\n"

    if dryrun:
        string += "All done, without updating the emulator controller config!"
    else:
        string += f"Writing to emulator controller config {_controller}"

    if skipconfig:
        pass
    if testsize is not None:
        pass

    sys.stdout.write(string)

    raise typer.Exit(0)


@app.command()
def measureT():
    """
    This function emulates the effect of NTC (measure module temperature)
    """
    module_state = get_module_state()

    T = module_state["temperature"]
    sys.stdout.write(f"{T}")
    raise typer.Exit(0)


@app.command()
def switchLPM(_: PSAction):
    raise typer.Exit(0)


def run_scanConsole():
    typer.run(scanConsole)


def run_write_register():
    typer.run(write_register)


def run_read_register():
    typer.run(read_register)


def run_read_adc():
    typer.run(read_adc)


def run_read_ringosc():
    typer.run(read_ringosc)


def run_switchLPM():
    typer.run(switchLPM)


def run_control_PS():
    typer.run(control_PS)


def run_control_HV():
    typer.run(control_HV)


def run_measureV():
    typer.run(measureV)


def run_measureT():
    typer.run(measureT)


def run_eyeDiagram():
    typer.run(eye_diagram)


if __name__ == "__main__":
    app()
