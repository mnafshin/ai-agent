#!/usr/bin/env python3
"""
Model Version Manager - Resolves model versions from config and handles model selection.

Usage:
    from tools.model_manager import ModelManager
    
    manager = ModelManager()
    model_id = manager.get_model_id("claude/opus-4-6")
    cost = manager.get_cost("gpt/gpt-5")
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import os


class ModelManager:
    """Manages model versions and resolves them to API identifiers."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize model manager with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "models.yaml"
        
        self.config_path = config_path
        self.config = self._load_config()
        self._api_key_cache = {}
    
    def _load_config(self) -> Dict[str, Any]:
        """Load models configuration from YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Model config not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_model_id(self, model_spec: str) -> str:
        """
        Get API model ID from specification.
        
        Examples:
            "claude/opus-4-6" → "claude-opus-4-1-20250805"
            "gpt/gpt-5" → "gpt-5-2025-06-01"
            "copilot/codex" → "github-copilot-codex-5-3"
        
        Args:
            model_spec: Format "provider/model" e.g. "claude/opus-4-6"
        
        Returns:
            API model identifier string
        
        Raises:
            ValueError: If model spec not found or invalid format
        """
        try:
            provider, model = model_spec.split("/")
        except ValueError:
            raise ValueError(f"Invalid model spec format: {model_spec}. Use 'provider/model'")
        
        try:
            model_config = self.config["models"][provider][model]
            return model_config["id"]
        except KeyError:
            available = self._get_available_models(provider)
            raise ValueError(
                f"Model not found: {model_spec}\n"
                f"Available {provider} models: {', '.join(available)}"
            )
    
    def get_model_version(self, model_spec: str) -> str:
        """Get version string for a model."""
        provider, model = model_spec.split("/")
        return self.config["models"][provider][model]["version"]
    
    def get_cost(self, model_spec: str) -> Dict[str, float]:
        """
        Get cost per 1M tokens for a model.
        
        Returns:
            Dict with "input" and "output" costs
        """
        provider, model = model_spec.split("/")
        return self.config["models"][provider][model]["cost"]
    
    def get_description(self, model_spec: str) -> str:
        """Get description of what a model is good for."""
        provider, model = model_spec.split("/")
        return self.config["models"][provider][model]["description"]
    
    def get_max_tokens(self, model_spec: str) -> int:
        """Get max_tokens parameter for a model."""
        provider, model = model_spec.split("/")
        return self.config["models"][provider][model]["max_tokens"]
    
    def get_recommended_model(self, task: str) -> str:
        """Get recommended model for a task type."""
        try:
            return self.config["recommended_models"][task]
        except KeyError:
            available_tasks = list(self.config["recommended_models"].keys())
            raise ValueError(
                f"Task not found: {task}\n"
                f"Available tasks: {', '.join(available_tasks)}"
            )
    
    def resolve_best_available(self, model_spec: str) -> Tuple[str, str]:
        """
        Resolve to best available model with fallback strategy.
        
        Returns:
            Tuple of (model_id, actual_model_spec_used)
        """
        # Try primary model
        try:
            return (self.get_model_id(model_spec), model_spec)
        except (ValueError, KeyError):
            pass
        
        # Try fallback chain
        fallback_chain = self.config.get("fallback", {})
        for level in ["level1", "level2", "level3"]:
            fallback_spec = fallback_chain.get(level)
            if fallback_spec:
                try:
                    return (self.get_model_id(fallback_spec), fallback_spec)
                except (ValueError, KeyError):
                    continue
        
        raise ValueError(f"No available model found, even with fallbacks")
    
    def get_api_key(self, provider: str) -> str:
        """Get API key for a provider from environment."""
        if provider in self._api_key_cache:
            return self._api_key_cache[provider]
        
        env_vars = {
            "claude": "ANTHROPIC_API_KEY",
            "gpt": "OPENAI_API_KEY",
            "copilot": "GITHUB_COPILOT_TOKEN",
        }
        
        env_var = env_vars.get(provider)
        if not env_var:
            raise ValueError(f"Unknown provider: {provider}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError(
                f"API key not found for {provider}. "
                f"Set {env_var} environment variable."
            )
        
        self._api_key_cache[provider] = api_key
        return api_key
    
    def list_models(self, provider: Optional[str] = None) -> Dict[str, str]:
        """List available models, optionally filtered by provider."""
        if provider:
            models = self.config["models"].get(provider, {})
            return {
                name: config["description"]
                for name, config in models.items()
            }
        else:
            result = {}
            for prov, models in self.config["models"].items():
                for model_name, config in models.items():
                    result[f"{prov}/{model_name}"] = config["description"]
            return result
    
    def _get_available_models(self, provider: str) -> list:
        """Get list of available models for a provider."""
        return list(self.config["models"].get(provider, {}).keys())
    
    def get_model_config(self, model_spec: str) -> Dict[str, Any]:
        """Get complete configuration for a model."""
        provider, model = model_spec.split("/")
        return self.config["models"][provider][model].copy()
    
    def estimate_cost(self, model_spec: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a model call."""
        cost = self.get_cost(model_spec)
        input_cost = (input_tokens / 1_000_000) * cost["input"]
        output_cost = (output_tokens / 1_000_000) * cost["output"]
        return input_cost + output_cost


class SkillModelResolver:
    """Resolves models from SKILL file specifications."""
    
    def __init__(self, model_manager: Optional[ModelManager] = None):
        """Initialize resolver."""
        self.manager = model_manager or ModelManager()
    
    def parse_model_spec(self, spec: str) -> str:
        """
        Parse SKILL model specification to API model ID.
        
        Handles multiple formats:
            "claude/opus-4-6"        → API ID
            "gpt/gpt-5"              → API ID
            "claude/opus-4-6 (best)" → API ID (ignores comment)
            "gpt-4o"                 → Assumes gpt/gpt-4o
        
        Args:
            spec: Model specification string
        
        Returns:
            API model identifier
        """
        # Remove comments
        spec = spec.split("(")[0].strip()
        
        # Add provider if missing
        if "/" not in spec:
            # Try to infer provider
            if "gpt" in spec.lower() or "codex" in spec.lower():
                if "codex" in spec.lower():
                    spec = f"copilot/{spec}"
                else:
                    spec = f"gpt/{spec}"
            else:
                # Default to Claude
                spec = f"claude/{spec}"
        
        return self.manager.get_model_id(spec)


# Example usage demonstration
if __name__ == "__main__":
    manager = ModelManager()
    
    # List all models
    print("=== Available Models ===")
    all_models = manager.list_models()
    for model, desc in all_models.items():
        print(f"  {model:<25} {desc}")
    
    # Get specific model
    print("\n=== Model Specifications ===")
    model_id = manager.get_model_id("claude/opus-4-6")
    print(f"claude/opus-4-6 → {model_id}")
    
    # Get cost estimate
    print("\n=== Cost Estimation ===")
    cost = manager.estimate_cost("claude/opus-4-6", input_tokens=1000, output_tokens=500)
    print(f"Cost for 1k input + 500 output: ${cost:.6f}")
    
    # Test resolver
    print("\n=== SKILL Model Resolution ===")
    resolver = SkillModelResolver()
    print(f"'opus-4-6' → {resolver.parse_model_spec('opus-4-6')}")
    print(f"'gpt/gpt-5' → {resolver.parse_model_spec('gpt/gpt-5')}")
    print(f"'codex/codex (best)' → {resolver.parse_model_spec('codex/codex (best)')}")
