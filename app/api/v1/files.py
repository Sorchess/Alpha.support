from fastapi import APIRouter, UploadFile, File

from api.dependencies.context import UserIdDep
from api.dependencies.services import FilesServiceDep
from core.exceptions import (
    StreamingFileFailedException,
    StreamingFileFailedHTTPException,
    FileNotFoundException,
    FileNotFoundHTTPException,
    InvalidMetadataException,
    NotAuthorizedException,
    FileDeleteFailedException,
    InvalidMetadataHTTPException,
    NotAuthorizedHTTPException,
    FileDeleteFailedHTTPException,
    FileTooLargeHTTPException,
    FileTooLargeException,
    FileUploadFailedException,
    FileUploadFailedHTTPException,
    EmptyFileException,
    EmptyFileExceptionHTTPException,
)

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/")
async def upload_file(
    files_service: FilesServiceDep,
    user_oid: UserIdDep,
    file: UploadFile = File(...),
):
    try:
        data = await files_service.upload_file(
            user_oid=user_oid,
            file=file,
        )
        return {
            "status": "success",
            "message": "File uploaded successfully.",
            "data": data,
        }
    except EmptyFileException:
        raise EmptyFileExceptionHTTPException
    except FileTooLargeException:
        raise FileTooLargeHTTPException
    except FileUploadFailedException:
        raise FileUploadFailedHTTPException


@router.get("/{file_name}")
async def proxy_file(
    files_service: FilesServiceDep,
    file_name: str,
):
    try:
        return await files_service.proxy_file(
            file_name=file_name,
        )
    except StreamingFileFailedException:
        raise StreamingFileFailedHTTPException
    except FileNotFoundException:
        raise FileNotFoundHTTPException


@router.delete("/{file_name}")
async def delete_file(
    files_service: FilesServiceDep,
    file_name: str,
    user_oid: UserIdDep,
):
    try:
        await files_service.delete_file(
            user_oid=user_oid,
            file_name=file_name,
        )
        return {
            "status": "success",
            "message": "File deleted successfully.",
        }
    except FileNotFoundException:
        raise FileNotFoundHTTPException
    except InvalidMetadataException:
        raise InvalidMetadataHTTPException
    except NotAuthorizedException:
        raise NotAuthorizedHTTPException
    except FileDeleteFailedException:
        raise FileDeleteFailedHTTPException
