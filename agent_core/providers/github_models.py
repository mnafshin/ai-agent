"""
GitHub Models API provider.

Uses a GitHub PAT to access models.inference.ai.azure.com.
Available models: GPT-4o, GPT-4o-mini, Llama-3, Mistral, etc.
No Claude models available through this endpoint.

Env vars:
  GITHUB_TOKEN  or  GITHUB_COPILOT_TOKEN
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

BASE_URL = "https://models.inference.ai.azure.com"

# Models confirmed available on GitHub Models API
_MODELS = [
    ModelInfo("gpt-4o",                         "gpt",     "balanced",  "github_models", "GPT-4o"),
    ModelInfo("gpt-4o-mini",                     "gpt",     "fast",      "github_models", "GPT-4o mini"),
    ModelInfo("Meta-Llama-3.1-405B-Instruct",    "llama",   "powerful",  "github_models", "Llama 3.1 405B"),
    ModelInfo("Meta-Llama-3.1-70B-Instruct",     "llama",   "balanced",  "github_models", "Llama 3.1 70B"),
    ModelInfo("Meta-Llama-3.1-8B-Instruct",      "llama",   "fast",      "github_models", "Llama 3.1 8B"),
    ModelInfo("Mistral-large-2407",              "mistral", "balanced",  "github_models", "Mistral Large"),
    ModelInfo("Mistral-Nemo",                    "mistral", "fast",      "github_models", "Mistral Nemo"),
    ModelInfo("AI21-Jamba-Instruct",             "other",   "balanced",  "github_models", "AI21 Jamba"),
]


class GitHubModelsProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "github_models"

    def _token(self) -> str | None:
        return os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_COPILOT_TOKEN")

    def is_available(self) -> bool:
        return _SDK_AVAILABLE and bool(self._token())

    def models(self) -> list[ModelInfo]:
        return list(_MODELS)

    def status_line(self) -> str:
        if not _SDK_AVAILABLE:
            return "openai SDK not installed"
        if not self._token():
            return "no GITHUB_TOKEN set"
        src = "GITHUB_TOKEN" if os.getenv("GITHUB_TOKEN") else "GITHUB_COPILOT_TOKEN"
        return f"{src} → models.inference.ai.azure.com"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = OpenAI(api_key=self._token(), base_url=BASE_URL)
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

