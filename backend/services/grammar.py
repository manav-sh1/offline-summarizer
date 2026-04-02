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
    """Service for checking grammar and spelling using an LLM backend."""

    def __init__(self, settings: Settings, ollama_client: OllamaClient) -> None:
        self._settings = settings
        self._ollama = ollama_client
        self._model = settings.ollama_grammar_model or settings.ollama_model

    @alru_cache(maxsize=128)
    async def _check_chunk(self, chunk: str) -> dict:
        """Internal method to check an individual chunk with its own cache."""
        try:
            # Escape triple quotes within the chunk to prevent simple prompt injection bypass
            safe_chunk = chunk.replace('"""', '\\"\\"\\"')
            delimited_text = f'"""\n{safe_chunk}\n"""'
            
            prompt = (
                "You are an elite grammar and spell-checking assistant.\n"
                "Analyze the text provided within the triple quotes for grammatical, spelling, and usage errors.\n"
                "Return valid JSON only, using this exact structure:\n"
                "{\n"
                '  "corrected_text": "<fully corrected version of the provided text>",\n'
                '  "issues": [\n'
                '    {\n'
                '      "message": "<description of the error>",\n'
                '      "replacements": ["<suggestion1>", "<suggestion2>"],\n'
                '      "error_text": "<EXACT faulty substring from the original text>",\n'
                '      "context": "<short snippet of the original surrounding text containing the error>"\n'
                '    }\n'
                '  ]\n'
                "}\n"
                "Ensure that 'error_text' appears verbatim in the original text.\n"
                "Do not include conversational preambles or markdown markers.\n"
                f"Source Text:\n{delimited_text}"
            )
            
            raw_response = await self._ollama.generate(prompt, model=self._model)
            return self._ollama.parse_json(raw_response)
        except Exception as exc:
            logger.error("Chunk grammar check failed: %s", exc)
            return {"corrected_text": chunk, "issues": []}

    async def check(self, text: str) -> GrammarResponse:
        """
        Analyzes the text for grammar issues using paragraph-level chunking for efficient caching.
        """
        if not text.strip():
            return GrammarResponse(issues=[], corrected_text=text, provider=f"ollama:{self._model}")

        logger.info("Grammar service invoked (len=%s)", len(text))
        
        # Split text into paragraphs to optimize caching and avoid LLM token limits on large docs
        paragraphs = text.splitlines(keepends=True)
        
        all_issues = []
        all_corrected_chunks = []
        current_offset = 0
        
        for chunk in paragraphs:
            trimmed = chunk.strip()
            if not trimmed:
                all_corrected_chunks.append(chunk)
                current_offset += len(chunk)
                continue

            payload = await self._check_chunk(trimmed)
            
            # Map issues back to their absolute offset in the complete original document
            chunk_raw_issues = payload.get("issues", [])
            for item in chunk_raw_issues:
                issue = self._to_suggestion(chunk, item, base_offset=current_offset)
                if issue:
                    all_issues.append(issue)
            
            # Reconstruct text while preserving original newline structure
            corrected_chunk = payload.get("corrected_text", trimmed)
            suffix = chunk[len(trimmed):]
            all_corrected_chunks.append(corrected_chunk + suffix)
            
            current_offset += len(chunk)

        return GrammarResponse(
            issues=all_issues,
            corrected_text="".join(all_corrected_chunks),
            provider=f"ollama:{self._model}",
        )

    def _to_suggestion(self, source_text: str, item: dict, base_offset: int = 0) -> GrammarSuggestion | None:
        """Parses a raw issue dictionary into a GrammarSuggestion object with improved offset reliability."""
        error_text = str(item.get("error_text", "")).strip()
        context = str(item.get("context", "")).strip()
        if not error_text:
            return None

        # Determine localized offset using context window to avoid false positives with common repeating words.
        start_index = -1
        if context and error_text in context:
            ctx_match = re.search(re.escape(context), source_text)
            if ctx_match:
                rel_match = re.search(re.escape(error_text), context)
                if rel_match:
                    start_index = ctx_match.start() + rel_match.start()
        
        # Fallback to simple search if context is not present or non-matching
        if start_index < 0:
            match = re.search(re.escape(error_text), source_text)
            if match is None:
                return None
            start_index = match.start()

        message = str(item.get("message", "Potential grammar issue")).strip()
        replacements = [str(r).strip() for r in item.get("replacements", []) if str(r).strip()][:5]
        
        display_context = context or source_text[
            max(0, start_index - 30): start_index + len(error_text) + 30
        ]

        return GrammarSuggestion(
            message=message or "Potential grammar issue",
            replacements=replacements,
            offset=base_offset + start_index,
            error_length=len(error_text),
            context=display_context,
        )
