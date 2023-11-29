# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import importlib
import urllib.parse

from .types import ICryptoBackend


_BACKENDS: list[ICryptoBackend] = []


def install_backend(qualname: str, _version: str = 'v1') -> None:
    """Given the qualified name to a Python module, install
    the backend implementation of cryptographic operations.
    """
    module = importlib.import_module(qualname)
    if module not in _BACKENDS: # type: ignore
        _BACKENDS.insert(0, module) # type: ignore


def get_backend(uri: str | urllib.parse.ParseResult) -> ICryptoBackend:
    install_backend('aiopki.ext.cryptography')
    if not isinstance(uri, urllib.parse.ParseResult):
        uri = urllib.parse.urlparse(uri)
    backend = None
    for candidate in _BACKENDS:
        if not candidate.handles(uri):
            continue
        backend = candidate
        break
    if backend is None:
        raise ValueError("Unable to determine backend for URI.")
    return backend


def parse_uri(uri: str):
    backend = get_backend(uri)
    return backend.parse_key(urllib.parse.urlparse(uri))