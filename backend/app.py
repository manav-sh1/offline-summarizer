from fastapi import FastAPI

from backend.api.router import api_router
from config import get_settings
from logging_config import get_logger


logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    logger.info("Creating FastAPI application for %s", settings.app_name)
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.include_router(api_router, prefix=settings.api_base_path)
    logger.info("Registered API router with base path %s", settings.api_base_path)
    return app


app = create_app()
