# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
import pytest

import aiopki
from aiopki.ext import jose


class Model(pydantic.BaseModel):
    jwt: jose.CompactSerialized



@pytest.mark.asyncio
async def test_parse_josetype(jwks: jose.JWKS):
    alg = aiopki.algorithms.get('ES256')
    jwk = jwks.get('example')
    jws = jose.jws({'msg': 'Hello world!'})
    await jws.sign(alg, jwk)

    obj = Model.model_validate({'jwt': jws.encode(encoder=bytes.decode)})
    assert isinstance(obj.jwt, jose.JOSEObject)
    assert await obj.jwt.verify(jwk)
    jwt = obj.jwt.payload()
    assert jwt.claims.get('msg') == 'Hello world!'