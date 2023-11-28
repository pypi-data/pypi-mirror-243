from typing import Optional, Union, Any, Dict

from drf_yasg.openapi import Schema, Parameter, IN_QUERY

from ._base import SwaggerParamsBase
from ._types import SwaggerParamsEnum


class SwaggerQueryParams(SwaggerParamsBase):
    name: str
    type: Union[SwaggerParamsEnum, Any]
    require: bool
    description: Optional[str]

    def __init__(self, name: str, require: bool = False,
                 description: Optional[str] = None):
        self.name = name
        self.type = SwaggerParamsEnum.string
        self.require = require
        self.description = description

    def params(self, properties: Optional[Dict[str, Schema]] = None, items: Schema = None) -> Union[Schema, Parameter]:
        return Parameter(
            name=self.name,
            in_=IN_QUERY,
            description=self.description,
            required=self.require,
            type=self.type
        )
