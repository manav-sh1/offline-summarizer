from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TextForge"
    app_env: str = Field(default="development", alias="APP_ENV")
    api_host: str = Field(default="127.0.0.1", alias="API_HOST")
    api_port: int = Field(default=5000, alias="API_PORT")
    api_base_path: str = Field(default="/api/v1", alias="API_BASE_PATH")
    ollama_base_url: str = Field(
        default="http://127.0.0.1:11434", alias="OLLAMA_BASE_URL"
    )
    ollama_model: str = Field(default="qwen2.5:1.5b", alias="OLLAMA_MODEL")
    ollama_summary_model: str | None = Field(
        default=None, alias="OLLAMA_SUMMARY_MODEL"
    )
    ollama_keywords_model: str | None = Field(
        default=None, alias="OLLAMA_KEYWORDS_MODEL"
    )
    ollama_grammar_model: str | None = Field(
        default=None, alias="OLLAMA_GRAMMAR_MODEL"
    )
    ollama_timeout_seconds: int = Field(
        default=90, alias="OLLAMA_TIMEOUT_SECONDS"
    )
    frontend_api_url: str = Field(
        default="http://127.0.0.1:5000/api/v1", alias="FRONTEND_API_URL"
    )
    request_timeout_seconds: int = Field(default=120, alias="REQUEST_TIMEOUT_SECONDS")
    max_keywords: int = Field(default=10, alias="MAX_KEYWORDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
