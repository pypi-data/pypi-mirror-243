# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Iterable
from typing import TypeVar

import pydantic

from aiopki.types import IAlgorithm
from aiopki.types import ICryptoKey


T = TypeVar('T', bound='BaseCryptoKey')


class BaseCryptoKey(pydantic.BaseModel):

    @property
    def thumbprint(self) -> str:
        return self.get_thumbprint()

    @property
    def public(self) -> Any:
        raise NotImplementedError
    
    def can_use(self, algorithm: IAlgorithm) -> bool:
        raise NotImplementedError

    def default(self) -> ICryptoKey:
        return self

    def default_algorithm(self) -> IAlgorithm:
        raise NotImplementedError

    def get_thumbprint(self) -> str:
        raise NotImplementedError

    def is_available(self) -> bool:
        raise NotImplementedError

    async def _discover(self: T) -> T:
        return await self.discover()
    
    async def discover(self):
        return self

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bytes:
        raise NotImplementedError

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bool:
        raise NotImplementedError

    def versions(self) -> Iterable[ICryptoKey]:
        raise NotImplementedError

    def __await__(self):
        return self._discover().__await__()