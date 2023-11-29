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

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

import aiopki
from aiopki.algorithms import RSASigning
from aiopki.types import IAlgorithm
from aiopki.utils import b64decode_int
from aiopki.utils import b64encode
from .basejwk import BaseJWK


class RSAPublicKey(BaseJWK):
    kty: Literal['RSA']
    n: str
    e: str
    _public_numbers: RSAPublicNumbers

    @property
    def public(self): # pragma: no cover
        return self

    @property
    def thumbprint(self) -> str:
        message = self.public.model_dump_json(include={'e', 'kty', 'n'})
        return b64encode(hashlib.sha256(str.encode(message)).digest(), encoder=bytes.decode)

    def can_use(self, algorithm: IAlgorithm) -> bool:
        return isinstance(algorithm, RSASigning)

    def default_algorithm(self) -> IAlgorithm:
        assert self.use is not None
        algorithm: IAlgorithm = aiopki.algorithms.get('notimplemented')
        match self.use:
            case 'sig':
                algorithm = aiopki.algorithms.get('RS256')
            case 'enc':
                algorithm = aiopki.algorithms.get('RSA-OAEP-256')
        return algorithm

    def is_public(self) -> bool:
        return True

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        self._public_numbers = RSAPublicNumbers(
            e=b64decode_int(self.e),
            n=b64decode_int(self.n)
        )
        if not self.key_ops:
            self.key_ops = []
            match self.use:
                case 'sig':
                    self.key_ops.append('verify')
                    if not self.is_public():
                        self.key_ops.append('sign')
                case 'enc':
                    self.key_ops.append('wrapKey')
                    if not self.is_public():
                        self.key_ops.append('unWrapKey')
                case None:
                    self.key_ops.extend([
                        'verify',
                        'wrapKey',
                    ])
                    if not self.is_public():
                        self.key_ops.extend([
                            'sign',
                            'unWrapKey'
                        ])

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm,
        using: str | None = None
    ) -> bool:
        public = self._public_numbers.public_key()
        try:
            public.verify(
                signature,
                message,
                padding=algorithm.get_padding(),
                algorithm=algorithm.get_digest_algorithm()
            )
            return True
        except InvalidSignature:
            return False