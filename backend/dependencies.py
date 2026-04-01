from functools import lru_cache

from backend.services.grammar import GrammarService
from backend.services.keyword_extractor import KeywordExtractorService
from backend.services.summarizer import SummarizerService
from backend.services.text_service import TextService
from config import get_settings
from logging_config import get_logger


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_text_service() -> TextService:
    settings = get_settings()
    logger.info("Creating cached TextService dependencies")
    return TextService(
        summarizer=SummarizerService(settings),
        keyword_extractor=KeywordExtractorService(settings),
        grammar_checker=GrammarService(settings),
    )
