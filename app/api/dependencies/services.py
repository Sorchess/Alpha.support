from fastapi import Depends
from typing import Annotated

from api.dependencies.infra import (
    DBDep,
    CacheDep,
    S3Dep,
    EmailPublisherDep,
    MessagePublisherDep,
)
from logic.services.auth_service import AuthService
from logic.services.emails_service import EmailsService
from logic.services.files_service import FilesService
from logic.services.messages_service import MessagesService
from logic.services.sockets_service import SocketsService
from logic.services.topics_service import TopicsService
from logic.services.users_service import UsersService


def get_auth_service(
    db: DBDep,
    redis: CacheDep,
) -> AuthService:
    """Сервис аутентификации и авторизации"""
    return AuthService(db=db, redis=redis)


def get_users_service(
    db: DBDep,
    s3: S3Dep,
) -> UsersService:
    """Сервис управления пользователями"""
    return UsersService(db=db, s3=s3)


def get_emails_service(
    db: DBDep,
    redis: CacheDep,
    pub: EmailPublisherDep,
) -> EmailsService:
    """Сервис верификации и отправки email"""
    return EmailsService(db=db, redis=redis, pub=pub)


def get_files_service(
    db: DBDep,
    s3: S3Dep,
) -> FilesService:
    """Сервис для обработки файлов"""
    return FilesService(db=db, s3=s3)


def get_topics_service(
    db: DBDep,
) -> TopicsService:
    """Сервис управления топиками"""
    return TopicsService(db=db)


def get_message_service(
    db: DBDep,
    pub: MessagePublisherDep,
) -> MessagesService:
    """Сервис управления топиками"""
    return MessagesService(db=db, pub=pub)


def get_sockets_service(
    db: DBDep,
    redis: CacheDep,
) -> SocketsService:
    """Сервис управления топиками"""
    return SocketsService(db=db, redis=redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
EmailsServiceDep = Annotated[EmailsService, Depends(get_emails_service)]
FilesServiceDep = Annotated[FilesService, Depends(get_files_service)]
TopicsServiceDep = Annotated[TopicsService, Depends(get_topics_service)]
MessageServiceDep = Annotated[MessagesService, Depends(get_message_service)]
SocketsServiceDep = Annotated[SocketsService, Depends(get_sockets_service)]
