from __future__ import annotations

import json

import requests

from config import Settings


class OllamaClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def generate(self, prompt: str, model: str | None = None) -> str:
        response = requests.post(
            f"{self._settings.ollama_base_url}/api/generate",
            json={
                "model": model or self._settings.ollama_model,
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
        return generated

    @staticmethod
    def parse_json(content: str) -> dict:
        return json.loads(content)
