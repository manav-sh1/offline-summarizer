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

    def summarize(self, payload: SummarizeRequest) -> SummarizeResponse:
        return self._summarizer.summarize(payload.text, payload.length, payload.query)

    def extract_keywords(self, payload: KeywordRequest) -> KeywordResponse:
        return self._keyword_extractor.extract(payload.text, payload.top_k)

    def check_grammar(self, payload: GrammarRequest) -> GrammarResponse:
        return self._grammar_checker.check(payload.text)
