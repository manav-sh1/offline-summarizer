from fastapi import APIRouter

from backend.schemas.common import HealthResponse
from logging_config import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    logger.info("Healthcheck requested")
    return HealthResponse(status="ok")
