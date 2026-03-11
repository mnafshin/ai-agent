"""
Local / Self-hosted LLM provider.

Connects to any OpenAI-compatible local server. Works with:
  - Ollama          (http://localhost:11434/v1)
  - LM Studio       (http://localhost:1234/v1)
  - vLLM             (http://localhost:8000/v1)
  - llama.cpp server (http://localhost:8080/v1)
  - LocalAI          (http://localhost:8080/v1)
  - text-gen-webui   (http://localhost:5000/v1)
  - DeepSeek local   (http://localhost:8000/v1)
  - Any other OpenAI-compatible endpoint

Data stays 100% on your machine. No external API calls.

Env vars:
  LOCAL_LLM_URL      (required — base URL, e.g. http://localhost:11434/v1)
  LOCAL_LLM_KEY      (optional — API key if your server requires one, default: "none")
  LOCAL_LLM_MODELS   (optional — comma-separated model names to expose,
                       e.g. "deepseek-coder-v2:latest,llama3.1:70b,codestral:latest"
                       If not set, the provider will try to auto-discover models
                       from the server's /models endpoint)
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

# Well-known local model presets (family + tier guesses based on name)
_FAMILY_HINTS = {
    "deepseek":   "deepseek",
    "codestral":  "mistral",
    "mistral":    "mistral",
    "llama":      "llama",
    "phi":        "phi",
    "gemma":      "gemma",
    "qwen":       "qwen",
    "starcoder":  "starcoder",
    "codellama":  "llama",
    "wizard":     "wizard",
    "yi":         "yi",
    "command":    "cohere",
    "mixtral":    "mistral",
    "nous":       "nous",
}

_TIER_HINTS = {
    # Size-based tier guesses
    "405b": "powerful", "236b": "powerful", "180b": "powerful",
    "120b": "powerful", "70b":  "powerful",
    "34b":  "balanced", "33b":  "balanced",  "32b": "balanced",
    "27b":  "balanced", "22b":  "balanced",  "14b": "balanced",
    "13b":  "balanced", "8b":   "balanced",  "7b":  "balanced",
    "3b":   "fast",     "2b":   "fast",      "1b":  "fast",
    "1.5b": "fast",     "0.5b": "fast",
    # Name-based
    "coder": "balanced",
    "chat":  "balanced",
    "instruct": "balanced",
}


def _guess_model_info(model_name: str) -> ModelInfo:
    """Build a ModelInfo from a local model name with best-effort guesses."""
    name_lower = model_name.lower()

    # Guess family
    family = "local"
    for hint, fam in _FAMILY_HINTS.items():
        if hint in name_lower:
            family = fam
            break

    # Guess tier
    tier = "balanced"
    for hint, t in _TIER_HINTS.items():
        if hint in name_lower:
            tier = t
            break

    display = model_name.split("/")[-1].split(":")[0]  # strip repo prefix / tag
    return ModelInfo(
        model_id=model_name,
        family=family,
        tier=tier,
        provider_name="local",
        display_name=f"{display} (local)",
    )


class LocalProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "local"

    def _url(self) -> str | None:
        return os.getenv("LOCAL_LLM_URL")

    def _key(self) -> str:
        return os.getenv("LOCAL_LLM_KEY", "none")

    def is_available(self) -> bool:
        return _SDK_AVAILABLE and bool(self._url())

    def models(self) -> list[ModelInfo]:
        """
        Return the list of models this provider can serve.

        Priority:
          1. LOCAL_LLM_MODELS env var (explicit list)
          2. Auto-discover from the server's /models endpoint
          3. Fallback to a generic "local-model" entry
        """
        explicit = os.getenv("LOCAL_LLM_MODELS", "").strip()
        if explicit:
            return [_guess_model_info(m.strip()) for m in explicit.split(",") if m.strip()]

        # Try auto-discovery
        discovered = self._discover_models()
        if discovered:
            return discovered

        # Fallback
        return [ModelInfo("local-model", "local", "balanced", "local", "Local Model")]

    def _discover_models(self) -> list[ModelInfo]:
        """Try to list models from the server's /models endpoint."""
        if not self.is_available():
            return []
        try:
            client = OpenAI(api_key=self._key(), base_url=self._url())
            response = client.models.list()
            return [_guess_model_info(m.id) for m in response.data]
        except Exception:
            return []

    def status_line(self) -> str:
        if not _SDK_AVAILABLE:
            return "openai SDK not installed"
        url = self._url()
        if not url:
            return "no LOCAL_LLM_URL set"
        model_count = len(self.models())
        return f"{url} ({model_count} model{'s' if model_count != 1 else ''} available)"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = OpenAI(api_key=self._key(), base_url=self._url())
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

