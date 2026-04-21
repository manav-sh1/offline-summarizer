from __future__ import annotations

import httpx
from fastapi import APIRouter, Request

from backend.schemas.common import HealthResponse
from config import get_settings
from logging_config import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def healthcheck(request: Request) -> HealthResponse:
    """Verifies backend liveness AND Ollama connectivity."""
    settings = get_settings()
    client: httpx.AsyncClient = request.app.state.http_client

    try:
        resp = await client.get(
            f"{settings.ollama_base_url}/api/tags",
            timeout=5,
        )
        resp.raise_for_status()
        logger.info("Healthcheck passed — Ollama reachable")
        return HealthResponse(status="ok")
    except httpx.HTTPError as exc:
        logger.warning("Healthcheck degraded — Ollama unreachable: %s", exc)
        return HealthResponse(status="degraded")
