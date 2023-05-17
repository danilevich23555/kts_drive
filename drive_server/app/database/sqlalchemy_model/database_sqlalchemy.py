import logging
from contextlib import asynccontextmanager
from typing import AsyncContextManager
from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.ext.asyncio.session import async_session
from threading import Lock

from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

Base = declarative_base()
Base.metadata.schema = 'public'

class SingletonPool(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Database(object, metaclass=SingletonPool):
    """Отвечает за соединения с БД"""

    __pool = dict()
    _lock: Lock = Lock()

    @classmethod
    def create_engine(cls, name=None, *args, **kwargs) -> None:
        if name is None:
            name = 'root'
        if name in cls.__pool:
            raise Exception("this engine already exist")

        else:
            _engine = create_async_engine(
                kwargs["dsn"],
                echo=False,
                future=True,
                connect_args={"command_timeout": 60},
                pool_size=kwargs["pool_size"]
            )
            cls.__pool[name] = _engine

    @classmethod
    def get_pool(cls, name=None) -> create_async_engine:
        if name is None:
            name = 'root'
        if name not in cls.__pool:
            raise KeyError(f'engin with name {name} does not exist')
        return cls.__pool.get(name)

    async def stop(cls) -> None:
        await cls.get_pool.dispose()  # type: ignore


    @classmethod
    @asynccontextmanager
    async def session(cls) -> AsyncContextManager[AsyncSession]:
        _sessionmaker: sessionmaker = sessionmaker(
            cls.get_pool(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        session = _sessionmaker()

        try:
            yield session
        except Exception as ex:
            await session.rollback()
            raise
        finally:
            session.commit()
            await session.close()


# @asynccontextmanager
# async def get_session() -> AsyncContextManager[AsyncSession]:
#     _async_session = async_scoped_session(
#         async_sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             class_=AsyncSession,
#             expire_on_commit=False,
#             bind=Database.get_pool(),
#         ),
#         scopefunc=current_task,
#     )
#
#     session = _async_session()
#     try:
#         yield session
#     except Exception as ex:
#         logger.error(str(ex))
#         await session.rollback()
#         raise
#     finally:
#         await session.close()
#         await _async_session.remove()
