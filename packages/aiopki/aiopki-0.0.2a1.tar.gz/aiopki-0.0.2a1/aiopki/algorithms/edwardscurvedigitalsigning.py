# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cryptography.hazmat.primitives.asymmetric.padding import PSS, PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256, SHA384, SHA512
from ..types import IAlgorithm


class EdwardsCurveDigitalSigning(IAlgorithm):
    __module__: str = 'aiopki.algorithms'
    name: str
    curve: str | None

    def __init__(self, curve: str | None = None) -> None:
        self.curve = curve

    def get_digest_algorithm(self) -> SHA256 | SHA384 | SHA512:
        raise NotImplementedError

    def get_padding(self) -> PKCS1v15 | PSS:
        raise NotImplementedError