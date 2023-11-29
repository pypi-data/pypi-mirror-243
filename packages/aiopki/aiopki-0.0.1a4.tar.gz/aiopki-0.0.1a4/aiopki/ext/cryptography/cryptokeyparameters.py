# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any

import pydantic


class CryptoKeyParameters(pydantic.BaseModel):
    __module__: str = 'aiopki.ext.cryptography'
    kty: str
    crv: str | None = None
    alg: str | None = None

    @pydantic.model_validator(mode='before')
    def preprocess(cls, values: dict[str, Any]) -> dict[str, Any]:
        crv = values.get('crv')
        if crv in {'P-256', 'P-256K', 'P-384', 'P-512'}:
            assert isinstance(crv, str)
            values['kty'] = 'EC'
            if not values.get('alg'):
                values['alg'] = 'ES' + re.sub(r'^P\-', '', crv)
        return values