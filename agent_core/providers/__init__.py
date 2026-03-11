"""
LLM Provider abstraction layer.

Supported providers:
  - github_models : GitHub Models API (free, GPT-4o/4o-mini, Llama, Mistral)
  - anthropic     : Direct Anthropic API (Claude 3.5 Haiku/Sonnet, Opus)
  - openai        : Direct OpenAI API (GPT-4o, o1, etc.)
  - bedrock       : AWS Bedrock (Claude + many others, data stays in your AWS)
  - vertex        : GCP Vertex AI (Claude + Gemini, data stays in your GCP)
  - local         : Any OpenAI-compatible local server (Ollama, LM Studio, vLLM, DeepSeek, etc.)
"""

from .base import LLMProvider, ProviderRegistry
from .github_models import GitHubModelsProvider
from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider
from .bedrock_provider import BedrockProvider
from .vertex_provider import VertexProvider
from .local_provider import LocalProvider

__all__ = [
    "LLMProvider",
    "ProviderRegistry",
    "GitHubModelsProvider",
    "AnthropicProvider",
    "OpenAIProvider",
    "BedrockProvider",
    "VertexProvider",
    "LocalProvider",
]
