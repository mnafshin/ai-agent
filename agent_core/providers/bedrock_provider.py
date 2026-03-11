"""
AWS Bedrock provider — access Claude (and more) through your AWS account.

Data stays in YOUR AWS infrastructure. No training on your data.
Uses standard AWS IAM credentials.

Env vars (any standard AWS auth method works):
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_REGION              (default: us-east-1)
  AWS_PROFILE             (optional, for named profiles)

Required package:
  pip install boto3
"""

from __future__ import annotations
import os
import json

from .base import LLMProvider, ModelInfo

_SDK_AVAILABLE = False
try:
    import boto3
    _SDK_AVAILABLE = True
except ImportError:
    pass

# Bedrock model IDs — Anthropic models available on Bedrock
# Reference: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
_MODELS = [
    # Claude models
    ModelInfo("anthropic.claude-3-5-haiku-20241022-v1:0",    "claude",  "fast",      "bedrock", "Claude 3.5 Haiku (Bedrock)"),
    ModelInfo("anthropic.claude-3-5-sonnet-20241022-v2:0",   "claude",  "balanced",  "bedrock", "Claude 3.5 Sonnet v2 (Bedrock)"),
    ModelInfo("anthropic.claude-3-opus-20240229-v1:0",       "claude",  "powerful",  "bedrock", "Claude 3 Opus (Bedrock)"),
    ModelInfo("anthropic.claude-3-sonnet-20240229-v1:0",     "claude",  "balanced",  "bedrock", "Claude 3 Sonnet (Bedrock)"),
    ModelInfo("anthropic.claude-3-haiku-20240307-v1:0",      "claude",  "fast",      "bedrock", "Claude 3 Haiku (Bedrock)"),
    # Llama models
    ModelInfo("meta.llama3-1-405b-instruct-v1:0",            "llama",   "powerful",  "bedrock", "Llama 3.1 405B (Bedrock)"),
    ModelInfo("meta.llama3-1-70b-instruct-v1:0",             "llama",   "balanced",  "bedrock", "Llama 3.1 70B (Bedrock)"),
    ModelInfo("meta.llama3-1-8b-instruct-v1:0",              "llama",   "fast",      "bedrock", "Llama 3.1 8B (Bedrock)"),
    # Mistral
    ModelInfo("mistral.mistral-large-2407-v1:0",             "mistral", "balanced",  "bedrock", "Mistral Large (Bedrock)"),
]


class BedrockProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "bedrock"

    def _region(self) -> str:
        return os.getenv("AWS_REGION", "us-east-1")

    def is_available(self) -> bool:
        if not _SDK_AVAILABLE:
            return False
        # boto3 can authenticate via many methods (env vars, profiles, instance role)
        # We check for the most explicit ones; boto3 will handle the rest at call time
        has_explicit_keys = bool(os.getenv("AWS_ACCESS_KEY_ID"))
        has_profile       = bool(os.getenv("AWS_PROFILE"))
        has_bedrock_flag  = os.getenv("LLM_PROVIDER", "").lower() == "bedrock"
        return has_explicit_keys or has_profile or has_bedrock_flag

    def models(self) -> list[ModelInfo]:
        return list(_MODELS)

    def status_line(self) -> str:
        if not _SDK_AVAILABLE:
            return "boto3 not installed (pip install boto3)"
        if not self.is_available():
            return "no AWS credentials found"
        region = self._region()
        return f"AWS Bedrock → {region} (data stays in your AWS account)"

    def call(
        self,
        model_id: str,
        messages: list[dict],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self._region(),
        )

        # Build Anthropic-compatible request body for Claude models
        if "anthropic" in model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        elif "meta" in model_id:
            # Llama on Bedrock uses a simpler format
            prompt = "\n".join(
                f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
                for m in messages
            ) + "\nAssistant:"
            body = {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": temperature,
            }
        elif "mistral" in model_id:
            body = {
                "prompt": messages[-1]["content"] if messages else "",
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        else:
            # Generic fallback — try Anthropic format
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())

        # Parse response based on model type
        if "anthropic" in model_id:
            return result["content"][0]["text"]
        elif "meta" in model_id:
            return result.get("generation", "")
        elif "mistral" in model_id:
            return result.get("outputs", [{}])[0].get("text", "")
        else:
            return result.get("content", [{}])[0].get("text", str(result))

