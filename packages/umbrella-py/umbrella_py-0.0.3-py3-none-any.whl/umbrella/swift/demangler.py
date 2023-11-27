# Copyright (c) 2023 MatrixEditor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# APPLE SOURCE CODE LICENSE
# Copyright (c) 2014 - 2017 Apple Inc. and the Swift project authors
# Licensed under Apache License v2.0 with Runtime Library Exception
#
# See https://swift.org/LICENSE.txt for license information
# See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
from __future__ import annotations

import subprocess

from umbrella.runtime import RawCString

# TODO: implement parsing algorithm
MangledName = RawCString


def demangle(__name: bytes) -> str:
    try:
        if not __name.startswith((b"$", b"_")):
            __name = b"$s" + __name
        result = (
            subprocess.check_output(["swift", "demangle", "-compact", __name.decode()])
            .decode()
            .strip()
        )

        # remove extras
        result = result.replace("method descriptor for ", "").replace(
            "nominal type descriptor for ", ""
        )
        if not all(map(lambda x: x.isprintable(), result)):
            return repr(result.encode())[2:-1]
        return result
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return repr(__name)[2:-1]


