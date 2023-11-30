# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import TypeVar

import pydantic

import aiopki
from aiopki.types import IAlgorithm
from aiopki.types import ISigner
from aiopki.types import IVerifier
from aiopki.utils import b64decode
from .types import JWE
from .types import JWS
from .types import JWT


T = TypeVar('T')


class JOSEObject(pydantic.RootModel[JWS | JWE]):

    @staticmethod
    def deserialize(value: str | bytes) -> dict[str, Any]:
        if isinstance(value, bytes):
            value = bytes.decode(value, 'ascii')
        params: dict[str, Any] = {}
        if value.count('.') == 2:
            protected, payload, signature = str.split(value, '.')
            params.update({
                'payload': payload,
                'signatures': [{
                    'protected': protected,
                    'signature': b64decode(signature)
                }]
            })
        if value.count('.') == 4:
            protected, key, iv, ct, aad = str.split(value, '.')
            params.update({
                'protected': protected,
                'iv': iv,
                'aad': aad,
                'ciphertext': ct,
                'recipients': [{'encrypted_key': key}]
            })
        return params

    @classmethod
    def parse_compact(cls, value: str | bytes):
        return cls.model_validate(cls.deserialize(value))

    @pydantic.model_validator(mode='before')
    def preprocess(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = cls.deserialize(value)
        return value

    def payload(
        self,
        factory: Callable[[bytes], T] = JWT.model_validate
    ) -> T:
        obj = self.root
        if isinstance(obj, JWE):
            raise NotImplementedError
        assert obj.payload is not None
        return factory(b64decode(obj.payload))

    def encode(self, encoder: Callable[[bytes], T] = bytes) -> T:
        """Encodes the JWS/JWE."""
        return encoder(self.root.encode())

    async def sign(
        self,
        algorithm: str | IAlgorithm,
        signer: ISigner,
        protected: dict[str, Any] | None = None,
        header: dict[str, Any] | None = None
    ) -> None:
        """Add a signature to a JWS object."""
        if not isinstance(self.root, JWS):
            raise NotImplementedError
        if isinstance(algorithm, str):
            algorithm = aiopki.algorithm(algorithm)
        await self.root.sign(algorithm, signer, protected or {}, header or {})

    async def verify(self, verifier: IVerifier) -> bool:
        """Return a boolean indicating if at least one signature
        validated using the given verifier. Raise an exception if
        the object does not have signatures (i.e. is JWE).
        """
        return await self.root.verify(verifier)