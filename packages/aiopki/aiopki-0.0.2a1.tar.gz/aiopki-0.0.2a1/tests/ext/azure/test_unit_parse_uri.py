# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import pytest

from aiopki.ext import azure


def test_parse_key(key_uri: urllib.parse.ParseResult, vault_url: str):
    obj = azure.CryptoKey.parse_uri(key_uri)
    assert obj.vault_url == vault_url


def test_parse_key_version(key_version_uri: urllib.parse.ParseResult, vault_url: str):
    obj = azure.CryptoKey.parse_uri(key_version_uri)
    assert obj.vault_url == vault_url
    assert obj.default is not None


@pytest.mark.parametrize("uri", [
    "https://www.example.com",
    "https://www.example.com/foo",
    "https://foo.vault.azure.net/bar/baz"
])
def test_parse_invalid_uri(uri: str):
    with pytest.raises(ValueError):
        azure.CryptoKey.parse_uri(urllib.parse.urlparse(uri))