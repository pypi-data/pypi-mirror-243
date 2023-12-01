# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
from typing import Any
from typing import Literal
from typing import TypeAlias
from typing import Union

import pydantic
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric import ed448

from aiopki.algorithms import EdwardsCurveDigitalSigning
from aiopki.types import IAlgorithm
from aiopki.utils import b64decode
from aiopki.utils import b64encode
from .basejwk import BaseJWK



PublicKeyType: TypeAlias = Union[
    ed448.Ed448PublicKey,
    ed25519.Ed25519PublicKey,
]


class EdwardsCurvePublicKey(BaseJWK):
    kty: Literal['OKP']
    alg: Literal['EdDSA'] = 'EdDSA' # type: ignore
    crv: Literal['Ed448', 'Ed25519'] # type: ignore
    x: str
    _public: PublicKeyType

    @property
    def public(self): # pragma: no cover
        return self

    @property
    def public_key(self) -> PublicKeyType: # pragma: no cover
        return self._public

    @property
    def thumbprint(self) -> str:
        message = self.public.model_dump_json(include={'crv', 'kty', 'x'})
        return b64encode(hashlib.sha256(str.encode(message)).digest(), encoder=bytes.decode)

    @pydantic.model_validator(mode='before')
    def preprocess_curve(cls, values: dict[str, Any]) -> dict[str, Any]:
        crv = values.get('crv')
        if crv in {'Ed448', 'Ed25519'}:
            values.update({'kty': 'OKP', 'alg': 'EdDSA', 'use': 'sig'})
        return values

    def can_use(self, algorithm: IAlgorithm) -> bool:
        return isinstance(algorithm, EdwardsCurveDigitalSigning)

    def get_algorithm(self) -> IAlgorithm:
        return EdwardsCurveDigitalSigning(self.alg)

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        self.key_ops = ['verify']
        match self.crv:
            case 'Ed448':
                cls = ed448.Ed448PublicKey
            case 'Ed25519':
                cls = ed25519.Ed25519PublicKey
            case _: # type: ignore pragma: no cover
                raise NotImplementedError
        self._public = cls.from_public_bytes(b64decode(self.x))

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm,
        using: str | None = None
    ) -> bool:
        if not self.can_use(algorithm):
            raise NotImplementedError(
                f"{type(self).__name__} does not support signature verification "
                f"using the {algorithm.name} algorithm."
            )
        try:
            self._public.verify(signature, message)
            return True
        except InvalidSignature:
            return False