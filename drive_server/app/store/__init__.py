import typing

from drive_server.app.store.postgres.user_accesor import CrmAccessor
if typing.TYPE_CHECKING:
    from drive_server.app.web.app import Application


def setup_accessors(app: "Application"):
    app.crm_accessor = CrmAccessor()