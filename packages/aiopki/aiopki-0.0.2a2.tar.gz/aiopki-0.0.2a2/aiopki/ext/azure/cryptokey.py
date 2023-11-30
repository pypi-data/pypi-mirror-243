# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import re
import urllib.parse
from typing import cast
from typing import Iterable

import pydantic
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.keys.aio import KeyClient
from azure.keyvault.keys.crypto.aio import CryptographyClient

import aiopki
import aiopki.utils
from aiopki.ext import jose
from aiopki.types import IAlgorithm
from aiopki.types import ICryptoKey
from .cryptokeyversion import CryptoKeyVersion


credential: DefaultAzureCredential = DefaultAzureCredential()


EC_ALGORITHMS = {
    'P-384': 'ES384'
}


class CryptoKey(pydantic.BaseModel):
    default: str | None
    name: str
    vault_url: str
    _versions: list[CryptoKeyVersion] = []
    _index: dict[str, CryptoKeyVersion] = {}
    _loaded: bool = False


    @property
    def crv(self) -> str | None:
        assert self.default is not None
        return self._index[self.default].jwk.crv # type: ignore

    @property
    def thumbprint(self) -> str:
        assert self.default is not None
        return self._index[self.default].jwk.thumbprint

    @classmethod
    def parse_uri(cls, uri: urllib.parse.ParseResult):
        if uri.hostname is None: # pragma: no cover
            raise ValueError(f"Invalid URI: {uri}")
        if not re.match(r'^.*\.vault\.azure\.net', uri.hostname):
            raise ValueError("Not an Azure key or secret.")
        m = re.match(r'^/keys/([^/]+)(/[0-9a-z]+)?$', uri.path)
        if m is None:
            raise ValueError(f"Invalid URI: {uri.path}")
        name, version = m.groups()
        if version:
            version = re.sub(r'[^a-z0-9]+', '', version)
        return cls.model_validate({
            'name': name,
            'vault_url': f'{uri.scheme}://{uri.netloc}/',
            'default': version
        })

    def can_use(self, algorithm: IAlgorithm) -> bool:
        return any([
            v.public.can_use(algorithm)
            for v in self._versions if v.public
        ])

    def default_algorithm(self) -> IAlgorithm:
        assert self.default is not None
        return self._index[self.default].default_algorithm()

    def versions(self) -> Iterable[ICryptoKey]:
        return self._versions

    async def discover(self, _client: KeyClient | None = None):
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        if self._loaded: # pragma: no cover
            return self
        client: KeyClient | None = _client
        credential: DefaultAzureCredential | None = None
        if client is None:
            credential = DefaultAzureCredential()
            client = KeyClient(self.vault_url, credential=credential)
        try:
            versions: list[CryptoKeyVersion] = []
            async for props in client.list_properties_of_key_versions(self.name): # type: ignore
                assert props.created_on is not None
                if not props.enabled or props.version is None:
                    continue
                version = await client.get_key(props.name, version=props.version) # type: ignore
                public = None
                if str(version.key_type or '') in {'EC', 'EC-HSM', 'RSA', 'RSA-HSM'}:
                    kty = re.sub(r'^(oct|EC|RSA)(\-HSM)?$', r'\1', str(version.key_type))
                    public = {}
                    if version.key.crv: # type: ignore
                        public['alg'] = EC_ALGORITHMS[version.key.crv] # type: ignore
                    for attname in version.key._FIELDS: # type: ignore
                        v = getattr(version.key, attname)
                        if isinstance(v, bytes):
                            v = aiopki.utils.b64encode(v)
                        if attname == 'key_ops':
                            v = [str(x) for x in v]
                        public[attname] = v
                    public = jose.JWK.model_validate({
                        **public,
                        'kty': kty
                    })
                    assert public.alg is not None
                    versions.append(
                        CryptoKeyVersion.model_validate({
                            'name': props.version,
                            'exp': props.expires_on,
                            'kty': kty,
                            'iat': props.created_on,
                            'nbf': props.not_before,
                            'uri': props.id,
                            'jwk': public
                        })
                    )
                    self._index[public.thumbprint] = versions[-1]
        finally:
            if credential is not None:
                assert client is not None
                await credential.close() # type: ignore
                await client.close()

        # Set a default version that is not expired.
        self._versions = versions
        for version in self._versions:
            if version.exp is not None and version.exp <= now:
                continue
            if version.nbf is not None and version.nbf > now:
                continue
            self.default = version.jwk.thumbprint
            break
        if self.default not in self._index: # pragma: no cover
            raise ValueError(f"Default key {self.default} does not exist.")
        self._loaded = True
        return self

    async def sign(self, message: bytes, algorithm: IAlgorithm, using: str | None = None) -> bytes:
        if not self._loaded: # pragma: no cover
            raise RuntimeError(f"Call {type(self).__name__}.discover() or await object.")
        assert self.default is not None
        version = self._index[using or self.default]
        message = algorithm.digest(message)
        async with DefaultAzureCredential() as credential:
            async with CryptographyClient(version.uri, credential=credential) as client:
                client = cast(CryptographyClient, client)
                result = await client.sign(version.jwk.alg, message) # type: ignore
        return result.signature

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm,
        using: str | None = None
    ) -> bool:
        assert self.default is not None
        version = self._index[using or self.default]
        assert version.public is not None
        return await version.public.verify(signature, message, algorithm, using)


    def __await__(self):
        return self.discover().__await__()