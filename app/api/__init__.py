from fastapi import APIRouter

from .v1 import api_v1
from config import settings

api_router = APIRouter(prefix=settings.api.prefix)
api_router.include_router(api_v1)
