# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any

import pytest
import pytest_asyncio

import aiopki
from aiopki.types import IAlgorithm
from aiopki.ext import azure


@pytest.fixture(scope='session')
def key_uri() -> urllib.parse.ParseResult:
    return urllib.parse.urlparse('https://python-oauthx.vault.azure.net/keys/ES256')


@pytest.fixture(scope='session')
def key_version_uri() -> urllib.parse.ParseResult:
    return urllib.parse.urlparse('https://python-oauthx.vault.azure.net/keys/ES256/2c19c50887fe49c7ae98acdd2022ab76')


@pytest.fixture(scope='session')
def vault_url() -> str:
    return 'https://python-oauthx.vault.azure.net/'


@pytest.fixture
def signing_algorithm() -> IAlgorithm:
    return aiopki.algorithms.get('ES256')


@pytest_asyncio.fixture(scope='session') # type: ignore
async def signing_key(key_uri: urllib.parse.ParseResult):
    k =  await azure.parse_uri(key_uri)
    assert k.default == '03510ac0fa574ab0aa539e82d41ee156'
    return k


@pytest_asyncio.fixture(scope='session') # type: ignore
async def verifier(signing_key: Any):
    return signing_key