from __future__ import annotations

import requests

from backend.schemas.text import KeywordResponse
from backend.services.ollama_client import OllamaClient
from config import Settings


class KeywordExtractorService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ollama = OllamaClient(settings)

    def extract(self, text: str, top_k: int) -> KeywordResponse:
        keyword_limit = min(top_k, self._settings.max_keywords)
        try:
            payload = self._ollama.parse_json(self._ollama.generate(self._build_prompt(text, keyword_limit)))
            keywords = [
                str(keyword).strip()
                for keyword in payload.get("keywords", [])
                if str(keyword).strip()
            ][:keyword_limit]
            return KeywordResponse(keywords=keywords)
        except (requests.RequestException, ValueError, TypeError):
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
