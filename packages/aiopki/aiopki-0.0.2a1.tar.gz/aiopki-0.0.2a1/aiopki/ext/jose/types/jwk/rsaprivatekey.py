# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

from aiopki.types import IAlgorithm
from aiopki.utils import b64decode_int
from aiopki.utils import b64encode_int
from .rsapublickey import RSAPublicKey


class RSAPrivateKey(RSAPublicKey):
    d: str
    p: str
    q: str
    dp: str
    dq: str
    qi: str
    _private_numbers: rsa.RSAPrivateNumbers

    @property
    def public(self) -> RSAPublicKey:
        return RSAPublicKey.model_validate(self.model_dump())

    @classmethod
    def preprocess_key(cls, key: rsa.RSAPrivateKey | Any, **values: Any) -> dict[str, Any]:
        if not isinstance(key, rsa.RSAPrivateKey):
            raise NotImplementedError
        numbers = key.private_numbers()
        return {
            'n': b64encode_int(numbers.public_numbers.n),
            'e': b64encode_int(numbers.public_numbers.e),
            'd': b64encode_int(numbers.d),
            'p': b64encode_int(numbers.p),
            'q': b64encode_int(numbers.q),
            'dp': b64encode_int(numbers.dmp1),
            'dq': b64encode_int(numbers.dmq1),
            'qi': b64encode_int(numbers.iqmp),
        }

    def is_public(self) -> bool:
        return False

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        super().model_post_init(*args, **kwargs)
        self._private_numbers = rsa.RSAPrivateNumbers(
            public_numbers=self._public_numbers,
            d=b64decode_int(self.d),
            p=b64decode_int(self.p),
            q=b64decode_int(self.q),
            dmp1=b64decode_int(self.dp),
            dmq1=b64decode_int(self.dq),
            iqmp=b64decode_int(self.qi)
        )

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm
    ) -> bytes:
        private = self._private_numbers.private_key()
        return private.sign(
            data=algorithm.digest(message),
            padding=algorithm.get_padding(),
            algorithm=Prehashed(algorithm.get_digest_algorithm())
        )
