# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

import aiopki
from aiopki.types import IAlgorithm
from aiopki.types import ISigner
from aiopki.types import IVerifier
from aiopki.utils import b64decode_json
from aiopki.utils import b64encode
from .invalidobject import InvalidObject
from .jwsheader import JWSHeader


class Signature(pydantic.BaseModel):
    claims: JWSHeader
    protected: bytes | None = None
    header: dict[str, Any] = {}
    signature: bytes

    @property
    def alg(self) -> IAlgorithm:
        return aiopki.algorithm(self.claims.alg)

    @property
    def kid(self) -> str | None:
        return self.claims.kid

    @classmethod
    async def new(
        cls,
        algorithm: IAlgorithm,
        signer: ISigner,
        payload: bytes,
        protected: JWSHeader | dict[str, Any] | None = None,
        header: dict[str, Any] | None = None,
    ):
        if not isinstance(protected, JWSHeader):
            protected = JWSHeader.model_validate({
                **(protected or {}),
                'alg': algorithm.name,
                'crv': signer.crv,
                'kid': signer.thumbprint
            })
        assert isinstance(protected, JWSHeader), type(protected).__name__
        assert protected.alg == algorithm.name
        message = bytes.join(b'.', [protected.encode(), payload])
        return cls.model_validate({
            'protected': protected.encode(),
            'signature': await signer.sign(message, algorithm),
            'header': header or {}
        })


    @pydantic.field_validator('protected', mode='before')
    def preprocess_protected(cls, value: bytes | str | None) -> bytes | None:
        if isinstance(value, str):
            value = str.encode(value, 'ascii')
        return value
    
    @pydantic.model_validator(mode='before')
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        # The Header Parameter values used when creating or validating
        # individual signature or MAC values are the union of the two
        # sets of Header Parameter values that may be present: (1) the
        # JWS Protected Header represented in the "protected" member of
        # the signature/MAC's array element, and (2) the JWS Unprotected
        # Header in the "header" member of the signature/MAC's array element.
        # The union of these sets of Header Parameters comprises the JOSE
        # Header.  The Header Parameter names in the two locations MUST
        # be disjoint.
        claims = values.get('header') or {}
        protected = {}
        if values.get('protected'):
            protected = b64decode_json(values['protected'])
        if not isinstance(protected, dict):
            raise InvalidObject("The encoded protected header must be a JSON object.")
        if set(claims.keys()) & set(protected.keys()):
            raise InvalidObject(
                "The header parameter names in the protected and "
                "unprotected header must be disjoint."
            )
        values['claims'] = {**claims, **protected}
        return values

    def encode(self, payload: bytes) -> bytes:
        if self.protected is None: # pragma: no cover
            raise ValueError("Missing protected header.")
        return bytes.join(b'.', [
            self.protected,
            payload,
            b64encode(self.signature)
        ])

    async def verify(self, verifier: IVerifier, payload: bytes) -> bool:
        """Return a boolean indicating if the signature
        is valid.
        """
        assert self.protected is not None
        if not verifier.can_use(self.alg):
            return False

        return await verifier.verify(
            self.signature,
            bytes.join(b'.', [self.protected, payload]),
            algorithm=self.alg,
            using=self.kid,
        )