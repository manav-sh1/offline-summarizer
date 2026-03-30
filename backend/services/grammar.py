from __future__ import annotations

import re

import requests

from backend.schemas.text import GrammarResponse, GrammarSuggestion
from backend.services.ollama_client import OllamaClient
from config import Settings


class GrammarService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ollama = OllamaClient(settings)

    def check(self, text: str) -> GrammarResponse:
        try:
            payload = self._ollama.parse_json(self._ollama.generate(self._build_prompt(text)))
            raw_issues = payload.get("issues", [])
            issues = [self._to_suggestion(text, item) for item in raw_issues]
            return GrammarResponse(
                issues=[issue for issue in issues if issue is not None],
                provider=f"ollama:{self._settings.ollama_model}",
            )
        except (requests.RequestException, ValueError, TypeError, KeyError):
            return GrammarResponse(issues=[], provider="unavailable")

    def _build_prompt(self, text: str) -> str:
        return (
            "You are a grammar analysis assistant.\n"
            "Return strict JSON with this shape: "
            '{"issues":[{"message":"...",'
            '"replacements":["..."],'
            '"error_text":"...",'
            '"context":"..."}]}.\n'
            "Only include real grammar, spelling, punctuation, or usage issues.\n"
            "Use short messages and up to 5 replacements per issue.\n"
            f"Text:\n{text}"
        )

    def _to_suggestion(self, source_text: str, item: dict) -> GrammarSuggestion | None:
        error_text = str(item.get("error_text", "")).strip()
        if not error_text:
            return None

        match = re.search(re.escape(error_text), source_text)
        if match is None:
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
