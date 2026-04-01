from __future__ import annotations

import json

import requests

from config import Settings
from logging_config import get_logger


logger = get_logger(__name__)


class OllamaClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def generate(self, prompt: str, model: str | None = None) -> str:
        resolved_model = model or self._settings.ollama_model
        logger.info("Sending generation request to Ollama model=%s", resolved_model)
        response = requests.post(
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
            raise requests.RequestException("Empty response from Ollama.")
        logger.info("Received generation response from Ollama model=%s", resolved_model)
        return generated

    @staticmethod
    def parse_json(content: str) -> dict:
        logger.info("Parsing Ollama JSON response")
        return json.loads(content)
