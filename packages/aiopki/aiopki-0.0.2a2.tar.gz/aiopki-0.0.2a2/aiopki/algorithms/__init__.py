# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy

from cryptography.hazmat.primitives.asymmetric import ec

from ..types import IAlgorithm
from .aesencryption import AESEncryption
from .edwardscurvedigitalsigning import EdwardsCurveDigitalSigning
from .ellipticcurvesigning import EllipticCurveSigning
from .hmacsigning import HMACSigning
from .notimplemented import NotImplementedAlgorithm
from .rsasigning import RSASigning


__all__: list[str] = [
    'get',
    'register',
    'AESEncryption',
    'EdwardsCurveDigitalSigning',
    'EllipticCurveSigning',
    'HMACSigning',
    'RSASigning',
]


_REGISTRY: dict[str, IAlgorithm] = {}

CURVE_MAPPING: dict[str, type[ec.EllipticCurve]] = {
    "P-256": ec.SECP256R1,
    "P-384": ec.SECP384R1,
    "P-521": ec.SECP521R1,
    "P-256K": ec.SECP256K1,
    "P-512": ec.SECP521R1,
    ec.SECP256R1.__name__: ec.SECP256R1, 
    ec.SECP384R1.__name__: ec.SECP384R1, 
    ec.SECP521R1.__name__: ec.SECP521R1, 
    ec.SECP256K1.__name__: ec.SECP256K1, 
}


def curve(name: str) -> ec.EllipticCurve:
    return CURVE_MAPPING[name]()


def register(name: str, alg: IAlgorithm) -> None:
    alg = copy.deepcopy(alg)
    alg.name = name
    _REGISTRY[name] = alg


def get(name: str) -> IAlgorithm:
    return _REGISTRY[name]


register('notimplemented', NotImplementedAlgorithm())