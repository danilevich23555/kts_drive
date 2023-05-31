import json
from enum import Enum
from typing import Any, Optional
from aiohttp import web

from drive_server.app.base.application import Request
from drive_server.app.base.connect_accessor import BaseAccessor


class WSConnectionNotFound(Exception):
    pass


class WebSocketMessageKind(Enum):
    INITIAL = 'initial'
    UPLOAD_PROGRESS = 'upload_progress'
    UPLOAD_FINISH = 'upload_finish'


class WebSocketAccessor(BaseAccessor):
    def _init_(self):
        self._connections: dict[str, Any] = {}  # место, где хранится пара (user_id, WebSocketResponse)
        print(self._connections)

    async def handle(self, request: Request):
        # TODO: закрыть ws-сессию, если она уже есть
        await self.close(request.user_id)

        # TODO: подготовить WebSocketResponse
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # TODO: положить его в self._connections по user_id
        self._connections[request.user_id] = ws
        # TODO: отправить сообщения с типом WebSocketMessageKind.INITIAL
        await self.push(request.user_id, WebSocketMessageKind.INITIAL,
                        data= {
                            'trace_id': request.user_id
                        })
        # TODO: держать соединение
        await self.read(user_id=request.user_id)
        # TODO: вернуть ответ
        return ws


    async def close(self, _id: str):
        # TODO: закрыть ws-сессию по ключу
        try:
            await self._connections[_id].close()
        except KeyError:
            return None
        raise NotImplementedError

    async def push(self, user_id: str, kind: WebSocketMessageKind, data: Optional[dict] = None):
        # TODO: сформировать data и вызвать self._push, включив переданный kind
        if data is None:
            data = {}
        data['kind'] = kind.name
        json_data = json.dumps(data)
        await self._push(user_id, json_data)

    async def read(self, user_id: str):
        # TODO: читать сообщения из канала, чтобы не закрывать его
        async for message in self._connections[user_id]:
            self.app.logger.info(f'New ws message: {message.data}')

    async def _push(self, _id: str, data: str):
        # TODO: отправить сообщение в канал, а если канала нет, то кинуть WSConnectionNotFound
        try:
            await self._connections[_id].send_str(data)
        except KeyError:
            raise WSConnectionNotFound



