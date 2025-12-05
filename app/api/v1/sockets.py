from fastapi import APIRouter, WebSocket

from api.dependencies.context import UserIdDep
from api.dependencies.services import UsersServiceDep

router = APIRouter(prefix="/ws", tags=["websockets"])


@router.post("/")
async def get_token(
    user_oid: UserIdDep,
    users_service: UsersServiceDep,
):
    data = await users_service.get_token(user_oid=user_oid)
    return {
        "status": "success",
        "data": data,
    }


@router.websocket("/")
async def ws_connect(
    token: str,
    websocket: WebSocket,
    users_service: UsersServiceDep,
):
    try:
        await users_service.ws_connect(
            websocket=websocket,
            token=token,
        )
    except Exception as ex:
        raise ex
