##################################
# generate/exception.py
#
# SPDX-License-Identifier: Apache-2.0
##################################

"""Generate neutral exception stimuli for an external observer."""

from pathlib import Path
from random import seed

from testgen.asm.helpers import reproducible_hash
from testgen.data.config import ExpectedOutcome, TestConfig
from testgen.data.state import TestData
from testgen.exception import get_exception_cases
from testgen.io.writer import write_test_file


def generate_exception_tests(output_test_dir: Path) -> None:
    """Generate one independently terminating ELF source per exception case."""
    output_path = output_test_dir / "exception" / "ExceptionsI"
    output_path.mkdir(parents=True, exist_ok=True)

    for case in get_exception_cases():
        config = TestConfig(
            xlen=0,
            flen=64,
            testsuite="ExceptionsI",
            required_extensions=list(case.required_extensions),
            forbidden_extensions=list(case.forbidden_extensions),
            extra_params=list(case.params),
            expected_outcome=ExpectedOutcome(kind="exception", cause=case.cause),
        )
        data = TestData(config)
        reserved = [0, 1, 7, 10, 11, 12, *range(16, 32)]
        data.int_regs.consume_registers(reserved)
        seed(reproducible_hash(case.name))
        chunk = data.begin_test_chunk(case.name)
        chunk.code.extend(case.stimulus(data, "ExceptionsSm_cg"))
        chunk.code.append("RVMODEL_HALT_FAIL")
        chunk = data.end_test_chunk()
        write_test_file(config, None, [chunk], output_path, split_name=case.name)
        data.int_regs.return_registers(reserved)
        data.destroy()
