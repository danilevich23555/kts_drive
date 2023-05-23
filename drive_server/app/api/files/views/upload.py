import uuid
from datetime import datetime
from aiohttp.web import json_response

from drive_server.app.api.files.schemas import FilesUploadSchema
from drive_server.app.api.files.utils import make_upload_callback
from drive_server.app.base.application import View
from drive_server.app.store.websockets.websocket_accessor import WebSocketMessageKind
# from drive_server.app.web.response import json_response


class FilesUploadView(View):
    # TODO: @docs
    # TODO: @response_schema
    async def post(self):
        # TODO: получить id загрузки из заголовка X-Upload-Id и записать в upload_id
        raw_upload_id = self.request.headers.get('X-Upload-Id')
        upload_id = uuid.UUID(raw_upload_id)
        # TODO: получить файл и его имя из request.multipart
        from_fields = await self.request.multipart()
        reader, filename = None, None
        async for field in from_fields:
            if field.name == "file":
                reader = field
                filename = field.filename
                break
        content_length = self.request.headers.get('Content-Length')
        # TODO: получить его размер из заголовка Content-Length и  записать в total_size
        total_size = int(content_length)


        callback = make_upload_callback(self.store, self.request.user_id, upload_id, total_size)
        await self.store.s3.upload(key=filename, reader=reader, upload_callback=callback)
        await self.store.ws.push(self.request.user_id, kind=WebSocketMessageKind.UPLOAD_FINISH,
                                 data={
                                     'upload_id': str(upload_id)
                                 })
        # TODO: вызвать метод s3 accessor upload и пробросить нужные данные
        # TODO: дождаться конца загрузки
        #  и отправить в ws-канал сообщение о конце загрузки WebSocketMessageKind.UPLOAD_FINISH
        return json_response()
