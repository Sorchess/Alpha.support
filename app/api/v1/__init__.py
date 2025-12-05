from fastapi import APIRouter

from .users import router as users_router
from .emails import router as emails_router
from .files import router as storage_router
from .topics import router as topics_router
from .sockets import router as sockets_router

api_v1 = APIRouter(prefix="/v1")
api_v1.include_router(users_router)
api_v1.include_router(emails_router)
api_v1.include_router(topics_router)
api_v1.include_router(storage_router)
api_v1.include_router(sockets_router)
