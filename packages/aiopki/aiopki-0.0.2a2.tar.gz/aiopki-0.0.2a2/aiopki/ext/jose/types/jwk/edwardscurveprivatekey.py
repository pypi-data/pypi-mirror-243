# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Union

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric import ed448

from aiopki.utils import b64decode
from aiopki.utils import b64encode
from aiopki.types import IAlgorithm
from .edwardscurvepublickey import EdwardsCurvePublicKey


PrivateKeyClass: tuple[type, ...] = (
    ed448.Ed448PrivateKey,
    ed25519.Ed25519PrivateKey
)

PrivateKeyType = Union[
    ed448.Ed448PrivateKey,
    ed25519.Ed25519PrivateKey
]


class EdwardsCurvePrivateKey(EdwardsCurvePublicKey):
    d: str

    @property
    def public(self): # pragma: no cover
        return EdwardsCurvePublicKey.model_validate(self.model_dump())

    @classmethod
    def preprocess_key(cls, key: PrivateKeyType, **values: Any) -> dict[str, Any]:
        if not isinstance(key, PrivateKeyClass):
            raise NotImplementedError
        public = key.public_key()
        return {
            'x': b64encode(public.public_bytes_raw()),
            'd': b64encode(key.private_bytes_raw())
        }
        

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        super().model_post_init(*args, **kwargs)
        self.key_ops = ['sign', 'verify']
        match self.crv:
            case 'Ed448':
                cls = ed448.Ed448PrivateKey
            case 'Ed25519':
                cls = ed25519.Ed25519PrivateKey
            case _: # type: ignore pragma: no cover
                raise NotImplementedError
        self._private = cls.from_private_bytes(b64decode(self.d))

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm
    ) -> bytes:
        if not self.can_use(algorithm):
            raise NotImplementedError(
                f"{type(self).__name__} does not support signing "
                f"using the {algorithm.name} algorithm."
            )
        return self._private.sign(message)