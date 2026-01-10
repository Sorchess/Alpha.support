from enum import Enum

from pydantic import BaseModel

from config import settings


class ConfirmationAction(
    str, Enum
):  # без str пришлось бы писать например EMAIL_VERIFICATION.value
    EMAIL_VERIFICATION = "email_verification"
    USER_DELETION = "user_deletion"
    EDIT_USER = "edit_user"


class ConfirmationRequest(BaseModel):
    action: ConfirmationAction
    code: str
    attempts: int = settings.verification.attempts
    payload: str
