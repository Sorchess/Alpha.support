from fastapi import WebSocket


class WebsocketMangager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, user_oid: str, websocket: WebSocket):
        await websocket.accept()
        if user_oid not in self.active_connections:
            self.active_connections[user_oid] = []
        self.active_connections[user_oid].append(websocket)

    def disconnect(self, user_oid: str, websocket: WebSocket):
        if user_oid in self.active_connections:
            self.active_connections[user_oid].remove(websocket)

    async def send_to_user(self, user_oid: str, message: dict):
        """Отправляет сообщение на все устройства конкретного юзера"""
        if user_oid in self.active_connections:
            for connection in self.active_connections[user_oid]:
                try:
                    await connection.send_json(message)
                except RuntimeError:
                    pass


ws_manager = WebsocketMangager()
