from aiohttp import web
from aiohttp.web_response import json_response

from drive_server.app.base.application import View



class CoreCurrentView(View):
    # TODO: @docs
    # TODO: @response_schema
    async def get(self):
        # TODO: отдавать 401 ошибку, только пользователь не авторизован
        if not self.request.user_id:
            raise web.HTTPUnauthorized
        return json_response()
