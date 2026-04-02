from __future__ import annotations

import re
import httpx
from async_lru import alru_cache

from backend.schemas.text import GrammarResponse, GrammarSuggestion
from backend.services.ollama_client import OllamaClient
from config import Settings
from logging_config import get_logger

logger = get_logger(__name__)


class GrammarService:
    def __init__(self, settings: Settings, ollama_client: OllamaClient) -> None:
        self._settings = settings
        self._ollama = ollama_client
        self._model = settings.ollama_grammar_model or settings.ollama_model

    @alru_cache(maxsize=128)
    async def check(self, text: str) -> GrammarResponse:
        logger.info("Grammar service invoked with text length=%s", len(text))
        try:
            raw_response = await self._ollama.generate(self._build_prompt(text), model=self._model)
            payload = self._ollama.parse_json(raw_response)
            
            # Extract and filter individual issues
            raw_issues = payload.get("issues", [])
            issues = [issue for item in raw_issues if (issue := self._to_suggestion(text, item)) is not None]
            
            # Extract fully corrected text, fallback to original if missing
            corrected_text = str(payload.get("corrected_text", text)).strip()
            
            logger.info("Grammar check completed with %s issues highlighted", len(issues))
            return GrammarResponse(
                issues=issues,
                corrected_text=corrected_text or text,
                provider=f"ollama:{self._model}",
            )
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as exc:
            logger.warning("Grammar check failed, returning original text as fallback: %s", exc)
            return GrammarResponse(issues=[], corrected_text=text, provider="unavailable")

    def _build_prompt(self, text: str) -> str:
        return (
            "You are a grammar and spell-checking assistant.\n"
            "Analyze the provided text for errors and provide a fully corrected version.\n"
            "Return strict JSON with this shape:\n"
            "{\n"
            '  "corrected_text": "<fully_corrected_para>",\n'
            '  "issues": [{\n'
            '    "message": "<short_description_of_error>",\n'
            '    "replacements": ["<suggestion1>", "<suggestion2>"],\n'
            '    "error_text": "<exact_original_error_from_text>",\n'
            '    "context": "<short_snippet_with_error>"\n'
            '  }]\n'
            "}\n"
            "Only include real grammar, spelling, punctuation, or usage issues.\n"
            "Ensure the corrected_text is consistent with the suggestions in the issues array.\n"
            f"Text:\n{text}"
        )

    def _to_suggestion(self, source_text: str, item: dict) -> GrammarSuggestion | None:
        error_text = str(item.get("error_text", "")).strip()
        if not error_text:
            logger.debug("Skipping grammar issue without error_text")
            return None

        match = re.search(re.escape(error_text), source_text)
        if match is None:
            logger.debug("Skipping grammar issue because source match was not found")
            return None

        message = str(item.get("message", "Potential grammar issue")).strip() or "Potential grammar issue"
        replacements = [str(value).strip() for value in item.get("replacements", []) if str(value).strip()][:5]
        context = str(item.get("context", "")).strip() or source_text[max(0, match.start() - 20): match.end() + 20]
        return GrammarSuggestion(
            message=message,
            replacements=replacements,
            offset=match.start(),
            error_length=len(error_text),
            context=context,
        )
