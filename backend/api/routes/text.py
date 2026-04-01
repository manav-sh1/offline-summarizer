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
def summarize_text(
    payload: SummarizeRequest,
    service: TextService = Depends(get_text_service),
) -> SummarizeResponse:
    logger.info("Summarize endpoint called with length=%s query_present=%s", payload.length, bool(payload.query))
    return service.summarize(payload)


@router.post("/keywords", response_model=KeywordResponse)
def extract_keywords(
    payload: KeywordRequest,
    service: TextService = Depends(get_text_service),
) -> KeywordResponse:
    logger.info("Keywords endpoint called with top_k=%s", payload.top_k)
    return service.extract_keywords(payload)


@router.post("/grammar", response_model=GrammarResponse)
def check_grammar(
    payload: GrammarRequest,
    service: TextService = Depends(get_text_service),
) -> GrammarResponse:
    logger.info("Grammar endpoint called")
    return service.check_grammar(payload)
