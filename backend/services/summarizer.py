from __future__ import annotations

import re

import requests

from backend.schemas.text import SummarizeResponse
from backend.services.ollama_client import OllamaClient
from config import Settings


class SummarizerService:
    _sentence_pattern = re.compile(r"(?<=[.!?])\s+")

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ollama = OllamaClient(settings)
        self._length_map = {
            "short": "2-3 sentences",
            "medium": "3-5 sentences",
            "long": "5-8 sentences",
        }

    def summarize(self, text: str, length: str, query: str | None = None) -> SummarizeResponse:
        try:
            summary = self._summarize_with_ollama(text, length, query)
            return SummarizeResponse(summary=summary, provider=f"ollama:{self._settings.ollama_model}")
        except requests.RequestException:
            return SummarizeResponse(summary=self._extractive_summary(text, length), provider="extractive-fallback")

    def _summarize_with_ollama(self, text: str, length: str, query: str | None) -> str:
        prompt = self._build_prompt(text, length, query)
        payload = self._ollama.parse_json(self._ollama.generate(prompt))
        summary = str(payload.get("summary", "")).strip()
        if not summary:
            raise requests.RequestException("Empty summary from Ollama.")
        return summary

    def _build_prompt(self, text: str, length: str, query: str | None) -> str:
        focus = f"Focus specifically on: {query}\n" if query else ""
        return (
            "You are a concise offline summarization assistant.\n"
            "Return strict JSON with this shape: "
            '{"summary": "<text>"}.\n'
            f"Write a {self._length_map[length]} summary.\n"
            "Preserve factual meaning and avoid fluff.\n"
            f"{focus}"
            "Text:\n"
            f"{text}"
        )

    def _extractive_summary(self, text: str, length: str) -> str:
        sentences = [part.strip() for part in self._sentence_pattern.split(text.strip()) if part.strip()]
        sentence_count = {"short": 2, "medium": 4, "long": 6}[length]
        return " ".join(sentences[:sentence_count]) if sentences else text.strip()
