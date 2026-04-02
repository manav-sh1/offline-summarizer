from typing import Literal

from pydantic import BaseModel, Field, field_validator


SummaryLength = Literal["short", "medium", "long"]


class TextPayload(BaseModel):
    text: str = Field(..., min_length=20, max_length=10000, description="Input text to process.")

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Text must not be empty.")
        return normalized


class SummarizeRequest(TextPayload):
    length: SummaryLength = "medium"
    query: str | None = Field(default=None, max_length=300)

    @field_validator("query")
    @classmethod
    def strip_query(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None


class SummarizeResponse(BaseModel):
    summary: str
    provider: str


class KeywordRequest(TextPayload):
    top_k: int = Field(default=8, ge=3, le=20)


class KeywordResponse(BaseModel):
    keywords: list[str]


class GrammarRequest(TextPayload):
    pass


class GrammarSuggestion(BaseModel):
    message: str
    replacements: list[str]
    offset: int
    error_length: int
    context: str


class GrammarResponse(BaseModel):
    issues: list[GrammarSuggestion]
    corrected_text: str
    provider: str


class ParseResponse(BaseModel):
    text: str
    filename: str
    page_count: int | None = None
