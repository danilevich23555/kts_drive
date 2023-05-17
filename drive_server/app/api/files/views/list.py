from drive_server.app.api.files.schemas import FilesSchema
from drive_server.app.base.application import View
from drive_server.app.web.response import json_response


class FilesListView(View):
    # TODO: @docs
    # TODO: @response_schema
    async def get(self):
        # TODO: получить список всех файлов из S3 и отдать в нужном формате
        files = await self.store.s3.list_objects()
        return json_response({'items': files[::-1]})
