from dataclasses import dataclass

from fastapi import UploadFile

from core.exceptions import (
    FileNotFoundException,
    StreamingFileFailedException,
    FileDeleteFailedException,
    InvalidMetadataException,
    NotAuthorizedException,
    FileTooLargeException,
    FileUploadFailedException,
    EmptyFileException,
    ObjectNotFoundException,
)
from schemas.file import FileCreate, FileResponse
from infra.storage.adapter import S3Adapter
from logic.services.base_service import BaseService


@dataclass(eq=False, frozen=True)
class FilesService(BaseService):
    s3: S3Adapter

    async def proxy_file(
        self,
        file_name: str,
    ):
        try:
            return await self.s3.proxy_file(
                file_name=file_name,
            )
        except FileNotFoundException:
            raise FileNotFoundException
        except StreamingFileFailedException:
            raise StreamingFileFailedException

    async def upload_file(
        self,
        user_oid: str,
        file: UploadFile,
    ) -> FileResponse:
        try:
            key = await self.s3.upload_file(
                user_oid=user_oid,
                file=file,
            )
        except EmptyFileException:
            raise EmptyFileException
        except FileTooLargeException:
            raise FileTooLargeException
        except FileUploadFailedException:
            raise FileUploadFailedException

        new_file = FileCreate(
            key=key,
            owner_oid=user_oid,
            size=file.size,
            origin=file.filename or "unknown",
        )

        return await self.db.files.add(schema=new_file)

    async def delete_file(
        self,
        file_name: str,
        user_oid: str,
    ) -> None:
        try:
            await self.db.files.get_one(key=file_name)
        except ObjectNotFoundException:
            raise FileNotFoundException

        try:
            await self.s3.delete_file(
                file_name=file_name,
                user_oid=user_oid,
            )
        except FileNotFoundException:
            raise FileNotFoundException
        except InvalidMetadataException:
            raise InvalidMetadataException
        except NotAuthorizedException:
            raise NotAuthorizedException
        except FileDeleteFailedException:
            raise FileDeleteFailedException

        await self.db.files.delete(key=file_name)
