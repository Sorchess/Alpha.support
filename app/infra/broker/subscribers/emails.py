import logging
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from faststream.rabbit import RabbitRouter

from core import email_backend

router = RabbitRouter()

env = Environment(
    loader=FileSystemLoader("/app/templates"),
    autoescape=True,
)
logger = logging.getLogger(__name__)


@router.subscriber(queue="emails")
async def send_email(email: EmailStr, payload: str):
    template = env.get_template("confirmation.html")
    html_content = await template.render_async(
        code=payload,
    )

    email_backend.send_email(
        recipient=email,
        subject="Cowork: space for students",
        html_content=html_content,
    )
