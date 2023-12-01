# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
import hmac
from typing import Any
from typing import Literal

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES

import aiopki
from aiopki.algorithms import HMACSigning
from aiopki.types import EncryptionResult
from aiopki.types import IAlgorithm
from aiopki.types import Plaintext
from aiopki.utils import b64decode
from aiopki.utils import b64encode
from .basejwk import BaseJWK


class OctetPrivateKey(BaseJWK):
    k: str
    kty: Literal['oct']

    @property
    def public(self) -> None:
        return None

    @property
    def thumbprint(self) -> str:
        message = self.model_dump_json(include={'k', 'kty'})
        return b64encode(hashlib.sha256(str.encode(message)).digest(), encoder=bytes.decode)

    def can_use(self, algorithm: IAlgorithm) -> bool:
        return isinstance(algorithm, HMACSigning)

    def default_algorithm(self) -> IAlgorithm:
        assert self.use is not None
        algorithm: IAlgorithm = aiopki.algorithms.get('notimplemented')
        match self.use:
            case 'sig':
                algorithm = aiopki.algorithms.get('HS256')
            case 'enc':
                algorithm = aiopki.algorithms.get('A256GCM')
        return algorithm

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        self._key = b64decode(self.k)
        if not self.key_ops:
            self.key_ops = []
            match self.use:
                case 'sig':
                    self.key_ops.extend([
                        'sign',
                        'verify'
                    ])
                case 'enc':
                    if self.alg in {'dir', None}:
                        self.key_ops.extend([
                            'encrypt',
                            'decrypt'
                        ])
                    if self.alg != 'dir':
                        self.key_ops.extend([
                            'unWrapKey',
                            'wrapKey'
                        ])
                case None:
                    self.key_ops.extend([
                        'sign',
                        'verify',
                        'unWrapKey',
                        'wrapKey'
                    ])


    async def decrypt(
        self,
        ct: EncryptionResult,
        algorithm: IAlgorithm | None = None
    ) -> Plaintext:
        algorithm = algorithm or self.default_algorithm()
        mode, _ = algorithm.get_initialization_vector(ct.root.iv, ct.root.tag)
        cipher = Cipher(AES(self._key), mode)
        decrypter = cipher.decryptor()
        if algorithm.supports_aad():
            decrypter.authenticate_additional_data(ct.aad)
        return Plaintext.model_validate({
            'pt': decrypter.update(bytes(ct)) + decrypter.finalize(),
            'aad': ct.aad
        })

    async def encrypt(
        self,
        pt: bytes | Plaintext,
        algorithm: IAlgorithm | None = None
    ) -> EncryptionResult:
        if isinstance(pt, bytes):
            pt = Plaintext(pt=pt)
        algorithm = algorithm or self.default_algorithm()
        mode, iv = algorithm.get_initialization_vector()
        cipher = Cipher(AES(self._key), mode)
        encrypter = cipher.encryptor()
        if algorithm.supports_aad():
            encrypter.authenticate_additional_data(b'') # type: ignore
        ct = encrypter.update(bytes(pt)) + encrypter.finalize()
        return EncryptionResult.model_validate({
            'aad': b'',
            'alg': algorithm.name,
            'kid': self.kid,
            'ct': ct,
            'iv': iv,
            'tag': encrypter.tag
        })

    async def sign( # type: ignore
        self,
        message: bytes,
        algorithm: HMACSigning,
    ) -> bytes:
        return hmac.digest(self._key, message, algorithm.digestmod)

    async def verify( # type: ignore
        self,
        signature: bytes,
        message: bytes,
        algorithm: HMACSigning,
        using: str | None = None
    ) -> bool:
        h = hmac.new(self._key, message, algorithm.digestmod)
        return hmac.compare_digest(h.digest(), signature)