# Этот файл не надо менять

import typing
from logging import Logger

from aiohttp import web
from aiohttp_cors import CorsConfig, CorsViewMixin

if typing.TYPE_CHECKING:
    from drive_server.app.config.dataclasses import Config
    from drive_server.app.store.store import Store


class Application(web.Application):
    config: 'Config'
    store: 'Store'
    cors: CorsConfig
    logger: typing.Optional[Logger] = None


class Request(web.Request):
    user_id: str

    @property
    def app(self) -> 'Application':
        return super().app


class View(CorsViewMixin, web.View):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def app(self) -> 'Application':
        return self.request.app

    @property
    def store(self) -> 'Store':
        return self.app.store

    # @property
    # def body(self) -> dict:
    #     return self.request.get('json', {})

    @property
    def user(self) -> typing.Optional[dict]:
        return self.request['session']

    @property
    def config(self) -> 'Config':
        return self.app.config
