import logging
from dataclasses import dataclass
from uuid import uuid4

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from urllib.parse import quote, unquote


from config import settings
from infra.storage.client import S3ClientFactory
from utils.file import (
    get_ext_from_upload,
    build_content_disposition,
)
from core.exceptions import (
    StreamingFileFailedException,
    FileNotFoundException,
    FileDeleteFailedException,
    InvalidMetadataException,
    NotAuthorizedException,
    FileTooLargeException,
    FileUploadFailedException,
    EmptyFileException,
)

logger = logging.getLogger(__name__)


@dataclass
class S3Adapter:
    client: S3ClientFactory

    async def upload_file(
        self,
        file: UploadFile,
        user_oid: str,
        folder: str = "uploads",
    ) -> str:
        key = uuid4().hex
        content_type = file.content_type or "application/octet-stream"
        ext = get_ext_from_upload(file)

        path = f"public/{folder}/{key}{ext}"

        data = await file.read()
        size = len(data)
        if size == 0:
            raise EmptyFileException
        if size > settings.s3.max_size * 1024 * 1024:
            raise FileTooLargeException

        original_name = file.filename or "unknown"
        meta_value = quote(original_name)

        metadata = {
            "author_oid": user_oid,
            "original-filename": meta_value,
        }

        try:
            await self.client.put_object(
                path=path,
                data=data,
                content_type=content_type,
                size=size,
                metadata=metadata,
            )
            return f"{key}{ext}"
        except Exception:
            raise FileUploadFailedException

    async def _get_file_chunk(
        self,
        key: str,
        content_length: int,
        chunk_length: int,
    ) -> AsyncGenerator[bytes, None]:
        for offset in range(0, content_length, chunk_length):
            end = min(offset + chunk_length - 1, content_length - 1)
            try:
                file = await self.client.get_object(key=key, offset=offset, end=end)
            except FileNotFoundException:
                raise FileNotFoundException
            except:
                raise StreamingFileFailedException

            async with file["Body"] as stream:
                yield await stream.read()

    async def proxy_file(
        self,
        file_name: str,
        folder: str = "uploads",
    ):
        key = f"public/{folder}/{file_name}"
        chunk_lenght = 1024 * 1024

        try:
            resp = await self.client.head_object(key=key)
        except FileNotFoundException:
            raise FileNotFoundException
        except:
            raise StreamingFileFailedException

        content_length = resp.get("ContentLength")
        content_type: str = resp.get("ContentType") or "application/octet-stream"

        meta = resp.get("Metadata") or {}
        encoded_name = meta.get("original-filename")
        original_name = None

        if encoded_name:
            try:
                original_name = unquote(encoded_name)
            except Exception as exception:
                logger.warning(f"Error with unquote file name: {exception}")

        disposition = build_content_disposition(
            original_name=original_name, default_name=file_name
        )

        headers = {
            "Content-Disposition": disposition,
            "Content-Length": str(content_length),
            "Accept-Ranges": "bytes",
        }

        file_chunk_iterator = self._get_file_chunk(
            key=key,
            content_length=content_length,
            chunk_length=chunk_lenght,
        )
        return StreamingResponse(
            content=file_chunk_iterator, media_type=content_type, headers=headers
        )

    async def delete_file(
        self,
        file_name: str,
        user_oid: str,
        folder: str = "uploads",
    ):
        key = f"public/{folder}/{file_name}"

        try:
            resp = await self.client.head_object(key=key)
        except FileNotFoundException:
            raise FileNotFoundException
        except:
            raise FileDeleteFailedException

        meta = resp.get("Metadata") or {}
        author = meta.get("author_oid")

        if not author:
            raise InvalidMetadataException

        try:
            author_oid = int(author)
        except ValueError:
            raise InvalidMetadataException

        if author_oid != user_oid:
            raise NotAuthorizedException

        try:
            await self.client.delete_object(key=key)
        except:
            raise FileDeleteFailedException

    async def get_presigned_url(
        self,
        file_name: str,
        expires_in: int,
        folder: str = "uploads",
    ) -> str:
        key = f"public/{folder}/{file_name}"
        return await self.client.generate_url(key=key, expires_in=expires_in)
