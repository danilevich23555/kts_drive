import uuid

from drive_server.app.base.application import View
from drive_server.app.web.response import json_response
import bcrypt
from aiohttp.web_response import json_response
from aiohttp.web_exceptions import HTTPNotFound
import aiohttp_session
from aiohttp import web

from drive_server.app.database.sqlalchemy_model.models import User, UserSession
from drive_server.app.pydantic_model.models import User as UserValidPydantic
from work_with_cookie.utils import set_user_in_cockie



class CoreLoginView(View):
    # TODO: @docs
    # TODO: @json_schema
    # TODO: @response_schema
    async def post(self):
        try:
        # TODO: сделать авторизацию, создать сессию и сохранить uuid4() в session['user']['id']
            print(self.request.user_id)
            if self.request.user_id:
                return json_response(f'пользователь авторизирован!')
            data = await self.request.json()
            UserValidPydantic(email=data['username'])
            user = await self.app.store.postgres_user.get_user(data['username'])
            # raw_user = [(x.user_name, x.password, x.id) for x in user] #todo это выкидывай тут можно user.
            password_b = data['password'].encode('utf-8')
            res = bcrypt.checkpw(password_b, user.password.encode('utf-8'))
            print(res)
            if data['username'] != user.user_name or bcrypt.checkpw(password_b,
                                                                    user.password.encode('utf-8')) == False:
                raise web.HTTPForbidden(reason='Неверная пара логин/пароль!')
            session = await aiohttp_session.new_session(request=self.request)
            session['user'] = {
                'id': str(uuid.uuid4())
            }
            user_session = UserSession(user_id=user.id, id_session=session['user']['id'])
            await self.request.app.store.postgres_user.add_user(user_session) #todo при логине не нужно добовлять каждый раз юзера для этого есть метод register

            #todo добавляем куку в редис
            await set_user_in_cockie(request=self.request, usr_token=str(user.user_token))
        except Exception as ex:
            print(ex)

        return json_response(data= {'data': "login success", 'status': 'ok'})



class GetUserView(View):
    async def get(self,):
        user_id = self.request.query['id']
        user = await self.request.app.store.postgres_user.crm_accessor.get_user((user_id))
        if user:
            return json_response(text=f'{user}')
        else:
            raise HTTPNotFound




class AddUserView(View):
    async def post(self):
        data = await self.request.json()
        user = UserValidPydantic(email=data['username'])
        user = await self.app.store.postgres_user.get_user(data['username'])
        # raw_user = [x.user_name for x in user]
        # print(raw_user[0])
        if user is None:
            user1 = User(user_name=data['username'], password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode())
            print(user1.user_name, user1.password, user1.registration_time)
            await self.request.app.store.postgres_user.add_user(user1)
            return json_response(data={'status': 'ok', 'data_reg': f'{user1.user_name, user1.password,}'})