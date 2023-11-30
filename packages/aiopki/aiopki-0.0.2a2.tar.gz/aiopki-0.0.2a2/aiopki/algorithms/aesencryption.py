# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Literal

from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers.modes import GCM

from .encryptionalgorithm import EncryptionAlgorithm


class AESEncryption(EncryptionAlgorithm):
    __module__: str = 'oauthx.algorithms'
    iv_length: int = 12
    _modes: dict[str, type[CBC | GCM]] = {
        'CBC': CBC,
        'GCM': GCM
    }

    def __init__(self, mode: Literal['CBC', 'GCM']) -> None:
        self._mode = mode

    def get_initialization_vector(self, iv: bytes | None = None, tag: bytes | None = None) -> tuple[GCM, bytes]:
        Mode = self._modes[self._mode]
        iv = iv or os.urandom(self.iv_length)
        
        assert Mode == GCM
        return Mode(iv, tag=tag), iv # type: ignore

    def supports_aad(self) -> bool:
        return self._mode == 'GCM'