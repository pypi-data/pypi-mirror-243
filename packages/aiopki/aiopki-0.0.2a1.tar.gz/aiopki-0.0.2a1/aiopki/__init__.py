# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .algorithms import get as algorithm
from .algorithms import curve
from .algorithms import register
from .backends import install_backend
from .basecryptokey import BaseCryptoKey
from .cryptokeyspecification import CryptoKeySpecification
from .cryptokeyuri import CryptoKeyURI
from .secreturi import SecretURI
from . import types


__all__: list[str] = [
    'algorithm',
    'curve',
    'install_backend',
    'register',
    'types',
    'BaseCryptoKey',
    'CryptoKeySpecification',
    'CryptoKeyURI',
    'SecretURI',
]


def key(uri: str):
    pass