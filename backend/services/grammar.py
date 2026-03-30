from __future__ import annotations

from functools import lru_cache

try:
    import language_tool_python
except ImportError:  # pragma: no cover
    language_tool_python = None

from backend.schemas.text import GrammarResponse, GrammarSuggestion
from config import Settings


class GrammarService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @lru_cache(maxsize=1)
    def _client(self) -> "language_tool_python.LanguageTool | None":
        if language_tool_python is None:
            return None
        return language_tool_python.LanguageTool(self._settings.grammar_language)

    def check(self, text: str) -> GrammarResponse:
        client = self._client()
        if client is None:
            return GrammarResponse(issues=[], provider="unavailable")

        try:
            matches = client.check(text)
        except Exception:
            return GrammarResponse(issues=[], provider="unavailable")

        issues = [
            GrammarSuggestion(
                message=match.message,
                replacements=list(match.replacements[:5]),
                offset=match.offset,
                error_length=match.errorLength,
                context=match.context,
            )
            for match in matches
        ]
        return GrammarResponse(issues=issues, provider="language-tool")
