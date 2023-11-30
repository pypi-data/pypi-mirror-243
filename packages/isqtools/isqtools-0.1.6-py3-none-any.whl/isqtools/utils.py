# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""This file provides some utility functions for calling the ``isqc`` compiler
from python."""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from collections.abc import Sequence
from typing import Literal

TARGET = Literal["qir", "open-qasm3", "qcis"]


class _IsqcPath:
    """Default ``isqc`` path."""

    __slot__ = ("default_isqc_path",)
    default_isqc_path = ""


_default_isqc_path = _IsqcPath()


def get_isqc_path() -> str:
    return _default_isqc_path.default_isqc_path


def set_isqc_path(isqc_path: str) -> None:
    _default_isqc_path.default_isqc_path = os.path.expanduser(isqc_path)


class IsqcError(Exception):
    """IsQ compiler Error."""


def compile(
    file: str,
    target: TARGET = "qir",
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    additional_args: str = "",
) -> None:
    """This function encapsulates the ``compile`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        target: The compiled target output form:
                1) qir;
                2) open-qasm3;
                3) qcis.
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        additional_args: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    """

    file = os.path.expanduser(file)

    target_cmd = f"--target {target}"
    int_cmd, double_cmd = _deal_params(int_param, double_param)
    isqc_path = os.path.join(_default_isqc_path.default_isqc_path, "isqc")
    compile_cmd = (
        f"{isqc_path} compile {file} "
        f"{target_cmd} {int_cmd} {double_cmd} "
        f"{additional_args}"
    )

    out = subprocess.run(
        compile_cmd,
        shell=True,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
    )
    if out.returncode != 0:
        raise IsqcError(
            f"Compile Failed! "
            f"Error code: {out.returncode}."
            # f"Error message: {out.stdout.decode()} {out.stderr.decode()}"
        )


def simulate(
    file: str,
    shots: int = 100,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    additional_args: str = "",
) -> dict[str, int]:
    """This function encapsulates the ``simulate`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        shots: Shots number of quantum simulation.
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        additional_args: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    """

    file = os.path.expanduser(file)

    if file.endswith(".so"):
        so_file = file
    elif file.endswith(".isq"):
        so_file = os.path.splitext(file)[0] + ".so"
    else:
        raise IsqcError(
            f"`{file}`'s format is not supported.\n"
            "Please use `.isq` or `.so`"
        )

    if not os.path.exists(so_file):
        raise IsqcError(
            f"`{so_file}` does not exit. Please compile isQ file first."
        )

    int_cmd, double_cmd = _deal_params(int_param, double_param)
    isqc_path = os.path.join(_default_isqc_path.default_isqc_path, "isqc")
    simulate_cmd = (
        f"{isqc_path} simulate {int_cmd} {double_cmd} --shots {shots} "
        f"{additional_args} {so_file}"
    )

    out = subprocess.run(
        simulate_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if out.returncode != 0:
        raise IsqcError(
            "Simulate Failed! "
            f"Error code: {out.returncode}\n"
            f"Error message: {out.stdout.decode()} {out.stderr.decode()}"
        )

    return dict(json.loads(out.stdout))


def run(
    file: str,
    target: TARGET = "qir",
    shots: int = 100,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
) -> dict[str, int]:
    """This method executes ``compile`` and ``simulate`` in sequence."""

    compile(
        file=file,
        target=target,
    )

    return simulate(
        file=file,
        shots=shots,
        int_param=int_param,
        double_param=double_param,
    )


def _deal_params(
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
) -> tuple[str, str]:
    """Convert integer and double parameters supported by isQ compiler."""

    int_cmd = ""
    double_cmd = ""
    if int_param is not None:
        if isinstance(int_param, int):
            int_param = [int_param]
        int_param = list(int_param)
        int_cmd = []
        for each_int in int_param:
            int_cmd.append(f"-i {each_int}")
        int_cmd = " ".join(int_cmd)

    if double_param is not None:
        if isinstance(double_param, float):
            double_param = [double_param]
        double_param = list(double_param)
        double_cmd = []
        for each_double in double_param:
            double_cmd.append(f"-d {each_double}")
        double_cmd = " ".join(double_cmd)
    return int_cmd, double_cmd


def _gen_qcis_from_so(
    file: str,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    additional_args: str = "",
) -> None:
    """According to the compilation plan of isQ compiler, this function is not
    open to users.
    """

    file = os.path.expanduser(file)
    int_cmd, double_cmd = _deal_params(int_param, double_param)
    qcis_path = os.path.splitext(file)[0] + ".qcis"

    FindSimulator.makeSimulatorBIN()
    simulator_exec = FindSimulator.get_simulatorBIN_path()

    simulate_cmd = (
        f"{simulator_exec} {file} --qcisgen -e __isq__entry "
        f"{int_cmd} {double_cmd} {additional_args} "
        f"> {qcis_path}"
    )

    out = subprocess.run(
        simulate_cmd,
        shell=True,
        stderr=subprocess.PIPE,
    )

    if out.returncode != 0:
        raise IsqcError(
            "Generate QCIS Failed! "
            f"Error code: {out.returncode}"
            f"Error message: {out.stderr.decode()}"
        )


class FindSimulator:
    """To build a SIMULATOR BIN for isqc."""

    def __init__(self) -> None:
        self.makeSimulatorBIN()

    @staticmethod
    def set_simulator_file_name():
        return "SIMULATOR"

    @staticmethod
    def get_dir_name_of_simulator(isqcDIR):
        storeDIR = os.path.join(isqcDIR, "nix", "store")
        messList = os.listdir(storeDIR)
        for line in messList:
            if "simulator" in line:
                return line.strip()
        logging.error("cannot find simulator dir")

    @staticmethod
    def get_isQ_dir():
        if not get_isqc_path():
            isqcBIN = os.popen("which isqc").read().strip()
            isqcDIR = os.path.dirname(isqcBIN)
            return isqcDIR
        return get_isqc_path()

    @classmethod
    def get_simulatorBIN_path(cls):
        return os.path.join(cls.get_isQ_dir(), cls.set_simulator_file_name())

    @classmethod
    def makeSimulatorBIN(cls):
        # will automatically find dir of isqc, and make a SIMULATOR with
        # appropriate chmod
        simBinFile = cls.get_simulatorBIN_path()
        if os.path.exists(simBinFile):
            return
        isQdir = cls.get_isQ_dir()
        messName = cls.get_dir_name_of_simulator(isQdir)
        # replaceKeyWord = f"/nix/store/{messName}/bin/simulator"
        isqcFile = os.path.join(isQdir, "isqc")
        with open(isqcFile, "r") as f:
            isqcContent = f.read()
        slides = isqcContent.split(" ")
        slides[-2] = f"/nix/store/{messName}/bin/simulator"
        simBINcontent = " ".join(slides)
        with open(simBinFile, "w") as f:
            f.write(simBINcontent)
        os.chmod(simBinFile, 0o555)


def split_str(string, sep="\n"):
    # warning: does not yet work if sep is a lookahead like `(?=b)`
    if sep == "":
        return (c for c in string)
    else:
        return (
            _.group(1)
            for _ in re.finditer(f"(?:^|{sep})((?:(?!{sep}).)*)", string)
        )


class QcisParser:
    """Qcis parser"""

    def __init__(self, qcis_str: str) -> None:
        self._qdic = {}
        self._qnum = 0
        self._mq = []
        self._gates = []
        self._get_gates(qcis_str)

    def _get_gates(self, qcis_str: str) -> None:
        for line in qcis_str.split("\n"):
            line = line.strip()
            if not line:
                continue
            data_per_line = line.split(" ")
            if data_per_line[1] not in self._qdic:
                self._qdic[data_per_line[1]] = self._qnum
                self._qnum += 1
            if data_per_line[0] in ["CZ", "CY", "CX", "CNOT"]:
                if data_per_line[2] not in self._qdic:
                    self._qdic[data_per_line[2]] = self._qnum
                    self._qnum += 1

            qid1 = self._qdic[data_per_line[1]]
            if data_per_line[0] == "M":
                self._mq.append(qid1)
            else:
                if data_per_line[0] in ["CZ", "CY", "CX", "CNOT"]:
                    qid2 = self._qdic[data_per_line[2]]
                    self._gates.append((data_per_line[0], (qid1, qid2), None))
                elif data_per_line[0] in ["RX", "RY", "RZ", "RXY"]:
                    self._gates.append(
                        (
                            data_per_line[0],
                            (qid1,),
                            tuple(float(v) for v in data_per_line[2:]),
                        )
                    )
                else:
                    self._gates.append((data_per_line[0], (qid1,), None))

    def getNq(self) -> int:
        """return number of effective qubits"""
        return self._qnum

    def exportGates(self) -> list[tuple[str, tuple[int], tuple[float] | None]]:
        """return [ <gateName>, [intParams], [floatParams] ]"""
        return self._gates

    def getMeasurements(self) -> list[int]:
        """return list of index of qubit for final measurement"""
        return self._mq
