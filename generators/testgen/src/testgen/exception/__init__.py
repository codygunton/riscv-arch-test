##################################
# exception/__init__.py
#
# SPDX-License-Identifier: Apache-2.0
##################################

"""Neutral architectural exception cases and observer-independent metadata."""

from testgen.exception.registry import ExceptionCase, get_exception_cases

__all__ = ["ExceptionCase", "get_exception_cases"]
