# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import pathlib
from typing import Any

import pytest
import yaml

import aiopki
from aiopki.ext import jose
from aiopki.ext.jose import JWKS


aiopki.install_backend('aiopki.ext.cryptography')


@pytest.fixture(scope='session')
def jwks_yaml():
    with open(pathlib.Path(__file__).parent.joinpath('jwks.yml'), 'r') as f:
        return yaml.safe_load(f.read())


@pytest.fixture(scope='function')
def jwks(jwks_yaml: dict[str, Any]):
    return JWKS.model_validate(jwks_yaml)


@pytest.fixture
def jws() -> jose.JOSEObject:
    return jose.jws(b'Hello world!')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def signer(jwks: jose.JWKS) -> jose.JWK:
    return jwks.get('rfc7515:a3')


@pytest.fixture
def untrusted_signer(jwks: jose.JWKS) -> jose.JWK:
    return jwks.get('example')