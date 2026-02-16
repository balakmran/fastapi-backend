from fastapi import APIRouter

from app.modules.system import router as system_router
from app.modules.user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(system_router)
