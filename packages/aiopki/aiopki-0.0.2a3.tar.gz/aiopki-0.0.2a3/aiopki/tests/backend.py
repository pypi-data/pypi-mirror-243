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
from aiopki.types import IAlgorithm
from aiopki.types import ISigner
from aiopki.types import IVerifier


@pytest.mark.asyncio
async def test_sign(signing_key: ISigner, signing_algorithm: IAlgorithm, verifier: IVerifier):
    message = b'Hello world'
    signature = await signing_key.sign(message, signing_algorithm)
    assert await verifier.verify(signature, b'Hello world', signing_algorithm)


@pytest.mark.asyncio
async def test_verify(signing_key: ISigner, signing_algorithm: IAlgorithm, verifier: IVerifier):
    message = b'Hello world'
    signature = await signing_key.sign(message, signing_algorithm)
    assert not await verifier.verify(signature, b'Hello underworld', signing_algorithm)


@pytest.mark.asyncio
async def test_sign_jws(
    jws: jose.JWS,
    signing_key: ISigner,
    signing_algorithm: IAlgorithm,
    verifier: IVerifier
):
    await jws.sign(signing_algorithm, signing_key)
    assert await jws.verify(verifier)


@pytest.mark.asyncio
async def test_verify_jws(
    jws: jose.JWS,
    untrusted_signer: ISigner, 
    signing_algorithm: IAlgorithm,
    verifier: IVerifier
):
    await jws.sign(signing_algorithm, untrusted_signer)
    assert not await jws.verify(verifier)