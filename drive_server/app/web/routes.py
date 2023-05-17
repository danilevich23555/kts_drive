import typing

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


def setup_routes(app_: 'Application'):
    from drive_server.app.api.core.routes import setup_routes as core_setup_routes
    from drive_server.app.api.files.routes import setup_routes as files_setup_routes
    core_setup_routes(app_)
    files_setup_routes(app_)
