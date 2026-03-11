"""
Direct Anthropic API provider.

Uses ANTHROPIC_KEY to call api.anthropic.com directly.

Env vars:
  ANTHROPIC_KEY
"""

from __future__ import annotations
import os

from .base import LLMProvider, ModelInfo

_SDK_AVAILABLE = False
try:
    from anthropic import Anthropic
    _SDK_AVAILABLE = True
except ImportError:
    pass

_MODELS = [
    ModelInfo("claude-3-5-haiku-20241022",    "claude", "fast",      "anthropic", "Claude 3.5 Haiku"),
    ModelInfo("claude-3-5-sonnet-20241022",   "claude", "balanced",  "anthropic", "Claude 3.5 Sonnet"),
    ModelInfo("claude-3-opus-20240229",       "claude", "powerful",  "anthropic", "Claude 3 Opus"),
]


class AnthropicProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "anthropic"

    def _key(self) -> str | None:
        return os.getenv("ANTHROPIC_KEY")

    def is_available(self) -> bool:
        return _SDK_AVAILABLE and bool(self._key())

    def models(self) -> list[ModelInfo]:
        return list(_MODELS)

    def status_line(self) -> str:
        if not _SDK_AVAILABLE:
            return "anthropic SDK not installed"
        if not self._key():
            return "no ANTHROPIC_KEY set"
        return "ANTHROPIC_KEY → api.anthropic.com"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = Anthropic(api_key=self._key())
        response = client.messages.create(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return response.content[0].text

