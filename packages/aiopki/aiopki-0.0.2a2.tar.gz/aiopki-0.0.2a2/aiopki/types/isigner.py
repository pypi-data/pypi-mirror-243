# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from .ialgorithm import IAlgorithm


class ISigner(Protocol):
    __module__: str = 'aiopki.types'

    @property
    def thumbprint(self) -> str:
        ...

    def default_algorithm(self) -> IAlgorithm: ...
    async def sign(self, message: bytes, algorithm: IAlgorithm | None = None, using: str | None = None) -> bytes: ...