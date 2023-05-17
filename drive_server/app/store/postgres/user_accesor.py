import typing
from typing import Optional
from sqlalchemy import select

from drive_server.app.database.sqlalchemy_model.models import User
from drive_server.app.database.sqlalchemy_model.database_sqlalchemy import Database
from drive_server.app.base.application import Request
from drive_server.app.base.connect_accessor import BaseAccessor
# if typing.TYPE_CHECKING:
#
#     from app.web.app import Application



class CrmAccessor(BaseAccessor):

    async def add_user(self, user):
        async with Database.session() as session:
            insert_user = user
            print(user)
            session.add(insert_user)
            await session.commit()

    async def list_users(self):
        async with Database.session() as sessions:
            stmt = select(User)
            results = await sessions.execute(stmt)
            return results.scalars()

    async def get_user(self, email):
        async with Database.session() as sessions:
            stmt = select(User).where(User.user_name == email)
            results = await sessions.execute(stmt)
            return results.scalars()
