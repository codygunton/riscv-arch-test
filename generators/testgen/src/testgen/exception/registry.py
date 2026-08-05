##################################
# exception/registry.py
#
# SPDX-License-Identifier: Apache-2.0
##################################

"""Registry of observer-independent architectural exception cases."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

from testgen.data.state import TestData
from testgen.exception.common import (
    generate_breakpoint_tests,
    generate_illegal_instruction_test,
)

StimulusGenerator = Callable[[TestData, str], list[str]]


@dataclass(frozen=True)
class ExceptionCase:
    """A stimulus and its architectural outcome, independent of how it is observed."""

    name: str
    group: str
    cause: int
    stimulus: StimulusGenerator
    required_extensions: tuple[str, ...] = ("I",)
    params: tuple[str, ...] = ()


def _illegal(encoding: str) -> StimulusGenerator:
    name = f"illegal_{encoding.lower()}"
    return partial(generate_illegal_instruction_test, name=name, encoding=encoding)


def _misaligned_branch(test_data: TestData, covergroup: str) -> list[str]:
    coverpoint = "cp_instr_adr_misaligned_branch"
    return [
        test_data.add_testcase("taken_beq_pc_6", coverpoint, covergroup),
        "beq x0, x0, .+6",
        "addi x0, x2, 0",
        "nop",
    ]


def _misaligned_jal(test_data: TestData, covergroup: str) -> list[str]:
    coverpoint = "cp_instr_adr_misaligned_jal"
    return [
        test_data.add_testcase("jal_pc_6", coverpoint, covergroup),
        "jal x0, .+6",
        "addi x0, x2, 0",
        "nop",
    ]


def _misaligned_jalr(test_data: TestData, covergroup: str) -> list[str]:
    coverpoint = "cp_instr_adr_misaligned_jalr"
    addr_reg = test_data.int_regs.get_register()
    lines = [
        ".p2align 2",
        f"LA(x{addr_reg}, 1f)",
        test_data.add_testcase("jalr_pc_2", coverpoint, covergroup),
        f"jalr x0, 2(x{addr_reg})",
        "1:",
        "nop",
    ]
    test_data.int_regs.return_registers([addr_reg])
    return lines


def get_exception_cases() -> tuple[ExceptionCase, ...]:
    """Return neutral cases currently suitable for an external exception observer."""
    return (
        ExceptionCase("IllegalZero", "IllegalInstruction", 2, _illegal("0x00000000")),
        ExceptionCase("Breakpoint", "Breakpoint", 3, generate_breakpoint_tests),
        ExceptionCase("InstructionAddressMisalignedBranch", "InstructionAddressMisaligned", 0, _misaligned_branch),
        ExceptionCase("InstructionAddressMisalignedJal", "InstructionAddressMisaligned", 0, _misaligned_jal),
        ExceptionCase("InstructionAddressMisalignedJalr", "InstructionAddressMisaligned", 0, _misaligned_jalr),
    )
