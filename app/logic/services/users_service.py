import logging
from dataclasses import dataclass, field

from fastapi import UploadFile

from core.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    ObjectNotFoundException,
    UserNotFoundException,
    UnsupportedMediaTypeException,
)
from utils.websocket import WebsocketMangager, ws_manager
from schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)


from core.security import (
    hash_password,
)
from infra.database.models.user import DEFAULT_AVATAR_KEY
from infra.storage.adapter import S3Adapter
from logic.services.base_service import BaseService

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}

logger = logging.getLogger(__name__)


@dataclass(eq=False, frozen=True)
class UsersService(BaseService):
    s3: S3Adapter
    ws: WebsocketMangager = field(default=ws_manager)

    async def get_user_info(
        self,
        user_oid: str,
    ) -> UserResponse:
        try:
            user = await self.db.users.get_model(oid=user_oid)
        except ObjectNotFoundException:
            raise UserNotFoundException

        folder = "presets" if user.avatar == DEFAULT_AVATAR_KEY else "uploads"

        user.avatar_url = await self.s3.get_presigned_url(
            folder=folder,
            file_name=user.avatar,
            expires_in=300,
        )

        return UserResponse.model_validate(user)

    async def create_user(
        self,
        user_create: UserCreate,
    ) -> str:

        new_user = UserCreate(
            email=user_create.email,
            password=hash_password(user_create.password),
        )

        try:
            user = await self.db.users.add(schema=new_user)
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
        return user.oid

    async def change_avatar(
        self,
        user_oid: str,
        file: UploadFile,
    ) -> None:
        try:
            await self.db.users.get_one(oid=user_oid)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise UnsupportedMediaTypeException

        key = await self.s3.upload_file(
            user_oid=user_oid,
            file=file,
        )

        await self.db.users.patch(oid=user_oid, column="avatar", value=key)

    async def verify_email(
        self,
        user_oid: str,
    ) -> None:
        await self.db.users.patch(oid=user_oid, column="email_verified", value=True)

    async def edit_user(
        self,
        user_oid: str,
        user_update: UserUpdate,
    ) -> None:
        if user_update.password:
            setattr(user_update, "password", hash_password(user_update.password))

        await self.db.users.update(oid=user_oid, schema=user_update)

        if user_update.email:
            await self.db.users.patch(
                oid=user_oid, column="email_verified", value=False
            )

    async def delete_user(
        self,
        user_oid: str,
    ) -> None:
        await self.db.users.delete(oid=user_oid)
