from __future__ import annotations

import re
from collections import Counter

from backend.schemas.text import KeywordResponse
from config import Settings

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


class KeywordExtractorService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def extract(self, text: str, top_k: int) -> KeywordResponse:
        words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b", text.lower())
        filtered = [word for word in words if word not in STOP_WORDS]
        keyword_limit = min(top_k, self._settings.max_keywords)
        keywords = [word for word, _ in Counter(filtered).most_common(keyword_limit)]
        return KeywordResponse(keywords=keywords)
