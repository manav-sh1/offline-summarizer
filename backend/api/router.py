from fastapi import APIRouter

from backend.api.routes import health, text

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(text.router, prefix="/text", tags=["text"])
