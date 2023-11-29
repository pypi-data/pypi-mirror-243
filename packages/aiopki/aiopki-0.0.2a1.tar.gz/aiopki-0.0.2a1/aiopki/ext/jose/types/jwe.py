# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from aiopki.types import IVerifier


class JWE(pydantic.BaseModel):
    ciphertext: bytes
    iv: bytes
    payload: str | None = None

    def encode(self) -> bytes:
        """Encodes the JWS/JWE."""
        raise NotImplementedError

    async def verify(self, verifier: IVerifier) -> bool:
        raise TypeError("JWE does not have a signature.")