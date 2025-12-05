import json
from dataclasses import dataclass
from pydantic import SecretStr
from fastapi import Request, Response

from core.exceptions import InvalidTokenException
from logic.services.auth_service import AuthService
from logic.services.emails_service import EmailsService
from logic.services.users_service import UsersService
from schemas.confirmation import ConfirmationAction
from schemas.user import UserUpdate


@dataclass
class VerificationUseCase:
    users_service: UsersService
    emails_service: EmailsService
    auth_service: AuthService

    async def confirm_action(
        self, user_oid: str, code: SecretStr, response: Response, request: Request
    ):
        values = await self.emails_service.verify_code(user_oid, code)

        if values.get("action") == ConfirmationAction.EMAIL_VERIFICATION:
            await self.users_service.verify_email(
                user_oid=user_oid,
            )

        elif values.get("action") == ConfirmationAction.USER_DELETION:
            await self.users_service.delete_user(
                user_oid=user_oid,
            )
            await self.auth_service.logout(
                response=response,
                request=request,
            )
        elif values.get("action") == ConfirmationAction.EDIT_USER:
            if values.get("payload") is None:
                raise InvalidTokenException
            await self.users_service.edit_user(
                user_oid=user_oid,
                user_update=UserUpdate(**json.loads(values.get("payload"))),
            )
        else:
            raise InvalidTokenException
