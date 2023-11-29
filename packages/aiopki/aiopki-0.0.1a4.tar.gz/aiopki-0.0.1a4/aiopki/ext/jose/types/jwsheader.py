# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from aiopki.utils import b64encode
from .jwa import JWA
from .jwk import JWK


class JWSHeader(pydantic.BaseModel):
    alg: JWA
    crv: str | None = None
    cty: str | None = None
    crit: list[str] = []
    jku: str | None = None
    jwk: JWK | None = None
    kid: str | None = None
    typ: str | None = None
    x5c: str | None = None
    x5t: str | None = None
    x5t_sha256: str | None = pydantic.Field(default=None, alias='x5t#S256')
    x5u: str | None = None
    _extra: dict[str, Any]

    @pydantic.model_validator(mode='before')
    def preprocess(cls, values: dict[str, Any]) -> dict[str, Any]:
        return values

    def encode(self, **kwargs: Any) -> bytes:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_defaults', True)
        kwargs.setdefault('exclude_unset', True)
        return b64encode(self.model_dump_json(**kwargs))