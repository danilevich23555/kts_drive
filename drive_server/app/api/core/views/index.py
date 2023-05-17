# Этот файл не надо менять
import os

from aiohttp import web

from drive_server.app.base.application import View
from drive_server.main import BASE_DIR


class IndexView(View):
    async def get(self):
        with open(os.path.join(BASE_DIR, 'app', 'templates', 'index.html'), 'r') as f:
            file = f.read()

        file = file.replace('{{API_HOST}}', os.environ.get('API_EXPOSER_URL', 'http://0.0.0.0:8888'))
        return web.Response(body=file, headers={
            'Content-Type': 'text/html',
        })
