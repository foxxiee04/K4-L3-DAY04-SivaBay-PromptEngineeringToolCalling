from __future__ import annotations

import os

from providers.openai_provider import OpenAIProvider


class OllamaProvider(OpenAIProvider):
    """Ollama Cloud uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="OLLAMA_API_KEY",
            base_url=os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
            default_model=os.getenv("OLLAMA_MODEL", "gpt-oss:20b"),
        )
