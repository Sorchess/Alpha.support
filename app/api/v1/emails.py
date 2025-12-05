from fastapi import APIRouter, Request, Response
from pydantic import SecretStr

from api.dependencies.context import UserIdDep
from api.dependencies.services import UsersServiceDep, AuthServiceDep, EmailsServiceDep
from core.exceptions import (
    InvalidTokenHTTPException,
    InvalidTokenException,
    TooManyAttemptsHTTPException,
    TooManyAttemptsException,
)
from logic.useCases.verification import VerificationUseCase

router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/confirm")
async def confirm_code(
    user_oid: UserIdDep,
    users_service: UsersServiceDep,
    auth_service: AuthServiceDep,
    emails_service: EmailsServiceDep,
    response: Response,
    request: Request,
    code: SecretStr,
):
    try:
        await VerificationUseCase(
            users_service=users_service,
            auth_service=auth_service,
            emails_service=emails_service,
        ).confirm_action(
            code=code,
            user_oid=user_oid,
            response=response,
            request=request,
        )
        return {
            "status": "success",
            "message": "The verification code has been successfully verified.",
        }
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    except TooManyAttemptsException:
        raise TooManyAttemptsHTTPException
