# Этот файл не надо менять
from drive_server.app.base.application import View


class CoreWSConnectView(View):
    async def get(self):
        self.app.logger.info(f'New ws connection user_id={self.request.user_id}')
        ws = await self.store.ws.handle(self.request)
        return ws
