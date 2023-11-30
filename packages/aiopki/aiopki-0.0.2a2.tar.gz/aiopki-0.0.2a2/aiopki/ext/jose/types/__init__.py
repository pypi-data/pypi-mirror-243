# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .jwa import JWA
from .jwe import JWE
from .jwk import JWK
from .jwks import JWKS
from .jws import JWS
from .jwsheader import JWSHeader
from .jwt import BaseJWT
from .jwt import JWT
from .oidctoken import OIDCToken


__all__: list[str] = [
    'BaseJWT',
    'InvalidObject',
    'JWA',
    'JWE',
    'JWK',
    'JWKS',
    'JWS',
    'JWSHeader',
    'JWT',
    'OIDCToken',
]


class InvalidObject(TypeError):
    pass