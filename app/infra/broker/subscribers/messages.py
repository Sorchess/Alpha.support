import logging
from faststream.rabbit import RabbitRouter

from utils.websocket import ws_manager

router = RabbitRouter()

logger = logging.getLogger(__name__)


@router.subscriber(queue="messages")
async def send_message(
    message: dict,
):
    await ws_manager.send_to_user(user_oid=message.get("author_oid"), message=message)
