from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict, HttpUrl


class UserCredentials(BaseModel):
    email: EmailStr = Field(min_length=4, max_length=255)
    password: str = Field(min_length=6)


class UserCreate(UserCredentials):
    pass


class UserUpdate(UserCredentials):
    email: EmailStr | None = Field(min_length=4, max_length=255, default=None)
    username: str | None = Field(min_length=4, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


class UserResponse(BaseModel):
    oid: str
    username: str
    email: EmailStr
    email_verified: bool
    is_staff: bool = False
    registered_in: datetime
    avatar_url: Optional[HttpUrl] = None

    model_config = ConfigDict(from_attributes=True)
