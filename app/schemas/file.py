from pydantic import BaseModel, ConfigDict


class FileCreate(BaseModel):
    key: str
    owner_oid: str
    size: int
    origin: str


class FileResponse(BaseModel):
    oid: str
    key: str
    origin: str
    size: int
    topic_oid: str | None
    owner_oid: str

    model_config = ConfigDict(from_attributes=True)
