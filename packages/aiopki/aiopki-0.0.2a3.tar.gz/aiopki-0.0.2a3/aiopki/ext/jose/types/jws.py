# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from aiopki.types import IAlgorithm
from aiopki.types import ISigner
from aiopki.types import IVerifier
from .signature import Signature


class JWS(pydantic.BaseModel):
    payload: bytes
    signatures: list[Signature] = []
    claims: dict[str, Any] = {}

    def encode(self, compact: bool = True) -> bytes:
        """Encodes the JWS/JWE."""
        if len(self.signatures) > 1: # pragma: no cover
            raise ValueError("Compact encoding can not be used with multiple signatures.")
        return self.encode_compact()

    def encode_compact(self) -> bytes:
        assert len(self.signatures) == 1
        return self.signatures[0].encode(self.payload)

    async def sign(
        self,
        algorithm: IAlgorithm,
        signer: ISigner,
        protected: dict[str, Any] | None = None,
        header: dict[str, Any] | None = None
    ) -> Signature:
        sig = await Signature.new(algorithm, signer, self.payload, protected=protected, header=header)
        self.signatures.append(sig)
        return sig

    async def verify(self, verifier: IVerifier) -> bool:
        """Return a boolean indicating if at least one signature
        validated using the given verifier.
        """
        for signature in self.signatures:
            is_valid = await signature.verify(verifier, self.payload)
            if not is_valid:
                continue
            break
        else:
            is_valid = False
        return is_valid