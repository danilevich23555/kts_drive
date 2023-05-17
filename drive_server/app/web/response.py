from datetime import datetime
from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response
from marshmallow import Schema, fields


class ResponseSchema(Schema):
    status = fields.Str(dump_default='ok')
    data = fields.Raw(dump_default={})



def json_response(data: Any = None, schema: Optional[Any] = None) -> Response:
    if schema:
        class __GeneratedSchema(Schema):
            status = fields.Str(dump_default='ok')
            data = fields.Nested(schema)

        schema = __GeneratedSchema
    else:
        schema = ResponseSchema

    resp = {
        'status': 'ok',
        'data': data,
    }

    return Response(
        body=schema().dumps(resp),
        headers={
            'Content-Type': 'application/json',
        }
    )


def error_json_response(
        http_status: int,
        status: str = "error",
        message: Optional[str] = None,
        data: Optional[dict] = None,
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data,
        },
    )
