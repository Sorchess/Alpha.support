from typing import Annotated

from fastapi import Request, Depends, WebSocketException

from api.dependencies.services import AuthServiceDep
from core.exceptions import (
    MissingSessionCookieException,
    MissingSessionCookieHTTPException,
    InvalidSessionCookieException,
    InvalidSessionCookieHTTPException,
)
from core.security import decode_jwt


async def get_user_oid(
    request: Request,
    auth_service: AuthServiceDep,
) -> str:
    """Извлекает OID авторизованного пользователя из cookie"""
    try:
        return await auth_service.verify_cookie(request=request)
    except MissingSessionCookieException:
        raise MissingSessionCookieHTTPException
    except InvalidSessionCookieException:
        raise InvalidSessionCookieHTTPException


UserIdDep = Annotated[int, Depends(get_user_oid)]
