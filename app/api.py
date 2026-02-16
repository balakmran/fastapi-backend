from fastapi import APIRouter

from app.modules.system import router as system_router
from app.modules.user import router as user_router

# Versioned API router
v1_router = APIRouter()
v1_router.include_router(user_router)

# Top-level API router with version prefix
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(v1_router)

# System routes stay at root (health, ready, root page)
system_router_root = system_router
