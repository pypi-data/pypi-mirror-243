from ._params import SwaggerParams
from ._query import SwaggerQueryParams
from ._response import SwaggerParamsResponse
from ._types import SwaggerParamsEnum

params = Params = SwaggerParams
query = Query = SwaggerQueryParams
response_type = ResponseType = SwaggerParamsResponse
response_schema = ResponseSchema = SwaggerParamsResponse.inner
params_types = ParamsTypes = SwaggerParamsEnum

__all__ = [
    "params",
    "Params",
    "query",
    "Query",
    "response_type",
    "ResponseType",
    "response_schema",
    "ResponseSchema",
    "params_types",
    "ParamsTypes",
]
