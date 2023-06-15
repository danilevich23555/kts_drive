import logging

from aiohttp_session import get_session, new_session

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def set_user_in_cockie(request, usr_token):
    if request is not None:
        request.session = await get_session(request)
        logger.info(f'Текущая кука session_id={request.session.identity}, new={request.session.new}, '
                    f'user={request.session.get("usr_token")}')
        if request.session.identity is None:
            request.session = await new_session(request)
        request.session['usr_token'] = usr_token
        request.session.update()
        logger.info(f'Положили в куку session_id={request.session.identity}, user={request.session.get("usr_token")}')
