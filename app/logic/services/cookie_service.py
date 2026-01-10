from dataclasses import dataclass
from typing import Optional

from fastapi import Request, Response

from config import settings


@dataclass(eq=False, frozen=True)
class CookieService:
    cookie_name = settings.cookie.name
    cookie_max_age = settings.cookie.age * 24 * 60 * 60

    def set_auth_cookie(self, response: Response, session_id: str) -> None:
        response.set_cookie(
            key=self.cookie_name,
            value=session_id,
            httponly=True,
            max_age=self.cookie_max_age,
        )

    def delete_auth_cookie(self, response: Response) -> None:
        response.delete_cookie(self.cookie_name)

    def get_session_id(self, request: Request) -> Optional[str]:
        return request.cookies.get(self.cookie_name)
