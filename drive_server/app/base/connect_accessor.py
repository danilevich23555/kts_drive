# Этот файл не надо менять, но разобраться стоит

import typing

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


class BaseAccessor:
    config: typing.Any

    def __init__(self, app: 'Application'):
        self.app = app
        self._init_()

    def _init_(self) -> None:
        return None


class ConnectAccessor(BaseAccessor):
    def _init_(self) -> None:
        return None

    async def connect(self, _: 'Application'):
        await self._connect()

    async def disconnect(self, _: 'Application'):
        await self._disconnect()

    async def _connect(self) -> None:
        return None

    async def _disconnect(self) -> None:
        return None
