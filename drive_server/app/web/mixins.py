from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized


# TODO: разобраться в работе этого миксина
class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if not getattr(self.request, "user_id", None):
            raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()
