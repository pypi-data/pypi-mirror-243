# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


SUPPORTED_KEYS: list[str] = [
    "rfc7515:a1",
    "rfc7515:a2",
    "rfc7515:a3",
    "rfc7515:a4",
    "rfc8037:a1"
]

ENCRYPTION_KEYS: list[tuple[str, str]] = [
    ('symmetric16', 'A128GCM'),
    ('symmetric24', 'A192GCM'),
    ('symmetric32', 'A256GCM'),
]