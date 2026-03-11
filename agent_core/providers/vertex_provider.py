"""
GCP Vertex AI provider — access Claude + Gemini through your GCP project.

Data stays in YOUR GCP infrastructure. No training on your data.
Uses GCP service account or application default credentials.

Env vars:
  GOOGLE_CLOUD_PROJECT    (required — your GCP project ID)
  GOOGLE_CLOUD_REGION     (default: us-east5)
  GOOGLE_APPLICATION_CREDENTIALS  (optional — path to service account JSON)

Required package:
  pip install anthropic[vertex]
  pip install google-cloud-aiplatform   (for Gemini models)
"""

from __future__ import annotations
import os

from .base import LLMProvider, ModelInfo

_ANTHROPIC_VERTEX_AVAILABLE = False
try:
    from anthropic import AnthropicVertex
    _ANTHROPIC_VERTEX_AVAILABLE = True
except ImportError:
    pass

_VERTEX_AI_AVAILABLE = False
try:
    from google.cloud import aiplatform
    from vertexai.generative_models import GenerativeModel
    _VERTEX_AI_AVAILABLE = True
except ImportError:
    pass

# Claude models available on Vertex AI
_CLAUDE_MODELS = [
    ModelInfo("claude-3-5-haiku@20241022",    "claude", "fast",      "vertex", "Claude 3.5 Haiku (Vertex)"),
    ModelInfo("claude-3-5-sonnet-v2@20241022","claude", "balanced",  "vertex", "Claude 3.5 Sonnet v2 (Vertex)"),
    ModelInfo("claude-3-opus@20240229",       "claude", "powerful",  "vertex", "Claude 3 Opus (Vertex)"),
    ModelInfo("claude-3-sonnet@20240229",     "claude", "balanced",  "vertex", "Claude 3 Sonnet (Vertex)"),
    ModelInfo("claude-3-haiku@20240307",      "claude", "fast",      "vertex", "Claude 3 Haiku (Vertex)"),
]

# Gemini models available on Vertex AI
_GEMINI_MODELS = [
    ModelInfo("gemini-1.5-pro",               "gemini", "powerful",  "vertex", "Gemini 1.5 Pro (Vertex)"),
    ModelInfo("gemini-1.5-flash",             "gemini", "fast",      "vertex", "Gemini 1.5 Flash (Vertex)"),
    ModelInfo("gemini-2.0-flash",             "gemini", "fast",      "vertex", "Gemini 2.0 Flash (Vertex)"),
]


class VertexProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "vertex"

    def _project(self) -> str | None:
        return os.getenv("GOOGLE_CLOUD_PROJECT")

    def _region(self) -> str:
        return os.getenv("GOOGLE_CLOUD_REGION", "us-east5")

    def is_available(self) -> bool:
        has_sdk = _ANTHROPIC_VERTEX_AVAILABLE or _VERTEX_AI_AVAILABLE
        has_project = bool(self._project())
        return has_sdk and has_project

    def models(self) -> list[ModelInfo]:
        result = []
        if _ANTHROPIC_VERTEX_AVAILABLE:
            result.extend(_CLAUDE_MODELS)
        if _VERTEX_AI_AVAILABLE:
            result.extend(_GEMINI_MODELS)
        return result

    def status_line(self) -> str:
        if not (_ANTHROPIC_VERTEX_AVAILABLE or _VERTEX_AI_AVAILABLE):
            return "no Vertex SDK installed (pip install anthropic[vertex] or google-cloud-aiplatform)"
        if not self._project():
            return "no GOOGLE_CLOUD_PROJECT set"
        sdks = []
        if _ANTHROPIC_VERTEX_AVAILABLE:
            sdks.append("Claude")
        if _VERTEX_AI_AVAILABLE:
            sdks.append("Gemini")
        return f"project={self._project()} region={self._region()} ({' + '.join(sdks)})"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        # Claude models on Vertex use the Anthropic SDK with Vertex backend
        if "claude" in model_id:
            return self._call_claude(model_id, messages, max_tokens, temperature)
        # Gemini models use the Vertex AI SDK
        elif "gemini" in model_id:
            return self._call_gemini(model_id, messages, max_tokens, temperature)
        else:
            raise RuntimeError(f"Vertex provider doesn't know how to call model: {model_id}")

    def _call_claude(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
    ) -> str:
        if not _ANTHROPIC_VERTEX_AVAILABLE:
            raise RuntimeError(
                "anthropic[vertex] not installed. Run: pip install anthropic[vertex]"
            )
        client = AnthropicVertex(
            project_id=self._project(),
            region=self._region(),
        )
        response = client.messages.create(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return response.content[0].text

    def _call_gemini(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
    ) -> str:
        if not _VERTEX_AI_AVAILABLE:
            raise RuntimeError(
                "google-cloud-aiplatform not installed. Run: pip install google-cloud-aiplatform"
            )
        aiplatform.init(project=self._project(), location=self._region())
        model = GenerativeModel(model_id)
        # Convert OpenAI-style messages to Gemini format
        prompt = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Model'}: {m['content']}"
            for m in messages
        )
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        return response.text

