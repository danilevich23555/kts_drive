import base64
import os
import pathlib

import aiohttp_cors
import fernet as fernet
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import asyncio
import aioredis


from drive_server.app.base.application import Application
from drive_server.app.config.dataclasses import create_config
from drive_server.app.database.sqlalchemy_model.database_sqlalchemy import Database
from drive_server.app.store.store import Store
from drive_server.app.web.middlewares import setup_middlewares
from drive_server.app.web.routes import setup_routes
from drive_server.app.settings.settings import settings


BASE_DIR = pathlib.Path(__file__).parent


async def make_redis_pool():
    redis_address = settings.DSN_REDIS
    return await aioredis.create_redis_pool(redis_address, timeout=1)

def create_app() -> Application:
    app: Application = web.Application()
    app.config = create_config(app)
    # TODO: настроить базовую конфигурацию для логгера
    # TODO: присвоить app.logger новый логгер
    app.store = Store(app)
    app.cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        )
    })
    # TODO: aiohttp_session.setup, cookie name='sessionid'
    # loop = asyncio.get_event_loop()
    # redis_pool = loop.run_until_complete(make_redis_pool())
    # storage = RedisStorage(redis_pool)
    #
    # async def dispose_redis_pool(app):
    #     redis_pool.close()
    #     await redis_pool.wait_closed()
    #
    # # setup(app, storage)
    # app.on_cleanup.append(dispose_redis_pool)
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    storage = EncryptedCookieStorage(secret_key)
    setup(app, storage)
    setup_routes(app)
    Database.create_engine(dsn=settings.POSTGRES_DSN, pool_size=20)
    # TODO: setup_aiohttp_apispec, указать static_path='/swagger_static' для избежания конфликта со статикой приложения
    setup_middlewares(app)
    return app


if __name__ == '__main__':
    print(f'Интерфейс S3 доступен по {settings.DSN_MINIO},'
          f' логин: {settings.MINIO_ACCESS_KEY}, пароль: {settings.MINIO_SECRET_KEY}')
    web.run_app(create_app(), port=8888)
