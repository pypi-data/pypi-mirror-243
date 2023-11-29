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
from aiopki import backends


SUPPORTED_URIS: list[str] = [
    "file:///pki/sig.key?kty=OKP&alg=EdDSA&crv=Ed448",
    #"file:///pki/rsa.key?kty=RSA",
    "file:///pki/secp256k1.key?crv=P-256K",
    "file:///pki/secp384r1.key?crv=P-384",
    "file:///pki/secp521r1.key?crv=P-512",
]


class Model(pydantic.BaseModel):
    key: aiopki.CryptoKeyURI


@pytest.mark.asyncio
@pytest.mark.parametrize("uri", SUPPORTED_URIS)
async def test_parse_uri_signing_alg(uri: str):
    k = backends.parse_uri(uri)
    sig = await k.sign(b'Hello world')
    assert await k.verify(sig, b'Hello world')


@pytest.mark.parametrize("uri", SUPPORTED_URIS)
@pytest.mark.asyncio
async def test_parse_uri_on_pydantic_model(uri: str):
    obj = Model.model_validate({
        'key': uri
    })
    key = await obj.key
    sig = await key.sign(b'Hello world!')
    assert await key.verify(sig, b'Hello world!')