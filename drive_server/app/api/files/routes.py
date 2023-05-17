import typing

from drive_server.app.api.files.views.list import FilesListView
from drive_server.app.api.files.views.upload import FilesUploadView

if typing.TYPE_CHECKING:
    from drive_server.app.base.application import Application


def setup_routes(app: 'Application'):
    # TODO: добавить Route для недостающих методов
    app.cors.add(app.router.add_view('/files.list', FilesListView))
    app.cors.add(app.router.add_view('/files.upload', FilesUploadView))
