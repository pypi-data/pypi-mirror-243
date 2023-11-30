# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest_asyncio

import aiopki
from aiopki.types import ISigner
from aiopki.ext import jose


@pytest_asyncio.fixture(scope='function') # type: ignore
async def jwt(signer: ISigner) -> str:
    jws = jose.jws({'sub': '123', 'aud': 'test'})
    await jws.sign(aiopki.algorithms.get('ES256'), signer)
    return jws.encode(encoder=bytes.decode)