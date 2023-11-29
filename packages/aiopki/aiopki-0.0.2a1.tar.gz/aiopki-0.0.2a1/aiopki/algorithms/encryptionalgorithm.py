# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from ..types import IAlgorithm


class EncryptionAlgorithm(IAlgorithm):
    __module__: str = 'aiopki.algorithms'
    name: str

    def get_digest_algorithm(self) -> Any:
        raise NotImplementedError

    def get_padding(self) -> Any:
        raise NotImplementedError