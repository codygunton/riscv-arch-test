##################################
# exception/registry.py
#
# SPDX-License-Identifier: Apache-2.0
##################################

"""Registry of observer-independent architectural exception cases."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from testgen.data.state import TestData
from testgen.exception.common import (
    generate_breakpoint_tests,
    generate_illegal_instruction_tests,
    generate_instr_access_fault_tests,
    generate_load_access_fault_tests,
    generate_store_access_fault_tests,
)

StimulusGenerator = Callable[[TestData, str], list[str]]


@dataclass(frozen=True)
class ExceptionCase:
    """A stimulus and its architectural outcome, independent of how it is observed."""

    name: str
    cause: int
    stimulus: StimulusGenerator
    required_extensions: tuple[str, ...] = ("I",)
    forbidden_extensions: tuple[str, ...] = ()
    params: tuple[str, ...] = ()


def _illegal(encoding: str) -> StimulusGenerator:
    name = f"illegal_{encoding.lower()}"

    def generate(test_data: TestData, covergroup: str) -> list[str]:
        return generate_illegal_instruction_tests(test_data, covergroup, encodings=((name, encoding),))

    return generate


def _load(op: str) -> StimulusGenerator:
    def generate(test_data: TestData, covergroup: str) -> list[str]:
        return generate_load_access_fault_tests(test_data, covergroup, use_sigupd=False, operations=(op,))

    return generate


def _store(op: str) -> StimulusGenerator:
    def generate(test_data: TestData, covergroup: str) -> list[str]:
        return generate_store_access_fault_tests(test_data, covergroup, operations=(op,))

    return generate


def _instruction_access_fault(test_data: TestData, covergroup: str) -> list[str]:
    return generate_instr_access_fault_tests(test_data, covergroup, use_trap_handler_sentinel=False)


def get_exception_cases() -> tuple[ExceptionCase, ...]:
    """Return neutral cases currently suitable for an external exception observer."""
    return (
        ExceptionCase("IllegalZero", 2, _illegal("0x00000000")),
        ExceptionCase("IllegalOnes", 2, _illegal("0xFFFFFFFF")),
        ExceptionCase("Breakpoint", 3, generate_breakpoint_tests),
        ExceptionCase(
            "InstructionAccessFault",
            1,
            _instruction_access_fault,
            params=("RVMODEL_ACCESS_FAULT_ADDRESS_DEFINED: true",),
        ),
        *(ExceptionCase(f"LoadAccessFault{op.title()}", 5, _load(op), params=("RVMODEL_ACCESS_FAULT_ADDRESS_DEFINED: true",)) for op in ("lb", "lbu", "lh", "lhu", "lw", "lwu", "ld")),
        *(ExceptionCase(f"StoreAccessFault{op.title()}", 7, _store(op), params=("RVMODEL_ACCESS_FAULT_ADDRESS_DEFINED: true",)) for op in ("sb", "sh", "sw", "sd")),
    )
