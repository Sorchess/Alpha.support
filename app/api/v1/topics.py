from fastapi import APIRouter

from api.dependencies.context import UserIdDep
from api.dependencies.services import TopicsServiceDep, MessageServiceDep
from core.exceptions import (
    TopicAlreadyExistsHTTPException,
    TopicAlreadyExistsException,
    TopicNotFoundHTTPException,
    TopicNotFoundException,
    MessageAlreadyExistsException,
    MessageAlreadyExistsHTTPException,
    NotAuthorizedException,
    NotAuthorizedHTTPException,
)
from schemas.message import MessageCreate
from schemas.topic import TopicCreate

router = APIRouter(prefix="/topic", tags=["topic"])


@router.get("/")
async def get_topics(
    user_oid: UserIdDep,
    topics_service: TopicsServiceDep,
):
    data = await topics_service.get_topics(user_oid=user_oid)
    return {
        "status": "success",
        "data": data,
    }


@router.post("/", status_code=201)
async def upload_topic(
    user_oid: UserIdDep,
    topics_service: TopicsServiceDep,
    topic_create: TopicCreate,
):
    try:
        data = await topics_service.upload_topic(
            user_oid=user_oid, topic_create=topic_create
        )
        return {
            "status": "success",
            "data": data,
        }
    except TopicAlreadyExistsException:
        raise TopicAlreadyExistsHTTPException


@router.post("/{topic_oid}/message")
async def upload_message(
    topic_oid: str,
    user_oid: UserIdDep,
    message_create: MessageCreate,
    message_serivce: MessageServiceDep,
):
    try:
        message = await message_serivce.send_message(
            user_oid=user_oid, topic_oid=topic_oid, message_create=message_create
        )
        return {
            "status": "success",
            "data": message,
        }
    except MessageAlreadyExistsException:
        raise MessageAlreadyExistsHTTPException


@router.get("/{topic_oid}/messages")
async def get_messages(
    topic_oid: str,
    user_oid: UserIdDep,
    message_service: MessageServiceDep,
):
    try:
        data = await message_service.get_messages(
            topic_oid=topic_oid, user_oid=user_oid
        )
        return {
            "status": "success",
            "data": data,
        }
    except NotAuthorizedException:
        raise NotAuthorizedHTTPException
