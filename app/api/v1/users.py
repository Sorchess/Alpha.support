from fastapi import APIRouter, File, UploadFile, Response, Request

from api.dependencies.context import UserIdDep
from api.dependencies.services import EmailsServiceDep, UsersServiceDep, AuthServiceDep
from core.exceptions import (
    UserNotFoundException,
    UserNotFoundHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserEmailNotVerificatedException,
    UserEmailNotVerificatedHTTPException,
    UserWrongPasswordException,
    UserWrongPasswordHTTPException,
    InvalidSessionCookieException,
    InvalidSessionCookieHTTPException,
)
from schemas.user import UserCreate, UserUpdate, UserCredentials

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_personal_info(
    users_service: UsersServiceDep,
    user_oid: UserIdDep,
):
    try:
        result = await users_service.get_user_info(
            topic_oid=user_oid,
        )
        return {
            "status": "success",
            "data": result,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.get("/{user_oid}")
async def get_user(
    user_oid: str,
    users_service: UsersServiceDep,
):
    try:
        result = await users_service.get_user_info(
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "data": result,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post(
    "/sign-up",
)
async def register_user(
    user_create: UserCreate,
    users_service: UsersServiceDep,
    auth_service: AuthServiceDep,
    response: Response,
):
    try:
        user_oid = await users_service.create_user(user_create=user_create)
        data = await users_service.get_user_info(user_oid=user_oid)

        await auth_service.sign_in(
            user_credentials=user_create,
            response=response,
        )

        return {
            "status": "success",
            "message": "User created successfully.",
            "data": data,
        }
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserWrongPasswordException:
        raise UserWrongPasswordHTTPException


@router.post("/sign-in")
async def sign_in(
    response: Response,
    user_credentials: UserCredentials,
    auth_service: AuthServiceDep,
    users_service: UsersServiceDep,
):
    try:
        user_oid = await auth_service.sign_in(
            response=response,
            user_credentials=user_credentials,
        )
        data = await users_service.get_user_info(
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "message": "You have successfully logged in.",
            "data": data,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserWrongPasswordException:
        raise UserWrongPasswordHTTPException


@router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    auth_service: AuthServiceDep,
):
    try:
        await auth_service.logout(
            response=response,
            request=request,
        )
        return {
            "status": "success",
            "message": "You have successfully logged out.",
        }
    except InvalidSessionCookieException:
        raise InvalidSessionCookieHTTPException


@router.post("/edit")
async def edit_profile(
    user_update: UserUpdate,
    emails_service: EmailsServiceDep,
    user_oid: UserIdDep,
):
    try:
        await emails_service.edit_user(
            user_update=user_update,
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserEmailNotVerificatedException:
        raise UserEmailNotVerificatedHTTPException


@router.delete("/delete")
async def delete_user(
    emails_service: EmailsServiceDep,
    user_oid: UserIdDep,
):
    try:
        await emails_service.delete_user(
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except InvalidSessionCookieException:
        raise InvalidSessionCookieHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserEmailNotVerificatedException:
        raise UserEmailNotVerificatedHTTPException


@router.post("/verify-email")
async def verify_email(
    emails_service: EmailsServiceDep,
    user_oid: UserIdDep,
):
    try:
        await emails_service.verify_email(
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.patch("/change-avatar")
async def change_avatar(
    user_oid: UserIdDep,
    users_service: UsersServiceDep,
    file: UploadFile = File(...),
):
    try:
        await users_service.change_avatar(
            file=file,
            user_oid=user_oid,
        )
        return {
            "status": "success",
            "message": "Avatar changed successfully.",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
