from __future__ import annotations

import re
import httpx
from async_lru import alru_cache

from backend.schemas.text import SummarizeResponse
from backend.services.ollama_client import OllamaClient
from config import Settings
from logging_config import get_logger

logger = get_logger(__name__)


class SummarizerService:
    """Production-level summarizer service with asynchronous support and result caching."""
    
    _sentence_pattern = re.compile(r"(?<=[.!?])\s+")

    def __init__(self, settings: Settings, ollama_client: OllamaClient) -> None:
        self._settings = settings
        self._ollama = ollama_client
        self._model = settings.ollama_summary_model or settings.ollama_model
        self._length_map = {
            "short": "2-3 sentences",
            "medium": "3-5 sentences",
            "long": "5-8 sentences",
        }

    @alru_cache(maxsize=64, ttl=600)
    async def summarize(
        self, text: str, length: str, query: str | None = None
    ) -> SummarizeResponse:
        """
        Summarizes text asynchronously using an LRU cache for repeated requests.
        """
        logger.info(
            "Summarizer service invoked with length=%s query_present=%s",
            length, bool(query)
        )
        try:
            summary = await self._summarize_with_ollama(text, length, query)
            logger.info("Summarizer completed with Ollama model=%s", self._model)
            return SummarizeResponse(summary=summary, provider=f"ollama:{self._model}")
        except (httpx.HTTPError, ValueError) as exc:
            logger.warning("Ollama summarize failed, falling back to extractive: %s", exc)
            return SummarizeResponse(
                summary=self._extractive_summary(text, length),
                provider="extractive-fallback"
            )

    async def _summarize_with_ollama(self, text: str, length: str, query: str | None) -> str:
        """Private method to interface with the Ollama client asynchronously."""
        logger.info("Requesting summary from Ollama")
        prompt = self._build_prompt(text, length, query)
        raw_response = await self._ollama.generate(prompt, model=self._model)
        payload = self._ollama.parse_json(raw_response)
        summary = str(payload.get("summary", "")).strip()
        if not summary:
            raise ValueError("Empty summary from Ollama.")
        return summary

    def _build_prompt(self, text: str, length: str, query: str | None) -> str:
        # Wrap user input in delimiters to mitigate simple prompt injection
        safe_text = text.replace('"""', '\\"\\"\\"')
        safe_query = query.replace('"""', '\\"\\"\\"') if query else ""
        delimited_text = f"\"\"\"\n{safe_text}\n\"\"\""
        focus = f"Focus specifically on the query: {safe_query}\n" if query else ""
        return (
            "You are a concise offline summarization assistant.\n"
            "Summarize the text delimited by triple quotes.\n"
            "Return strict JSON with this exact shape: "
            '{"summary": "<text>"}.\n'
            f"Write a {self._length_map[length]} summary.\n"
            "Preserve factual meaning and avoid fluff.\n"
            f"{focus}"
            f"Text:\n{delimited_text}"
        )

    def _extractive_summary(self, text: str, length: str) -> str:
        """Deterministic fallback for summarize when the LLM is unreachable."""
        logger.info("Generating extractive fallback summary")
        sentences = [
            part.strip() 
            for part in self._sentence_pattern.split(text.strip()) 
            if part.strip()
        ]
        sentence_count = {"short": 2, "medium": 4, "long": 6}[length]
        return " ".join(sentences[:sentence_count]) if sentences else text.strip()
