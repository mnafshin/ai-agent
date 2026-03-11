"""
Base classes for the LLM provider abstraction.

Uses the Strategy pattern:
  - LLMProvider    — abstract interface for all providers
  - ProviderRegistry — discovers & initialises available providers from env
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelInfo:
    """Metadata about a model offered by a provider."""
    model_id: str           # ID sent to the API  (e.g. "claude-3-5-sonnet-20241022")
    family: str             # "claude" | "gpt" | "llama" | "mistral" | "gemini"
    tier: str               # "fast" | "balanced" | "powerful"
    provider_name: str      # which provider serves this model
    display_name: str = ""  # human-readable name


class LLMProvider(ABC):
    """
    Abstract base for every LLM backend.

    Each concrete provider must implement:
      - name            → short identifier  ("anthropic", "bedrock", …)
      - is_available()  → can this provider be used right now?
      - models()        → list of ModelInfo it can serve
      - call()          → execute a chat completion
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier for this provider (used in config & logs)."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if credentials and SDKs are ready."""

    @abstractmethod
    def models(self) -> list[ModelInfo]:
        """Return the list of models this provider can serve."""

    @abstractmethod
    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Execute a chat completion and return the response text."""

    @abstractmethod
    def status_line(self) -> str:
        """One-line human-readable auth/status string for dashboards."""

    def supports_model(self, model_id: str) -> bool:
        """Check if this provider can serve a given model_id."""
        return any(m.model_id == model_id for m in self.models())


class ProviderRegistry:
    """
    Discovers, initialises, and indexes all available LLM providers.

    Resolution order for a model request:
      1. If the user set LLM_PROVIDER env var → use that provider exclusively
      2. Otherwise, pick the first available provider that serves the model
         (ordered by priority: anthropic > bedrock > vertex > openai > github_models)
    """

    # Default priority order — higher-fidelity providers first.
    # "local" is placed before github_models so that when both are available
    # and the user has a powerful local model, it takes precedence over the
    # free but rate-limited GitHub Models API.
    PRIORITY = ["anthropic", "bedrock", "vertex", "openai", "local", "github_models"]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._providers: dict[str, LLMProvider] = {}
        self._forced_provider: Optional[str] = None
        self._auth_report: list[str] = []

        self._discover()

    # ── Discovery ─────────────────────────────────────────────────────────────

    def _discover(self):
        """Instantiate every provider class and keep those that are available."""
        from .github_models import GitHubModelsProvider
        from .anthropic_provider import AnthropicProvider
        from .openai_provider import OpenAIProvider
        from .bedrock_provider import BedrockProvider
        from .vertex_provider import VertexProvider
        from .local_provider import LocalProvider

        all_providers: list[LLMProvider] = [
            AnthropicProvider(),
            BedrockProvider(),
            VertexProvider(),
            OpenAIProvider(),
            LocalProvider(),
            GitHubModelsProvider(),
        ]

        for p in all_providers:
            if p.is_available():
                self._providers[p.name] = p
                self._auth_report.append(f"  ✅ {p.name:<16} {p.status_line()}")
            else:
                self._auth_report.append(f"  ── {p.name:<16} {p.status_line()}")

        # User can force a specific provider via LLM_PROVIDER env var
        forced = os.getenv("LLM_PROVIDER", "").strip().lower()
        if forced:
            if forced in self._providers:
                self._forced_provider = forced
                self._auth_report.append(f"  🔒 LLM_PROVIDER={forced} (forced)")
            else:
                self._auth_report.append(
                    f"  ⚠️  LLM_PROVIDER={forced} requested but not available"
                )

        if self.verbose:
            print("🔑 Provider registry:")
            for line in self._auth_report:
                print(line)

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def auth_report(self) -> list[str]:
        return list(self._auth_report)

    @property
    def available_providers(self) -> dict[str, LLMProvider]:
        return dict(self._providers)

    def resolve(self, model_id: str) -> tuple[LLMProvider, str]:
        """
        Find the best provider for a model_id.

        Returns (provider, actual_model_id).
        Raises RuntimeError if no provider can serve the model.
        """
        # Forced provider
        if self._forced_provider:
            p = self._providers[self._forced_provider]
            if p.supports_model(model_id):
                return p, model_id
            # The forced provider doesn't have this exact model —
            # try to find a compatible one in the same family
            return p, self._find_compatible(p, model_id)

        # Priority-based resolution
        for name in self.PRIORITY:
            if name in self._providers:
                p = self._providers[name]
                if p.supports_model(model_id):
                    return p, model_id

        # Fallback: find ANY provider with a compatible model
        for name in self.PRIORITY:
            if name in self._providers:
                p = self._providers[name]
                try:
                    alt = self._find_compatible(p, model_id)
                    return p, alt
                except RuntimeError:
                    continue

        available = ", ".join(self._providers.keys()) or "none"
        raise RuntimeError(
            f"❌ No provider can serve model '{model_id}'.\n"
            f"   Available providers: {available}\n"
            f"   Set LLM_PROVIDER or add credentials for a compatible provider."
        )

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Resolve provider and call the model."""
        provider, actual_model = self.resolve(model_id)
        return provider.call(actual_model, messages, max_tokens, temperature)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _find_compatible(provider: LLMProvider, model_id: str) -> str:
        """
        Find a model in `provider` that's compatible with the requested one.

        Compatibility means: same family (claude→claude, gpt→gpt) and
        closest tier match.
        """
        # Determine the family of the requested model
        family = _guess_family(model_id)
        tier   = _guess_tier(model_id)

        candidates = [m for m in provider.models() if m.family == family]
        if not candidates:
            # Cross-family fallback: if asked for claude but only gpt available
            candidates = [m for m in provider.models() if m.tier == tier]
        if not candidates:
            candidates = provider.models()
        if not candidates:
            raise RuntimeError(f"Provider {provider.name} has no models")

        # Prefer same tier, else highest tier
        tier_prio = {"powerful": 0, "balanced": 1, "fast": 2}
        candidates.sort(key=lambda m: abs(tier_prio.get(m.tier, 9) - tier_prio.get(tier, 1)))
        return candidates[0].model_id


# ── Module-level helpers ──────────────────────────────────────────────────────

def _guess_family(model_id: str) -> str:
    """Guess model family from its ID string."""
    mid = model_id.lower()
    if "claude" in mid:
        return "claude"
    if "gpt" in mid or "o1" in mid or "o3" in mid:
        return "gpt"
    if "llama" in mid:
        return "llama"
    if "mistral" in mid:
        return "mistral"
    if "gemini" in mid:
        return "gemini"
    return "unknown"


def _guess_tier(model_id: str) -> str:
    """Guess model tier from its ID string."""
    mid = model_id.lower()
    if any(k in mid for k in ("haiku", "mini", "fast", "flash")):
        return "fast"
    if any(k in mid for k in ("opus", "405b", "large", "o1", "o3")):
        return "powerful"
    return "balanced"

