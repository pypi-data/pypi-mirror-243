# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
from typing import Any
from typing import Iterable

import pydantic

from aiopki.utils import b64encode_json


class BaseJWT(pydantic.BaseModel):
    claims: dict[str, Any] = pydantic.Field(default={}, alias='__claims__')

    @pydantic.model_validator(mode='before')
    def preprocess(cls, values: bytes | str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(values, (bytes, str)):
            values = json.loads(values)
        assert isinstance(values, dict)
        return {
            **values,
            '__claims__': {
                k: v
                for k, v in values.items()
                if k not in cls.model_fields
            }
        }
    
    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_defaults', True)
        kwargs.setdefault('exclude_unset', True)
        exclude = kwargs.setdefault('exclude', set())
        exclude.add('claims')
        return {**self.claims, **super().model_dump(**kwargs)}

    def encode(self, **kwargs: Any) -> bytes:
        """Encode the payload of the JWT."""
        return b64encode_json({
            **self.claims,
            **self.model_dump(**kwargs)
        })
    
    def has_claims(self, claims: Iterable[str]) -> bool:
        """Return a boolean indicating if the token has the given claims."""
        return set(claims) <= set(self.model_dump(exclude_none=True))


class JWT(BaseJWT):
    aud: str | list[str] | None = None
    iss: str | None = None
    exp: int | None = None
    sub: str | None = None

    def model_post_init(self, _: Any) -> None:
        if isinstance(self.aud, list) and len(self.aud) == 1:
            self.aud = self.aud[0]

    @pydantic.field_serializer('aud')
    def serialize_aud(self, _: Any) -> str | list[str] | None:
        aud = self.aud
        if isinstance(self.aud, list) and len(self.aud) == 1: # pragma: no cover
            aud = self.aud[0]
        return aud

    def has_audience(self, value: str) -> bool:
        return self.aud is not None and any([
            isinstance(self.aud, list) and value in self.aud,
            isinstance(self.aud, str) and value == self.aud
        ])