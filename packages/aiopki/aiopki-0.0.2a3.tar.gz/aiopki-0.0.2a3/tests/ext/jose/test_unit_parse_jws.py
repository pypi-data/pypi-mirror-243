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

from aiopki.ext import jose

A1 = (
    'eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJl'
    'eHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0c'
    'nVlfQ.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'
)

A2 = (
    'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAs'
    'DQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ.cC4hiUPoj9Eetd'
    'gtv3hF80EGrhuB__dzERat0XF9g2VtQgr9PJbu3XOiZj5RZmh7AAuHIm4Bh-0Qc_l'
    'F5YKt_O8W2Fp5jujGbds9uJdbF9CUAr7t1dnZcAcQjbKBYNX4BAynRFdiuB--f_nZ'
    'LgrnbyTyWzO75vRK5h6xBArLIARNPvkSjtQBMHlb1L07Qe7K0GarZRmB_eSN9383L'
    'cOLn6_dO--xi12jzDwusC-eOkHWEsqtFZESc6BfI7noOPqvhJ1phCnvWh6IeYI2w9'
    'QOYEUipUTI8np6LbgGY9Fs98rqVt5AXLIhWkWywlVmtVrBp0igcN_IoypGlUPQGe7'
    '7Rw'
)


@pytest.mark.asyncio
@pytest.mark.parametrize("value,kid", [
    (A1, 'rfc7515:a1'),
    (A2, 'rfc7515:a2')
])
async def test_parse_rfc(value: str, kid: str, jwks: jose.JWKS):
    jws = jose.parse(value)
    assert await jws.verify(jwks.get(kid))


def test_parse_bytes():
    jose.parse(str.encode(A1))


@pytest.mark.parametrize("value", [
    "foo",
    "foo.bar.baz",
    "foo..baz",
    "foo.bar.",
    ".bar.baz",
    "...",
])
def test_parse_invalid(value: str):
    with pytest.raises(pydantic.ValidationError):
        jose.parse(value)