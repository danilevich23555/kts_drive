from drive_server.app.base.application import View
from drive_server.app.web.response import json_response


class FilesDeleteView(View):
    # TODO: @docs
    # TODO: @json_schema
    # TODO: @response_schema
    async def post(self):
        # TODO: удалить объект из S3 по ключу
        return json_response()
