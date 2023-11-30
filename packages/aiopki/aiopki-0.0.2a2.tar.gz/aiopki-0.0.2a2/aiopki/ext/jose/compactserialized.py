# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated
from typing import Any
from typing import TypeAlias

from pydantic_core import CoreSchema
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetJsonSchemaHandler

from .joseobject import JOSEObject
from .parser import parse


__all__: list[str] = [
    'CompactSerialized'
]


class CompactSerializedValidator:

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.chain_schema([
                core_schema.is_instance_schema(str),
                core_schema.str_schema(),
            ]),
            python_schema=core_schema.chain_schema(
                [
                    core_schema.is_instance_schema(str),
                    core_schema.no_info_plain_validator_function(parse),
                    core_schema.is_instance_schema(JOSEObject),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.encode(compact=True)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


CompactSerialized: TypeAlias = Annotated[JOSEObject, CompactSerializedValidator]