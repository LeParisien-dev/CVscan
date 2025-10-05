import os
from typing import Dict, Any

# --- Corrected imports using absolute package path ---
from src.services.llm.llm_interface import LlmProvider
from src.services.llm.openai_provider import OpenAIProvider
from src.services.llm.openrouter_provider import OpenRouterProvider


class LlmService:
    def __init__(self):
        provider_name = os.getenv("LLM_PROVIDER", "openrouter").lower()
        if provider_name == "openai":
            self.provider: LlmProvider = OpenAIProvider()
        else:
            self.provider: LlmProvider = OpenRouterProvider()

    async def chat(
        self,
        prompt: str,
        system: str = None,
        max_tokens: int = 512,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """Unified entry point for LLM chat interaction"""
        return await self.provider.chat(prompt, system, max_tokens, temperature)
