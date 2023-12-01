# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cryptography.hazmat.primitives.asymmetric import ec

import aiopki
from aiopki.types import IAlgorithm
from aiopki.utils import b64decode_int
from aiopki.utils import b64encode_int
from aiopki.utils import normalize_ec_signature
from .ellipticcurvepublickey import EllipticCurvePublicKey


class EllipticCurvePrivateKey(EllipticCurvePublicKey):
    d: str
    _private_numbers: ec.EllipticCurvePrivateNumbers

    @property
    def key(self) -> ec.EllipticCurvePrivateKey: # type: ignore
        return self._private_numbers.private_key()

    @property
    def public(self) -> EllipticCurvePublicKey:
        return EllipticCurvePublicKey.model_validate(self.model_dump())

    @classmethod
    def preprocess_key(cls, key: ec.EllipticCurvePrivateKey | Any, **values: Any) -> dict[str, Any]:
        if not isinstance(key, ec.EllipticCurvePrivateKey):
            raise NotImplementedError
        numbers = key.private_numbers()
        return {
            'crv': EllipticCurvePublicKey.curves[key.curve.name],
            'x': b64encode_int(numbers.public_numbers.x),
            'y': b64encode_int(numbers.public_numbers.y),
            'd': b64encode_int(numbers.private_value)
        }

    def get_algorithm(self) -> IAlgorithm:
        if self.alg is None:
            raise NotImplementedError
        return aiopki.algorithms.get(self.alg) 

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        super().model_post_init(*args, **kwargs)
        self._private_numbers = ec.EllipticCurvePrivateNumbers(
            private_value=b64decode_int(self.d),
            public_numbers=self._public_numbers
        )

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm,
    ) -> bytes:
        signature = self.key.sign(
            data=message,
            signature_algorithm=ec.ECDSA(algorithm.get_digest_algorithm())
        )
        return normalize_ec_signature(
            l=(self.public_key.curve.key_size + 7) // 8,
            sig=signature
        )