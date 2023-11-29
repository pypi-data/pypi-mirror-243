# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any

from aiopki import BaseCryptoKey
from aiopki import CryptoKeySpecification
from aiopki.ext.jose import JWKS
from aiopki.types import IAlgorithm
from aiopki.types import ICryptoKey


__all__: list[str] = [
    'Keychain'
]


class Keychain(BaseCryptoKey):
    keys: list[CryptoKeySpecification] = []
    _default: str | None = None
    _discovered: bool = False
    _index: dict[str, ICryptoKey] = {}
    _trust: dict[str, ICryptoKey] = {}

    def as_jwks(self) -> JWKS:
        keys: list[dict[str, Any]] = []
        for kid, obj in self._trust.items():
            keys.append({**obj.public.model_dump(), 'kid': kid})
        return JWKS.model_validate({'keys': keys})

    def model_post_init(self, _: Any) -> None:
        self._index = {}
        self._trust = {}

    def default(self) -> ICryptoKey:
        assert self._default
        return self._index[self._default]

    def get(self, using: str) -> ICryptoKey:
        return self._index[using]

    async def discover(self):
        if not self._discovered:
            await asyncio.gather(*map(CryptoKeySpecification.discover, self.keys))
            for key in self.keys:
                self._index[key.name] = await key
                if self._default is not None and key.default:
                    raise ValueError("Multiple default keys defined.")
                if key.default:
                    self._default = key.name
                for version in self._index[key.name].versions():
                    if not version.is_available():
                        continue
                    self._trust[version.get_thumbprint()] = version
        if self._default is None:
            self._default = self.keys[0].name
        self._discovered = True
        return self

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bool:
        if using not in self._trust:
            return False
        return await self._trust[using].verify(signature, message, algorithm)