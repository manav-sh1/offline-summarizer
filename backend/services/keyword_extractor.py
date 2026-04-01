from __future__ import annotations

import requests

from backend.schemas.text import KeywordResponse
from backend.services.ollama_client import OllamaClient
from config import Settings
from logging_config import get_logger


logger = get_logger(__name__)


class KeywordExtractorService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ollama = OllamaClient(settings)
        self._model = settings.ollama_keywords_model or settings.ollama_model

    def extract(self, text: str, top_k: int) -> KeywordResponse:
        keyword_limit = min(top_k, self._settings.max_keywords)
        logger.info("Keyword extractor invoked with requested_top_k=%s effective_top_k=%s", top_k, keyword_limit)
        try:
            payload = self._ollama.parse_json(
                self._ollama.generate(self._build_prompt(text, keyword_limit), model=self._model)
            )
            keywords = [
                str(keyword).strip()
                for keyword in payload.get("keywords", [])
                if str(keyword).strip()
            ][:keyword_limit]
            logger.info("Keyword extractor completed with %s keywords", len(keywords))
            return KeywordResponse(keywords=keywords)
        except (requests.RequestException, ValueError, TypeError) as exc:
            logger.warning("Keyword extraction failed, returning empty result: %s", exc)
            return KeywordResponse(keywords=[])

    def _build_prompt(self, text: str, top_k: int) -> str:
        return (
            "You are a keyword extraction assistant.\n"
            'Return strict JSON with this shape: {"keywords":["keyword1","keyword2"]}.\n'
            f"Extract the top {top_k} most important keywords or short keyphrases.\n"
            "Prefer meaningful concepts over filler words.\n"
            "Do not include duplicates.\n"
            f"Text:\n{text}"
        )
