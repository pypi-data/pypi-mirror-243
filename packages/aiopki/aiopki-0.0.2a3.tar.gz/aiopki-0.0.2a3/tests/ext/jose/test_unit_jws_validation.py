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
from aiopki.utils import b64encode_json
from aiopki.types import ISigner


def test_protected_header_must_be_a_dict():
    encoded = bytes.join(b'.', [
        b64encode_json([]),
        b'',
        b''
    ])
    with pytest.raises(ValueError):
        jose.parse(encoded)


@pytest.mark.asyncio
async def test_header_claims_must_be_disjoint(
    signer: ISigner
):
    jws = jose.jws(b'Hello world!', claims=None)
    with pytest.raises(ValueError):
        await jws.sign(aiopki.algorithms.get('ES256'), signer, {'typ': 'foo'}, {'typ': 'foo'})