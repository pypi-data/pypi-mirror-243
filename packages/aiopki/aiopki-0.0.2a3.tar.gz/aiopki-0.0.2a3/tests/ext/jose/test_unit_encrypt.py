# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

import aiopki
from aiopki.ext.jose import JWKS
from .const import ENCRYPTION_KEYS


PLAINTEXT: bytes = b'Hello world!'


@pytest.mark.parametrize("kid,alg", ENCRYPTION_KEYS)
@pytest.mark.asyncio
async def test_jwk_encrypt_decrypt(jwks: JWKS, kid: str, alg: str):
    k = jwks.get(kid)
    a = aiopki.algorithms.get(alg)
    ct = await k.encrypt(PLAINTEXT, a)
    pt = await k.decrypt(ct, a)
    assert bytes(pt) == PLAINTEXT


@pytest.mark.parametrize("kid,alg", ENCRYPTION_KEYS)
@pytest.mark.asyncio
async def test_jwks_encrypt_decrypt(jwks: JWKS, kid: str, alg: str):
    a = aiopki.algorithms.get(alg)
    ct = await jwks.encrypt(PLAINTEXT, a)
    pt = await jwks.decrypt(ct, a)
    assert bytes(pt) == PLAINTEXT