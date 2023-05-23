import os
import typing

from drive_server.app.api.core.views.connect import CoreWSConnectView
from drive_server.app.api.core.views.current import CoreCurrentView
from drive_server.app.api.core.views.index import IndexView
from drive_server.app.api.core.views.login import AddUserView, CoreLoginView
from drive_server.main import BASE_DIR

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


def setup_routes(app: 'Application'):
    app.cors.add(app.router.add_view('/', IndexView))
    app.cors.add(app.router.add_view('/core.login', CoreLoginView))
    app.cors.add(app.router.add_view('/core.current', CoreCurrentView))
    app.cors.add(app.router.add_view('/core.ws_connect', CoreWSConnectView))
    app.cors.add(app.router.add_view('/adduser', AddUserView))
    app.cors.add(app.router.add_static('/static', os.path.join(BASE_DIR, 'app', 'templates', 'static')))
    # TODO: добавить Route для недостающих методов
