from drive_server.app.base.application import View


class CoreCurrentView(View):
    # TODO: @docs
    # TODO: @response_schema
    async def get(self):
        # TODO: отдавать 401 ошибку, только пользователь не авторизован
        raise NotImplementedError
