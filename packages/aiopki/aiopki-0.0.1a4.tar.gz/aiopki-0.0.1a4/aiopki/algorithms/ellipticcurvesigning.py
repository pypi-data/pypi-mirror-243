# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric.padding import PSS
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hashes import SHA384
from cryptography.hazmat.primitives.hashes import SHA512

from ..types import IAlgorithm
from .rsasigning import DIGEST_ALGORITHMS


class EllipticCurveSigning(IAlgorithm):
    __module__: str = 'aiopki.algorithms'
    name: str

    @property
    def curve(self) -> str:
        return self._curve

    def __init__(self, curve: str, digestmod: str):
        self._curve = curve
        self._algorithm = DIGEST_ALGORITHMS[digestmod]

    def digest(self, value: bytes) -> bytes:
        h = Hash(self._algorithm())
        h.update(value)
        return h.finalize()

    def get_digest_algorithm(self) -> SHA256 | SHA384 | SHA512:
        return self._algorithm()
    
    def get_padding(self) -> PKCS1v15 | PSS:
        raise NotImplementedError