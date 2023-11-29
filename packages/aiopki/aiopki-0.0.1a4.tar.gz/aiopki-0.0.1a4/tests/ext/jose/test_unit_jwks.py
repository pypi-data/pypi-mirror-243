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


def test_jwks_public(jwks: jose.JWKS):
    assert all([x.is_public() for x in jwks.public.keys])


@pytest.mark.asyncio
async def test_jwks_verify(jwks: jose.JWKS, jwt: str):
    obj = jose.parse(jwt)
    assert await obj.verify(jwks)


@pytest.mark.asyncio
async def test_empty_jwks_does_not_verify(jwks: jose.JWKS, jwt: str):
    obj = jose.parse(jwt)
    mock = jose.JWKS()
    assert not await obj.verify(mock)


@pytest.mark.asyncio
async def test_unknown_kid_does_not_verify(jwks: jose.JWKS, signer: aiopki.types.ISigner):
    jws = jose.jws(b'Hello world!')
    await jws.sign(aiopki.algorithms.get('ES256'), signer, {'kid': 'foo'})
    assert not await jws.verify(jose.JWKS())


@pytest.mark.asyncio
async def test_known_kid_does_verify(jwks: jose.JWKS, signer: aiopki.types.ISigner):
    jws = jose.jws(b'Hello world!')
    await jws.sign(aiopki.algorithms.get('ES256'), signer, {'kid': 'rfc7515:a3'})
    assert await jws.verify(jwks)