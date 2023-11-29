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
from typing import Any

import pydantic
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient



class Secret(pydantic.BaseModel):
    name: str
    vault_url: str
    version: str

    @classmethod
    def parse_uri(cls, uri: urllib.parse.ParseResult):
        m = re.match(r'^/secrets/([^/]+)/([0-9a-z]+)$', uri.path)
        if m is None:
            raise ValueError(f"Invalid URI: {uri.path}")
        name, version = m.groups()
        return cls.model_validate({
            'name': name,
            'vault_url': f'{uri.scheme}://{uri.netloc}/',
            'version': version
        })

    async def discover(self) -> Any:
        async with DefaultAzureCredential() as credential:
            async with SecretClient(self.vault_url, credential=credential) as client:
                secret = await client.get_secret(self.name, self.version) # type: ignore
        return secret.value # type: ignore

    def __await__(self):
        return self.discover().__await__()