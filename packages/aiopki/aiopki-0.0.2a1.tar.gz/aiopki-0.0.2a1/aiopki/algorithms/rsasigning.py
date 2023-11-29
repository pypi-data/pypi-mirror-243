# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cryptography.hazmat.primitives.asymmetric.padding import PSS, PKCS1v15
from ..types import IAlgorithm

from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hashes import SHA384
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15


DIGEST_ALGORITHMS: dict[str, type[SHA256|SHA384|SHA512]] = {
    'sha256': SHA256,
    'sha384': SHA384,
    'sha512': SHA512,
}

PADDING_ALGORITHMS: dict[str, type[PKCS1v15|PSS]] = {
    'RSASSA-PKCS1-v1_5': PKCS1v15
}


class RSASigning(IAlgorithm):
    __module__: str = 'aiopki.algorithms'
    name: str

    def __init__(self, digalg: str, padding: str):
        self._digalg = DIGEST_ALGORITHMS[digalg]
        self._padding = PADDING_ALGORITHMS[padding]

    def digest(self, value: bytes) -> bytes:
        h = Hash(self._digalg())
        h.update(value)
        return h.finalize()

    def get_digest_algorithm(self) -> SHA256 | SHA384 | SHA512:
        return self._digalg()
    
    def get_padding(self) -> PKCS1v15 | PSS:
        params = {}
        if self._padding == PSS:
            raise NotImplementedError
        return self._padding(**params) # type: ignore