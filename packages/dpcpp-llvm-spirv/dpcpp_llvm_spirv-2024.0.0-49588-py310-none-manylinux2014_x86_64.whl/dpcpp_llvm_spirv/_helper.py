# SPDX-FileCopyrightText: 2020 - 2022 Intel Corporation
#
# SPDX-License-Identifier: Proprietary

import os
import platform


def get_llvm_spirv_path():
    """Returns the path to llvm-spirv executable
    vendored in this package.
    """

    result = os.path.join(os.path.dirname(__file__), "bin")

    if platform.system() is "Windows":
        result += "\llvm-spirv.exe"
    else:
        result += "/llvm-spirv"

    return result
