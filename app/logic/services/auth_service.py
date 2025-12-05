from dataclasses import dataclass, field

from fastapi import Response, Request

from config import settings
from core.exceptions import (
    MissingSessionCookieException,
    InvalidSessionCookieException,
    ObjectNotFoundException,
    UserNotFoundException,
    UserWrongPasswordException,
)
from core.security import generate_uuid, verify_password
from infra.redis.adapter import RedisAdapter
from schemas.user import UserCredentials, UserResponse
from logic.services.base_service import BaseService
from logic.services.cookie_service import CookieService


@dataclass(eq=False, frozen=True)
class AuthService(BaseService):
    redis: RedisAdapter
    cookie_service: CookieService = field(default_factory=CookieService)

    async def create_session(self, user_oid: str) -> str:
        session_id = generate_uuid()
        age = settings.cookie.age * 24 * 60 * 60
        await self.redis.set(key=session_id, value=user_oid, expire=age)
        return session_id

    async def verify_cookie(self, request: Request) -> str:
        cookie_value = self.cookie_service.get_session_id(request=request)

        if not cookie_value:
            raise MissingSessionCookieException

        user_oid = await self.redis.get(key=cookie_value)

        if not user_oid:
            raise InvalidSessionCookieException

        return user_oid

    async def verify_user(self, user_credentials: UserCredentials) -> UserResponse:
        try:
            user = await self.db.users.get_model(email=user_credentials.email)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not verify_password(user_credentials.password, user.password):
            raise UserWrongPasswordException

        return UserResponse.model_validate(user)

    async def sign_in(
        self,
        user_credentials: UserCredentials,
        response: Response,
    ) -> str:
        try:
            user = await self.verify_user(
                user_credentials=user_credentials,
            )
        except UserNotFoundException:
            raise UserNotFoundException
        except UserWrongPasswordException:
            raise UserWrongPasswordException

        session_id = await self.create_session(user_oid=user.oid)
        self.cookie_service.set_auth_cookie(response=response, session_id=session_id)
        return user.oid

    async def logout(
        self,
        response: Response,
        request: Request,
    ) -> None:
        cookie_value = self.cookie_service.get_session_id(request=request)

        user_id = await self.redis.get(cookie_value)

        if not user_id:
            raise InvalidSessionCookieException

        await self.redis.delete(cookie_value)

        self.cookie_service.delete_auth_cookie(response=response)
