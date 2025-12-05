from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from aiobotocore.session import get_session
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError

from config import settings
from core.exceptions import FileNotFoundException


@dataclass
class S3ClientFactory:
    access_key: str = field(default=settings.s3.access_key)
    secret_key: str = field(default=settings.s3.secret_key)
    endpoint_url: str = field(default=settings.s3.endpoint_url)
    bucket_name: str = field(default=settings.s3.bucket_name)

    def __post_init__(self):
        self.boto_config = BotoConfig(
            connect_timeout=15,
            read_timeout=60,
            retries={"max_attempts": 3},
            max_pool_connections=20,
            tcp_keepalive=True,
            signature_version="s3v4",
        )
        self.config = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "endpoint_url": self.endpoint_url,
            "config": self.boto_config,
        }
        self.bucket_name = self.bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def client_getter(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def head_object(self, key: str):
        async with self.client_getter() as client:
            try:
                return await client.head_object(Key=key, Bucket=self.bucket_name)
            except client.exceptions.NoSuchKey:
                raise FileNotFoundException
            except ClientError as ex:
                raise ex

    async def put_object(
        self,
        path: str,
        data: bytes,
        content_type: str,
        size: int,
        metadata: dict,
    ):
        async with self.client_getter() as client:
            try:
                await client.put_object(
                    Key=path,
                    Body=data,
                    Bucket=self.bucket_name,
                    ContentType=content_type,
                    ContentLength=size,
                    Metadata=metadata,
                )
            except ClientError as ex:
                raise ex

    async def get_object(self, key: str, offset: int, end: int) -> bytes:
        async with self.client_getter() as client:
            try:
                return await client.get_object(
                    Bucket=self.bucket_name, Key=key, Range=f"bytes={offset}-{end}"
                )
            except client.exceptions.NoSuchKey:
                raise FileNotFoundException
            except ClientError as ex:
                raise ex

    async def delete_object(self, key: str):
        async with self.client_getter() as client:
            try:
                await client.delete_object(Bucket=self.bucket_name, Key=key)
            except ClientError as ex:
                raise ex

    async def generate_url(self, key: str, expires_in: int):
        async with self.client_getter() as client:
            params = {"Bucket": self.bucket_name, "Key": key}
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params=params,
                ExpiresIn=expires_in,
                HttpMethod="GET",
            )
