# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import aiopki
from aiopki.algorithms import AESEncryption
from aiopki.algorithms import EdwardsCurveDigitalSigning
from aiopki.algorithms import EllipticCurveSigning
from aiopki.algorithms import HMACSigning
from aiopki.algorithms import RSASigning
from aiopki.types import ISigner
from aiopki.utils import b64encode
from .compactserialized import CompactSerialized
from .joseobject import JOSEObject
from .parser import parse
from .types import *


__all__: list[str] = [
    'parse',
    'sign',
    'InvalidObject',
    'JOSEObject',
    'CompactSerialized',
    'JWK',
    'JWKS',
]


def jwk(params: dict[str, Any]) -> JWK:
    return JWK.model_validate(params)


def jws(payload: dict[str, Any] | bytes, claims: dict[str, Any] | None = None) -> JOSEObject:
    claims = claims or {}
    if isinstance(payload, bytes):
        payload = b64encode(payload)
    if isinstance(payload, dict):
        claims.setdefault('typ', 'JWT')
        payload = JWT.model_validate(payload).encode()
    return JOSEObject.model_validate({
        'claims': claims,
        'payload': payload,
        'signatures': [],
    })


async def sign(
    key: ISigner,
    alg: str,
    payload: dict[str, Any] | bytes,
    protected: dict[str, Any] | None = None,
    header: dict[str, Any] | None = None,
) -> str:
    """Create a JSON Web Signature (JWS) with a JWT Claims Set or
    an unstructured payload. Return a string holding the JWS in the
    compact serialization.
    """
    obj = jws(payload, protected)
    await obj.sign(alg, key)
    return bytes.decode(obj.encode())


aiopki.register('HS256', HMACSigning('sha256'))
aiopki.register('HS384', HMACSigning('sha384'))
aiopki.register('HS512', HMACSigning('sha512'))
aiopki.register('RS256', RSASigning('sha256', 'RSASSA-PKCS1-v1_5'))
aiopki.register('ES256', EllipticCurveSigning('P-256', 'sha256'))
aiopki.register('ES384', EllipticCurveSigning('P-384', 'sha384'))
aiopki.register('ES512', EllipticCurveSigning('P-521', 'sha512'))
aiopki.register('ES256K', EllipticCurveSigning('P-256K', 'sha256'))
aiopki.register('EdDSA', EdwardsCurveDigitalSigning())

aiopki.register('A128GCM', AESEncryption(mode='GCM'))
aiopki.register('A192GCM', AESEncryption(mode='GCM'))
aiopki.register('A256GCM', AESEncryption(mode='GCM'))