#!/usr/bin/env python3
"""
ModelRouter — central auth & model dispatch for all 20 agent skills.

Supports multiple LLM backends via the Strategy pattern:

  Provider          | Env var needed            | Claude? | GPT? | Data location
  ──────────────────|───────────────────────────|─────────|──────|──────────────
  github_models     | GITHUB_TOKEN              | ❌      | ✅   | Microsoft
  anthropic         | ANTHROPIC_KEY             | ✅      | ❌   | Anthropic
  openai            | OPENAI_KEY                | ❌      | ✅   | OpenAI
  bedrock           | AWS_ACCESS_KEY_ID + region| ✅      | ❌   | Your AWS
  vertex            | GOOGLE_CLOUD_PROJECT      | ✅      | ✅*  | Your GCP
  local             | LOCAL_LLM_URL             | ❌**    | ❌** | Your machine

  *  Vertex also offers Gemini models.
  ** Local serves whatever models your server has (DeepSeek, Llama, Mistral, etc.)

Resolution order (automatic):
  1. If LLM_PROVIDER is set → use that provider exclusively
  2. Otherwise → pick the first available provider per model
     (priority: anthropic > bedrock > vertex > openai > github_models)

Usage:
    from copilot_models import ModelRouter
    router = ModelRouter()
    result = router.call_skill("gather_requirements", messages)
"""

import os
import sys
from pathlib import Path
from typing import Literal

# Allow imports from agent_core/
sys.path.insert(0, str(Path(__file__).parent))

from providers.base import ProviderRegistry, ModelInfo


# ─────────────────────────────────────────────────────────────────────────────
# Canonical model IDs — used in SKILL_MODEL_MAP
# These are the "ideal" models for each skill.  The ProviderRegistry will
# find the best available provider that can serve each one, or fall back
# to a compatible model in the same family/tier.
# ─────────────────────────────────────────────────────────────────────────────

# Claude
CLAUDE_HAIKU  = "claude-3-5-haiku-20241022"
CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
CLAUDE_OPUS   = "claude-3-opus-20240229"

# GPT
GPT_4O      = "gpt-4o"
GPT_4O_MINI = "gpt-4o-mini"


# ─────────────────────────────────────────────────────────────────────────────
# Skill → (family, model_id) mapping — covers all 20 agent skills
#
# "family" is the desired model family (claude/gpt).
# "model_id" is the canonical model ID.
# The ProviderRegistry resolves which backend actually serves it.
# ─────────────────────────────────────────────────────────────────────────────

SKILL_MODEL_MAP: dict[str, tuple[str, str]] = {
    # ── Product team ──────────────────────────────────────────────────────────
    "gather_requirements": ("claude", CLAUDE_SONNET),
    "write_spec":          ("claude", CLAUDE_OPUS),

    # ── Architecture team ─────────────────────────────────────────────────────
    "analyze_repo":        ("claude", CLAUDE_HAIKU),
    "design_system":       ("claude", CLAUDE_OPUS),

    # ── Development team ──────────────────────────────────────────────────────
    "plan_tasks":          ("claude", CLAUDE_SONNET),
    "implement_feature":   ("claude", CLAUDE_SONNET),
    "refactor_code":       ("claude", CLAUDE_SONNET),
    "fix_bug":             ("claude", CLAUDE_SONNET),

    # ── QA team ───────────────────────────────────────────────────────────────
    "generate_tests":      ("gpt",    GPT_4O),
    "debug_cycle":         ("claude", CLAUDE_SONNET),
    "review_code":         ("claude", CLAUDE_OPUS),

    # ── DevOps team ───────────────────────────────────────────────────────────
    "configure_ci":        ("gpt",    GPT_4O),
    "deploy_app":          ("gpt",    GPT_4O),

    # ── Documentation team ────────────────────────────────────────────────────
    "update_docs":         ("gpt",    GPT_4O),
    "write_release_notes": ("gpt",    GPT_4O),

    # ── Control layer ─────────────────────────────────────────────────────────
    "critic":              ("claude", CLAUDE_HAIKU),
    "verify_spec":         ("claude", CLAUDE_SONNET),
}

PROVIDER_SHORT = {
    "claude": "claude",
    "gpt":    "gpt",
}


# ─────────────────────────────────────────────────────────────────────────────
# ModelRouter
# ─────────────────────────────────────────────────────────────────────────────

class ModelRouter:
    """
    Resolves auth and dispatches LLM calls for all 20 skills.

    Delegates to ProviderRegistry which automatically discovers and
    prioritises all available LLM backends.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.registry = ProviderRegistry(verbose=verbose)

    # ── Public API ───────────────────────────────────────────────────────────

    def call_skill(
        self,
        skill_name: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Call the correct model for the given skill.

        The ProviderRegistry resolves which backend actually serves the
        model, performing cross-family fallback if needed (e.g. Claude
        skill falls back to GPT-4o when only github_models is available).
        """
        _family, model_id = SKILL_MODEL_MAP.get(
            skill_name, ("claude", CLAUDE_SONNET)
        )

        provider, actual_model = self.registry.resolve(model_id)

        if self.verbose:
            print(f"   🎯 {skill_name} → {provider.name}/{actual_model}")

        return provider.call(actual_model, messages, max_tokens, temperature)

    def get_model_info(self, skill_name: str) -> dict:
        """Return provider + model_id for a skill (useful for logging)."""
        _family, model_id = SKILL_MODEL_MAP.get(skill_name, ("claude", CLAUDE_SONNET))
        try:
            provider, actual_model = self.registry.resolve(model_id)
            return {
                "provider": provider.name,
                "model_id": actual_model,
                "short": provider.name,
            }
        except RuntimeError:
            return {
                "provider": "unavailable",
                "model_id": model_id,
                "short": "??",
            }

    def auth_status(self) -> list[str]:
        """Return the auth resolution report lines."""
        return self.registry.auth_report

    # ── Convenience wrappers (backwards compatibility) ────────────────────────

    def call_claude(
        self,
        messages: list,
        model_type: Literal["haiku", "sonnet", "opus"] = "sonnet",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str:
        model_map = {"haiku": CLAUDE_HAIKU, "sonnet": CLAUDE_SONNET, "opus": CLAUDE_OPUS}
        model_id = model_map.get(model_type, CLAUDE_SONNET)
        return self.registry.call(model_id, messages, max_tokens, temperature)

    def call_gpt(
        self,
        messages: list,
        model_type: Literal["gpt4o", "gpt4o-mini"] = "gpt4o",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str:
        model_map = {"gpt4o": GPT_4O, "gpt4o-mini": GPT_4O_MINI}
        model_id = model_map.get(model_type, GPT_4O)
        return self.registry.call(model_id, messages, max_tokens, temperature)

    def validate_token(self) -> bool:
        """Quick ping to verify at least one provider is reachable."""
        try:
            self.registry.call(GPT_4O, [{"role": "user", "content": "ping"}], 5, 0.0)
            return True
        except Exception:
            pass
        try:
            self.registry.call(CLAUDE_HAIKU, [{"role": "user", "content": "ping"}], 5, 0.0)
            return True
        except Exception as e:
            print(f"❌ Token validation failed: {e}")
            return False


# ── Backwards-compat alias ────────────────────────────────────────────────────
CopilotModelSelector = ModelRouter


# ─────────────────────────────────────────────────────────────────────────────
# Quick smoke-test
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load .env for standalone testing
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent / ".env")
        load_dotenv(Path(__file__).parent.parent / ".env")
    except ImportError:
        pass

    router = ModelRouter(verbose=True)

    print("\nSkill -> Model mapping (effective):")
    for skill, (_fam, mid) in SKILL_MODEL_MAP.items():
        info = router.get_model_info(skill)
        print(f"  {skill:<25} {info['provider']}/{info['model_id']}")

    print("\nAvailable providers:")
    for name, p in router.registry.available_providers.items():
        print(f"  {name}:")
        for m in p.models():
            print(f"    {m.model_id:<50} [{m.family}/{m.tier}]")
