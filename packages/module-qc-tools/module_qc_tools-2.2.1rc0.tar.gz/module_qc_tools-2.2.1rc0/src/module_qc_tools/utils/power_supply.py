#!/usr/bin/env python3
from __future__ import annotations

import logging

import numpy as np

from module_qc_tools.utils.hardware_control_base import hardware_control_base

log = logging.getLogger("measurement")


class power_supply(hardware_control_base):
    def __init__(self, config, name="power_supply", *args, **kwargs):
        self.on_cmd = ""
        self.off_cmd = ""
        self.set_cmd = ""
        self.ramp_cmd = ""
        self.getV_cmd = ""
        self.getI_cmd = ""
        self.measV_cmd = ""
        self.measI_cmd = ""
        self.polarity = 1
        self.n_try = 0
        self.success_code = 0
        super().__init__(config, name, *args, **kwargs)
        if "emulator" in self.on_cmd:
            log.info(f"[{name}] running power supply emulator!!")

    def on(self, v=None, i=None):
        cmd = f'{self.on_cmd.replace("{v}", str(v)).replace("{i}", str(i))}'

        return self.send_command(
            cmd,
            purpose=f"turn on power supply with {v}V, {i}A",
            pause=1,
            success_code=self.success_code,
        )

    def set(self, v=None, i=None):
        cmd = f'{self.set_cmd.replace("{v}", str(v)).replace("{i}", str(i))}'

        return self.send_command(
            cmd,
            purpose=f"set power supply to {v}V, {i}A",
            pause=1,
            success_code=self.success_code,
        )

    def off(self):
        return self.send_command(
            self.off_cmd,
            purpose="turn off power supply",
            extra_error_messages=[
                f"Run directory: `{self.run_dir}`"
                f"Off command: `{self.off_cmd}`"
                "Please manually turn off power supply!!"
            ],
            success_code=self.success_code,
        )

    def getV(self):
        return self.send_command_and_read(
            self.getV_cmd,
            purpose="inquire set voltage",
            unit="V",
            max_nTry=self.n_try,
            success_code=self.success_code,
        )

    def getI(self):
        return self.send_command_and_read(
            self.getI_cmd,
            purpose="inquire set current",
            unit="A",
            max_nTry=self.n_try,
            success_code=self.success_code,
        )

    def measV(self):
        return self.send_command_and_read(
            self.measV_cmd,
            purpose="measure output voltage",
            unit="V",
            max_nTry=self.n_try,
            success_code=self.success_code,
        )

    def measI(self):
        return self.send_command_and_read(
            self.measI_cmd,
            purpose="measure output current",
            unit="A",
            max_nTry=self.n_try,
            success_code=self.success_code,
        )

    def rampV(self, v=None, i=None, stepsize=5):
        if self.ramp_cmd:
            cmd = (
                f'{self.ramp_cmd.replace("{v}", str(v)).replace("{r}", str(stepsize))}'
            )
            return self.send_command(
                cmd,
                purpose=f"ramp power supply to {v}V at {stepsize}V/s",
                pause=1,
                success_code=self.success_code,
            )

        v_init, v_status = self.getV()
        v_final = v
        v_diff = v_final - v_init  ## gives the correct sign for the ramping direction
        log.debug("v_diff " + str(v_diff))
        stepsize = np.sign(v_diff) * stepsize
        log.debug("stepsize " + str(stepsize))
        if stepsize != 0:
            nsteps = int(v_diff / stepsize)
            log.debug("nsteps " + str(nsteps))
            v_target = v_init
            for _step in range(nsteps):
                v_target = v_target + stepsize
                log.debug("step " + str(_step) + " target " + str(v_target))
                self.set(v_target, i)  ## sleeps for 1 sec
        self.set(v_final, i)  # last step
        return self.getV()
