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

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_text(
    payload: SummarizeRequest,
    service: TextService = Depends(get_text_service),
) -> SummarizeResponse:
    return service.summarize(payload)


@router.post("/keywords", response_model=KeywordResponse)
def extract_keywords(
    payload: KeywordRequest,
    service: TextService = Depends(get_text_service),
) -> KeywordResponse:
    return service.extract_keywords(payload)


@router.post("/grammar", response_model=GrammarResponse)
def check_grammar(
    payload: GrammarRequest,
    service: TextService = Depends(get_text_service),
) -> GrammarResponse:
    return service.check_grammar(payload)
