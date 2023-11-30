# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json

import pytest

from aiopki.ext import jose



def test_parse_jwt(jwt: str):
    obj = jose.parse(jwt)
    assert isinstance(obj.payload(), jose.JWT)


@pytest.mark.parametrize("aud", [
    ['foo'],
    'foo',
])
def test_single_audience_is_string(aud :str):
    jwt = jose.JWT(aud=aud)
    assert isinstance(jwt.aud, str)
    assert jwt.aud == 'foo'


@pytest.mark.parametrize("aud", [
    ['foo'],
    'foo',
])
def test_single_audience_serializes_to_string(aud :str):
    jwt = jose.JWT(aud=aud)
    obj = json.loads(jwt.model_dump_json())
    assert isinstance(obj.get('aud'), str)
    assert obj.get('aud') == 'foo'


def test_has_aud():
    jwt = jose.JWT(aud='foo')
    assert jwt.has_audience('foo')


def test_has_claims():
    jwt = jose.JWT(aud='foo')
    assert jwt.has_claims({'aud'})