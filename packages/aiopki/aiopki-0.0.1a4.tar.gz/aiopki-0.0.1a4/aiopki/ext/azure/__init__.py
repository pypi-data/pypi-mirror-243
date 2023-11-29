# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
import urllib.parse

from .cryptokey import CryptoKey
from .secret import Secret


__all__: list[str] = [
    'handles',
    'parse_key',
    'parse_secret'
]


def handles(uri: urllib.parse.ParseResult) -> bool:
    return uri.hostname is not None\
        and bool(re.match(r'^.*\.vault\.azure\.net', uri.hostname))


parse_key = CryptoKey.parse_uri
parse_secret = Secret.parse_uri