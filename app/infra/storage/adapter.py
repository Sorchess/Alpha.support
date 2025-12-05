import logging
from dataclasses import dataclass
from uuid import uuid4

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from urllib.parse import quote, unquote


from config import settings
from infra.storage.factory import S3ClientFactory
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
    factory: S3ClientFactory

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
            "owner_oid": user_oid,
            "original-filename": meta_value,
        }
        async with self.factory.client_getter() as client:
            try:
                await self.factory.put_object(
                    client=client,
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
        chunk_size: int,
    ) -> AsyncGenerator[bytes, None]:
        async with self.factory.client_getter() as client:
            try:
                response = await self.factory.get_object(client=client, key=key)
            except FileNotFoundException:
                raise FileNotFoundException
            except:
                raise StreamingFileFailedException

            async with response.get("Body") as stream:
                async for chunk in stream.content.iter_chunked(chunk_size):
                    yield chunk

    async def proxy_file(
        self,
        file_name: str,
        folder: str = "uploads",
    ):
        key = f"public/{folder}/{file_name}"
        chunk_size = 1024 * 1024

        async with self.factory.client_getter() as client:
            try:
                resp = await self.factory.head_object(client=client, key=key)
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
            chunk_size=chunk_size,
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
        async with self.factory.client_getter() as client:
            try:
                resp = await self.factory.head_object(client=client, key=key)
            except FileNotFoundException:
                raise FileNotFoundException
            except:
                raise FileDeleteFailedException

            meta = resp.get("Metadata") or {}
            owner_oid = meta.get("owner_oid")

            if not owner_oid:
                raise InvalidMetadataException

            if owner_oid != user_oid:
                raise NotAuthorizedException

            try:
                await self.factory.delete_object(client=client, key=key)
            except:
                raise FileDeleteFailedException

    async def get_presigned_url(
        self,
        file_name: str,
        expires_in: int,
        folder: str = "uploads",
    ) -> str:
        key = f"public/{folder}/{file_name}"
        async with self.factory.client_getter() as client:
            return await self.factory.generate_url(
                client=client, key=key, expires_in=expires_in
            )
