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
from aiopki.ext import jose
from .const import SUPPORTED_KEYS


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_sign(jwks: jose.JWKS, kid: str):
    jwk = jwks.get(kid)
    assert jwk.alg is not None
    alg = aiopki.algorithms.get(jwk.alg)
    sig = await jwk.sign(b'Hello world!', alg)
    assert await jwk.verify(sig, b'Hello world!', alg)


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_signed_with_different_key(jwks: jose.JWKS, kid: str):
    k = jwks.get('example')

    assert k.alg is not None
    jws = jose.jws({'kid': k.kid})
    await jws.sign(k.alg, k) # type: ignore
    assert not await jws.verify(jwks.get(kid))