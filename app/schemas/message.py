from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageDB(MessageBase):
    topic_oid: str
    author_oid: str


class MessageResponse(MessageDB):
    oid: str
    sended_at: datetime

    model_config = ConfigDict(from_attributes=True)
