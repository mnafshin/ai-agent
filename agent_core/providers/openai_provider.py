"""
Direct OpenAI API provider.

Uses OPENAI_KEY to call api.openai.com directly.

Env vars:
  OPENAI_KEY
"""

from __future__ import annotations
import os

from .base import LLMProvider, ModelInfo

_SDK_AVAILABLE = False
try:
    from openai import OpenAI
    _SDK_AVAILABLE = True
except ImportError:
    pass

_MODELS = [
    ModelInfo("gpt-4o",         "gpt", "balanced",  "openai", "GPT-4o"),
    ModelInfo("gpt-4o-mini",    "gpt", "fast",      "openai", "GPT-4o mini"),
    ModelInfo("gpt-4-turbo",    "gpt", "balanced",  "openai", "GPT-4 Turbo"),
    ModelInfo("o1",             "gpt", "powerful",   "openai", "o1"),
    ModelInfo("o1-mini",        "gpt", "balanced",   "openai", "o1 mini"),
    ModelInfo("o3-mini",        "gpt", "fast",       "openai", "o3 mini"),
]


class OpenAIProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "openai"

    def _key(self) -> str | None:
        return os.getenv("OPENAI_KEY")

    def is_available(self) -> bool:
        return _SDK_AVAILABLE and bool(self._key())

    def models(self) -> list[ModelInfo]:
        return list(_MODELS)

    def status_line(self) -> str:
        if not _SDK_AVAILABLE:
            return "openai SDK not installed"
        if not self._key():
            return "no OPENAI_KEY set"
        return "OPENAI_KEY → api.openai.com"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = OpenAI(api_key=self._key())
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

