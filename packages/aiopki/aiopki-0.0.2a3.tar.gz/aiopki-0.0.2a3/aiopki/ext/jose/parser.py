
# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools

from .joseobject import JOSEObject



@functools.singledispatch
def parse(value: bytes | str) -> JOSEObject:
    raise NotImplementedError(type(value).__name__)


@parse.register
def parse_compact(value: str) -> JOSEObject:
    return JOSEObject.parse_compact(value)


@parse.register
def parse_compact_bytes(value: bytes) -> JOSEObject:
    return JOSEObject.parse_compact(value)