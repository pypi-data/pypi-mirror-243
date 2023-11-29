# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic

import aiopki
from aiopki.types import EncryptionResult
from aiopki.types import IAlgorithm
from aiopki.types import Plaintext


KeyOp = Literal['sign', 'verify', 'encrypt', 'decrypt', 'wrapKey', 'unWrapKey', 'deriveKey', 'deriveBits']


class BaseJWK(pydantic.BaseModel):
    alg: str | None = None
    crv: str | None = None
    exp: int | None = None
    iat: int | None = None
    key_ops: list[KeyOp] | None = None
    kid: str | None = None
    nbf: int | None = None
    use: Literal['enc', 'sig'] | None = None

    @property
    def thumbprint(self) -> str:
        raise NotImplementedError

    @pydantic.model_validator(mode='before')
    def preprocess(cls, values: dict[str, Any]) -> dict[str, Any]:
        key = values.get('key', None)
        if key is not None:
            try:
                values.update(cls.preprocess_key(key), **values)
            except NotImplementedError:
                pass
        return values

    @classmethod
    def preprocess_key(cls, key: Any, **values: Any) -> dict[str, Any]:
        raise NotImplementedError

    def can_use(self, algorithm: IAlgorithm) -> bool:
        raise NotImplementedError

    def default_algorithm(self) -> IAlgorithm:
        raise NotImplementedError

    def get_algorithm(self) -> IAlgorithm:
        if not self.alg:
            raise NotImplementedError
        return aiopki.algorithms.get(self.alg)

    def get_thumbprint(self) -> str:
        return self.thumbprint

    def is_public(self) -> bool:
        raise NotImplementedError

    async def decrypt(
        self,
        ct: EncryptionResult,
        algorithm: IAlgorithm | None = None
    ) -> Plaintext:
        raise NotImplementedError

    async def encrypt(
        self,
        pt: bytes | Plaintext,
        algorithm: IAlgorithm | None = None
    ) -> EncryptionResult:
        raise NotImplementedError

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm,
    ) -> bytes:
        raise NotImplementedError

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm,
        using: str | None = None
    ) -> bool:
        raise NotImplementedError