# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from aiopki.ext import jose
from .const import SUPPORTED_KEYS


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_sign_bytes(jwks: jose.JWKS, kid: str):
    k = jwks.get(kid)
    assert k.alg is not None
    t = await jose.sign(k, k.alg, b'Hello world!')
    o = jose.parse(t)
    p = o.payload(factory=bytes)
    assert await o.verify(k)
    assert p == b'Hello world!'


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_sign_claims(jwks: jose.JWKS, kid: str):
    k = jwks.get(kid)
    assert k.alg is not None
    t = await jose.sign(k, k.alg, {'sub': 'username'})
    o = jose.parse(t)
    p = o.payload(factory=jose.JWT.model_validate)
    assert await o.verify(k)
    assert p.sub == 'username'