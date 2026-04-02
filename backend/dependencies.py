from fastapi import Request

from backend.services.grammar import GrammarService
from backend.services.keyword_extractor import KeywordExtractorService
from backend.services.ollama_client import OllamaClient
from backend.services.summarizer import SummarizerService
from backend.services.text_service import TextService
from config import get_settings
from logging_config import get_logger

logger = get_logger(__name__)


def get_text_service(request: Request) -> TextService:
    """Provides a TextService from the application's shared state."""
    # We retrieve the shared TextService from the app state
    # This ensure connection reuse across requests while remaining async-safe.
    return request.app.state.text_service
