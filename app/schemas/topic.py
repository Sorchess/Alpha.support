from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    title: str
    description: str


class TopicCreate(TopicBase):
    pass


class TopicDB(TopicBase):
    author_oid: str


class TopicResponse(TopicBase):
    oid: str
    author_oid: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
