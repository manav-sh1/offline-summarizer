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
    """Provides a TextService with access to the application's shared HTTP client."""
    settings = get_settings()
    
    # We retrieve the shared httpx.AsyncClient from the app state
    # This ensures connection reuse across requests while remaining async-safe.
    http_client = request.app.state.http_client
    ollama_client = OllamaClient(settings, http_client)
    
    return TextService(
        summarizer=SummarizerService(settings, ollama_client),
        keyword_extractor=KeywordExtractorService(settings, ollama_client),
        grammar_checker=GrammarService(settings, ollama_client),
    )
