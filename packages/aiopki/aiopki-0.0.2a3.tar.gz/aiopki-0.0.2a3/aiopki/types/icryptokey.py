# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generator
from typing import Iterable
from typing import Protocol

from .ialgorithm import IAlgorithm


class ICryptoKey(Protocol):
    __module__: str = 'aiopki.types'

    @property
    def public(self) -> Any:
        ...

    @property
    def thumbprint(self) -> str:
        ...

    def can_use(self, algorithm: IAlgorithm) -> bool: ...
    def default(self) -> 'ICryptoKey': ...
    def default_algorithm(self) -> IAlgorithm: ...
    def get_thumbprint(self) -> str: ...
    def is_available(self) -> bool: ...
    def versions(self) -> Iterable['ICryptoKey']: ...

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bytes:
        ...

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bool:
        ...

    def __await__(self) -> Generator[Any, Any, 'ICryptoKey']: ...