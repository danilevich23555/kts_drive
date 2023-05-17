from drive_server.app.base.store import BaseStore
from drive_server.app.store.s3.accessor import S3Accessor
from drive_server.app.store.postgres.user_accesor import CrmAccessor
from drive_server.app.store.websockets.websocket_accessor import WebSocketAccessor


class Store(BaseStore):
    def _init_(self):
        self.s3 = S3Accessor(self.app)
        self.ws = WebSocketAccessor(self.app)
        self.postgres_user = CrmAccessor(self.app)

    @property
    def accessors(self):
        # TODO: за-yield'ить все accessor, которым нужен connect
        pass
