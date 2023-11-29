# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import urllib.parse
from typing import Iterable

import aiofiles
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import aiopki
from aiopki import BaseCryptoKey
from aiopki.types import IAlgorithm
from aiopki.types import ICryptoKey
from aiopki.ext.jose import JWK
from .cryptokeyparameters import CryptoKeyParameters


class CryptoKey(BaseCryptoKey):
    params: CryptoKeyParameters
    filename: str
    _public: JWK | None = None

    @property
    def crv(self) -> str | None:
        return self.params.crv

    @property
    def public(self) -> JWK | None:
        return self._public

    @classmethod
    def parse_uri(cls, uri: urllib.parse.ParseResult) -> 'CryptoKey':
        if uri.scheme != 'file': # pragma: no cover
            raise ValueError(f"Invalid URI: {uri}")
        return cls.model_validate({
            'params': dict(urllib.parse.parse_qsl(uri.query)),
            'filename': os.path.abspath(uri.path[1:]),
        })
    
    def can_use(self, algorithm: IAlgorithm) -> bool:
        return algorithm.name == self.params.alg

    def default_algorithm(self) -> IAlgorithm:
        if not self.params.alg:
            raise ValueError("CryptoKey does not specify a default algorithm.")
        return aiopki.algorithms.get(self.params.alg)

    def get_thumbprint(self) -> str:
        assert self.public is not None
        return self.public.thumbprint

    def is_available(self) -> bool:
        return True

    def versions(self) -> Iterable[ICryptoKey]:
        return [self]

    async def load(self) -> JWK:
        async with aiofiles.open(self.filename, 'rb') as f:
            if self.params.kty in {'EC', 'OKP', 'RSA'}:
                key = load_pem_private_key(await f.read(), None)
            else:
                raise NotImplementedError
            jwk = JWK.model_validate({'key': key, **self.params.model_dump()})
            self._public = jwk.public
        return jwk

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bytes:
        jwk = await self.load()
        return await jwk.sign(message, algorithm, using)

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bool:
        jwk = await self.load()
        return await jwk.verify(signature, message, algorithm, using)
    
    def __await__(self):
        async def f():
            jwk = await self.load()
            self._public = jwk.public
            return self
        return f().__await__()