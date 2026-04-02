from __future__ import annotations

import json
from json import JSONDecodeError

import httpx

from config import Settings
from logging_config import get_logger

logger = get_logger(__name__)


class OllamaClient:
    def __init__(self, settings: Settings, client: httpx.AsyncClient) -> None:
        self._settings = settings
        self._client = client

    async def generate(self, prompt: str, model: str | None = None) -> str:
        resolved_model = model or self._settings.ollama_model
        logger.info("Sending generation request to Ollama model=%s", resolved_model)
        
        try:
            response = await self._client.post(
                f"{self._settings.ollama_base_url}/api/generate",
                json={
                    "model": resolved_model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=self._settings.ollama_timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
            generated = payload.get("response", "").strip()
            
            if not generated:
                raise httpx.HTTPError("Empty response from Ollama.")
            
            logger.info("Received generation response from Ollama model=%s", resolved_model)
            return generated
        except httpx.HTTPError as exc:
            logger.error("HTTP error occurred while calling Ollama: %s", exc)
            raise

    @staticmethod
    def parse_json(content: str) -> dict:
        try:
            logger.info("Parsing Ollama JSON response")
            return json.loads(content)
        except JSONDecodeError as exc:
            logger.error("Failed to parse JSON content from Ollama: %s", exc)
            raise ValueError(f"Invalid JSON from Ollama: {exc}")
