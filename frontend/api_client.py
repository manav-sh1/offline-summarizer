from __future__ import annotations

import requests

from config import get_settings
from logging_config import get_logger


logger = get_logger(__name__)


class TextForgeApiClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.frontend_api_url.rstrip("/")
        self._timeout = settings.request_timeout_seconds
        logger.info("Initialized API client for %s", self._base_url)

    def health(self) -> dict:
        return self._request("GET", "/health")

    def summarize(self, text: str, length: str, query: str | None) -> dict:
        return self._request(
            "POST",
            "/text/summarize",
            json={"text": text, "length": length, "query": query},
        )

    def keywords(self, text: str, top_k: int) -> dict:
        return self._request("POST", "/text/keywords", json={"text": text, "top_k": top_k})

    def grammar(self, text: str) -> dict:
        return self._request("POST", "/text/grammar", json={"text": text})

    def _request(self, method: str, path: str, json: dict | None = None) -> dict:
        logger.info("Sending %s request to %s", method, path)
        response = requests.request(
            method=method,
            url=f"{self._base_url}{path}",
            json=json,
            timeout=self._timeout,
        )
        response.raise_for_status()
        logger.info("Received successful %s response from %s", method, path)
        return response.json()
