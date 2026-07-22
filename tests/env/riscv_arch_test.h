# riscv_arch_test.h
# Top-level riscv-arch-test header file
# Jordan Carlin jcarlin@hmc.edu October 2025
# SPDX-License-Identifier: Apache-2.0

#include "rvtest_config.h"
#undef H_SUPPORTED // TODO: Remove this once Sail supports Hypervisor
#include "derived_config.h"
#include "encoding.h"
#include "utils.h"
#include "rvmodel_macros.h"

// Record an expected architectural exception in the ELF. Models may override
// this hook to integrate the expectation with an in-target trap observer.
#ifndef RVMODEL_EXPECT_EXCEPTION
#define RVMODEL_EXPECT_EXCEPTION(_CAUSE) \
  .global rvtest_expected_exception;   \
  .set rvtest_expected_exception, _CAUSE;
#endif
#ifndef RVTEST_SELFCHECK
  #include "sail_macros.h"
#endif
#include "check_defines.h"
#include "signature.h"
#include "rvtest_macros.h"
#include "rvtest_pmp_macros.h"
#ifdef RVTEST_VECTOR
  #include "rvtest_macros_vector.h"
#endif
#ifdef RVTEST_HYPERVISOR
  #include "rvtest_macros_hypervisor.h"
#endif
#include "rvtest_trap_handler.h"
#include "rvtest_failure_code.h"
#include "rvtest_setup.h"
