# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Literal

import pydantic

import aiopki
from aiopki.ext import jose
from aiopki.types import IAlgorithm


class CryptoKeyVersion(aiopki.BaseCryptoKey):
    exp: int | None = None
    iat: int
    kty: Literal['oct', 'EC', 'RSA']
    name: str
    nbf: int | None = None
    jwk: jose.JWK
    uri: str

    @pydantic.field_validator('kty', mode='before')
    def preprocess_kty(cls, value: str) -> str:
        if value in {'EC-HSM', 'RSA-HSM'}:
            value = str.split(value, '-')[0]
        return value

    @pydantic.field_validator('exp', mode='before')
    def preprocess_exp(cls, value: int | datetime.datetime | None) -> int | None:
        if isinstance(value, datetime.datetime):
            value = int(value.timestamp())
        return value

    @pydantic.field_validator('iat', mode='before')
    def preprocess_iat(cls, value: int | datetime.datetime) -> int:
        if isinstance(value, datetime.datetime):
            value = int(value.timestamp())
        return value

    @pydantic.field_validator('nbf', mode='before')
    def preprocess_nbf(cls, value: int | datetime.datetime | None) -> int | None:
        if isinstance(value, datetime.datetime):
            value = int(value.timestamp())
        return value

    @property
    def alg(self) -> str:
        assert self.jwk.alg is not None
        return self.jwk.alg

    @property
    def public(self) -> jose.JWK | None:
        return self.jwk

    def default_algorithm(self) -> IAlgorithm:
        return aiopki.algorithms.get(self.alg)

    def is_available(self) -> bool:
        return self.jwk.is_available()

    def get_thumbprint(self) -> str:
        return self.jwk.thumbprint