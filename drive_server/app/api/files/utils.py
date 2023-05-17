from uuid import UUID

from drive_server.app.store.store import Store
from drive_server.app.store.websockets.websocket_accessor import WebSocketMessageKind


def make_upload_callback(store: Store, user_id: str, upload_id: UUID, total_size: int):
    async def upload_callback(uploaded_size: int):
        await store.ws.push(user_id=user_id, kind=WebSocketMessageKind.UPLOAD_PROGRESS,
                            data={
                                "upload_id": str(upload_id),
                                "total_size": total_size,
                                "uploaded_size": uploaded_size
                            })

    return upload_callback
