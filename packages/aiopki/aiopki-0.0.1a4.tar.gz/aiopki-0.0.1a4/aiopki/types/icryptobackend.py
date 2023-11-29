# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import urllib.parse
from typing import Protocol

from .icryptokey import ICryptoKey
from .isecret import ISecret


class ICryptoBackend(Protocol):
    __module__: str = 'aiopki.types'

    def handles(self, uri: urllib.parse.ParseResult) -> bool: ...
    def parse_key(self, uri: urllib.parse.ParseResult) -> ICryptoKey: ...
    def parse_secret(self, uri: urllib.parse.ParseResult) -> ISecret[Any]: ...