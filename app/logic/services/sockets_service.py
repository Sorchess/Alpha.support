from dataclasses import dataclass, field
from fastapi import WebSocket, WebSocketException, WebSocketDisconnect

from core.security import generate_uuid
from infra.redis.adapter import RedisAdapter
from logic.services.base_service import BaseService
from utils.websocket import WebsocketMangager, ws_manager


@dataclass(eq=False, frozen=True)
class SocketsService(BaseService):
    redis: RedisAdapter
    ws: WebsocketMangager = field(default=ws_manager)

    async def get_token(self, user_oid: str) -> str:
        token = generate_uuid()
        key = f"token:{token}"
        await self.redis.set(key=key, value=user_oid)
        return token

    async def ws_connect(
        self,
        token: str,
        websocket: WebSocket,
    ):
        key = f"token:{token}"
        user_oid = await self.redis.get(key=key)

        if not user_oid:
            raise WebSocketException(code=1008)

        await self.ws.connect(user_oid=user_oid, websocket=websocket)
        try:
            while True:
                # Просто держим соединение открытым
                data = await websocket.receive_text()

        except WebSocketDisconnect:
            self.ws.disconnect(user_oid, websocket)
