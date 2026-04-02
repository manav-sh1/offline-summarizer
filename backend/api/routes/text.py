from fastapi import APIRouter, Depends

from backend.dependencies import get_text_service
from backend.schemas.text import (
    GrammarRequest,
    GrammarResponse,
    KeywordRequest,
    KeywordResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from backend.services.text_service import TextService
from logging_config import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(
    payload: SummarizeRequest,
    service: TextService = Depends(get_text_service),
) -> SummarizeResponse:
    logger.info(
        "Summarize endpoint: length=%s queries=%s", 
        payload.length, bool(payload.query)
    )
    return await service.summarize(payload)


@router.post("/keywords", response_model=KeywordResponse)
async def extract_keywords(
    payload: KeywordRequest,
    service: TextService = Depends(get_text_service),
) -> KeywordResponse:
    logger.info("Keywords endpoint called with top_k=%s", payload.top_k)
    return await service.extract_keywords(payload)


@router.post("/grammar", response_model=GrammarResponse)
async def check_grammar(
    payload: GrammarRequest,
    service: TextService = Depends(get_text_service),
) -> GrammarResponse:
    logger.info("Grammar endpoint called")
    return await service.check_grammar(payload)
