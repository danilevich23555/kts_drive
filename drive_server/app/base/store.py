# Этот файл не надо менять, но разобраться стоит

import typing

from drive_server.app.base.connect_accessor import ConnectAccessor

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


class BaseStore:
    def __init__(self, app: 'Application'):
        self.app = app
        self._init_()
        # self.__connect()

    def _init_(self):
        pass

    @property
    def accessors(self) -> list[ConnectAccessor]:
        raise NotImplementedError

    # def __connect(self):
    #     for accessor in self.accessors:
    #         self.app.on_startup.append(accessor.connect)
    #         self.app.on_shutdown.append(accessor.disconnect)
