import logging
from dataclasses import dataclass

from pydantic import SecretStr

from config import settings
from core.exceptions import (
    InvalidTokenException,
    TooManyAttemptsException,
    ObjectNotFoundException,
    UserNotFoundException,
    UserEmailNotVerificatedException,
)
from infra.broker.publishers.emails import EmailPublisher
from infra.redis.adapter import RedisAdapter
from schemas.confirmation import ConfirmationRequest, ConfirmationAction
from schemas.user import UserResponse, UserUpdate
from core.security import (
    hash_password,
    verify_password,
    generate_secret_code,
)
from logic.services.base_service import BaseService

logger = logging.getLogger(__name__)


@dataclass(eq=False, frozen=True)
class EmailsService(BaseService):
    redis: RedisAdapter
    pub: EmailPublisher

    @staticmethod
    def _redis_keys(user_oid: str) -> str:
        return f"confirm:user:{user_oid}"

    async def send_confirmation_code(
        self,
        action: ConfirmationAction,
        user: UserResponse,
        payload: str = "",
    ) -> None:
        key = self._redis_keys(user_oid=user.oid)

        code = generate_secret_code()
        code_hash = hash_password(code)

        values = ConfirmationRequest(action=action, code=code_hash, payload=payload)
        expire = settings.verification.ttl * 60

        await self.redis.hset(
            key=key,
            values=values.model_dump(),
            expire=expire,
        )

        await self.pub.publish(
            message={
                "email": user.email,
                "payload": code,
            },
        )

    async def verify_code(
        self,
        user_oid: str,
        code: SecretStr,
    ) -> dict:

        key = self._redis_keys(user_oid=user_oid)
        values = await self.redis.hgetall(key=key)

        if not values:
            raise InvalidTokenException

        if not verify_password(
            password=code.get_secret_value(),
            hashed_password=values.get("code"),
        ):
            values["attempts"] = str(int(values.get("attempts")) - 1)

            await self.redis.hset(
                key=key,
                values=values,
            )

            if int(values.get("attempts", "0")) <= 0:
                await self.redis.delete(
                    key=key,
                )
                raise TooManyAttemptsException

            raise InvalidTokenException

        await self.redis.delete(key=key)

        return values

    async def edit_user(
        self,
        user_oid: str,
        user_update: UserUpdate,
    ) -> None:
        try:
            user = await self.db.users.get_one(oid=user_oid)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not user.email_verified:
            raise UserEmailNotVerificatedException

        await self.send_confirmation_code(
            user=user,
            action=ConfirmationAction.EDIT_USER,
            payload=user_update.model_dump_json(exclude_unset=True, exclude_none=True),
        )

    async def delete_user(
        self,
        user_oid: str,
    ) -> None:
        try:
            user = await self.db.users.get_one(oid=user_oid)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not user.email_verified:
            raise UserEmailNotVerificatedException

        await self.send_confirmation_code(
            action=ConfirmationAction.USER_DELETION,
            user=user,
        )

    async def verify_email(
        self,
        user_oid: str,
    ) -> None:
        try:
            user = await self.db.users.get_one(oid=user_oid)
        except ObjectNotFoundException:
            raise UserNotFoundException

        await self.send_confirmation_code(
            action=ConfirmationAction.EMAIL_VERIFICATION,
            user=user,
        )
