from backend.schemas.text import (
    GrammarRequest,
    GrammarResponse,
    KeywordRequest,
    KeywordResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from backend.services.grammar import GrammarService
from backend.services.keyword_extractor import KeywordExtractorService
from backend.services.summarizer import SummarizerService
from logging_config import get_logger


logger = get_logger(__name__)


class TextService:
    def __init__(
        self,
        summarizer: SummarizerService,
        keyword_extractor: KeywordExtractorService,
        grammar_checker: GrammarService,
    ) -> None:
        self._summarizer = summarizer
        self._keyword_extractor = keyword_extractor
        self._grammar_checker = grammar_checker

    async def summarize(self, payload: SummarizeRequest) -> SummarizeResponse:
        logger.info("Dispatching summarize request")
        return await self._summarizer.summarize(payload.text, payload.length, payload.query)

    async def extract_keywords(self, payload: KeywordRequest) -> KeywordResponse:
        logger.info("Dispatching keyword extraction request")
        return await self._keyword_extractor.extract(payload.text, payload.top_k)

    async def check_grammar(self, payload: GrammarRequest) -> GrammarResponse:
        logger.info("Dispatching grammar check request")
        return await self._grammar_checker.check(payload.text)
