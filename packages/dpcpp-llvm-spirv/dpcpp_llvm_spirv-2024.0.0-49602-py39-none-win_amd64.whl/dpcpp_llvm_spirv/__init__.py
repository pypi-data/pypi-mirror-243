# SPDX-FileCopyrightText: 2020 - 2022 Intel Corporation
#
# SPDX-License-Identifier: Proprietary

__doc__ = """ dpcpp_llvm_spirv Python package vendors llvm-spirv executable from Intel(R) oneAPI DPC++ compiler.

It provides `dpcpp_llvm_spirv.get_llvm_spirv_path()` function to query the path of the vendored executable.
"""

from ._helper import get_llvm_spirv_path

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = "0.0.0+dev"

__all__ = ["get_llvm_spirv_path", "__version__"]
