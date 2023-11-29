# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
from jwcrypto import jwk
from jwcrypto import jws

from aiopki.ext import jose
from .const import SUPPORTED_KEYS


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_sign_bytes_compact(jwks: jose.JWKS, kid: str):
    k1 = jwks.get(kid)
    assert k1.alg is not None
    assert k1.kid is not None

    k2 = jwk.JWK(**k1.model_dump(exclude_none=True)) # type: ignore
    j2 = jws.JWS(b'Hello world!')
    j2.add_signature(k2, k1.alg, {'alg': k1.alg, 'kid': k1.kid}) # type: ignore
    j1 = jose.parse(j2.serialize(compact=True))
    assert await j1.verify(k1)


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_sign_bytes_compact_invalid(jwks: jose.JWKS, kid: str):
    """Sign and verify with a different key than that was used to sign."""
    k1 = jwks.get(kid)
    k2 = jwk.JWK(**k1.model_dump(exclude_none=True)) # type: ignore
    assert k1.alg is not None
    assert k1.kid is not None

    j2 = jws.JWS(b'Hello world!')
    j2.add_signature(k2, k1.alg, {'alg': k1.alg, 'kid': k1.kid}) # type: ignore
    j1 = jose.parse(j2.serialize(compact=True))
    assert not await j1.verify(jwks.get('example'))


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_verify_bytes_compact(jwks: jose.JWKS, kid: str):
    k1 = jwks.get(kid)
    k2 = jwk.JWK(**k1.model_dump(exclude_none=True)) # type: ignore
    assert k1.alg is not None
    assert k1.kid is not None
    j1 = jose.jws(b'Hello world!')
    await j1.sign(k1.alg, k1, {'kid': k1.kid})

    j2 = jws.JWS()
    j2.deserialize(bytes.decode(j1.encode())) # type: ignore
    j2.verify(k2) # type: ignore


@pytest.mark.asyncio
@pytest.mark.parametrize("kid", SUPPORTED_KEYS)
async def test_verify_bytes_compact_invalid(jwks: jose.JWKS, kid: str):
    k1 = jwks.get(kid)
    k2 = jwks.get('example')
    assert k1.alg is not None
    assert k1.kid is not None
    j1 = jose.jws(b'Hello world!')
    await j1.sign(k1.alg, k1, {'kid': k1.kid})

    j2 = jws.JWS()
    j2.deserialize(bytes.decode(j1.encode())) # type: ignore
    with pytest.raises(jws.InvalidJWSSignature):
        j2.verify(k2) # type: ignore