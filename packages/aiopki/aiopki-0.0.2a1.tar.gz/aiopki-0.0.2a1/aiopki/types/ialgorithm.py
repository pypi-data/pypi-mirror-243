# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol

from cryptography.hazmat.primitives.ciphers.modes import GCM


class IAlgorithm(Protocol):
    __module__: str = 'aiopki.types'
    name: str

    def get_digest_algorithm(self) -> Any: ...
    def get_padding(self) -> Any: ...

    def digest(self, value: bytes) -> bytes:
        raise NotImplementedError

    def get_initialization_vector(self, iv: bytes | None = None, tag: bytes | None = None) -> tuple[GCM, bytes]:
        raise NotImplementedError

    def supports_aad(self) -> bool:
        raise NotImplementedError