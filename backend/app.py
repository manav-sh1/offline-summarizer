from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx
from fastapi import FastAPI, Request, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from backend.api.router import api_router
from config import get_settings
from logging_config import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Manages the application lifecycle: startup and shutdown."""
    logger.info("Initializing application resources")
    settings = get_settings()
    
    # Initialize a shared AsyncClient for entire app lifecycle.
    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        
        # Initialize Core Services as singletons
        from backend.services.ollama_client import OllamaClient
        from backend.services.summarizer import SummarizerService
        from backend.services.grammar import GrammarService
        from backend.services.keyword_extractor import KeywordExtractorService
        from backend.services.text_service import TextService
        
        ollama_client = OllamaClient(settings, client)
        app.state.text_service = TextService(
            summarizer=SummarizerService(settings, ollama_client),
            keyword_extractor=KeywordExtractorService(settings, ollama_client),
            grammar_checker=GrammarService(settings, ollama_client),
        )
        
        yield
    
    logger.info("Shutting down application resources")


def create_app() -> FastAPI:
    """Production-level FastAPI application factory."""
    settings = get_settings()
    logger.info("Creating production FastAPI application for %s", settings.app_name)
    
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Register global exception handlers for production-safe error surfacing.
    @app.exception_handler(httpx.HTTPError)
    async def httpx_exception_handler(request: Request, exc: httpx.HTTPError):
        logger.error("External connection failure: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "Offline provider is currently unreachable."},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.error("Data validation/parsing error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": str(exc)},
        )

    # Performance Optimization: Compress responses larger than 1000 bytes
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Register internal API routes
    app.include_router(api_router, prefix=settings.api_base_path)
    
    logger.info("Application initialized with base path %s", settings.api_base_path)
    return app


app = create_app()
