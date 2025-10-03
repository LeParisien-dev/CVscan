import os
from typing import Dict, Any

from services.llm.llm_interface import LlmProvider
from services.llm.openai_provider import OpenAIProvider
from services.llm.openrouter_provider import OpenRouterProvider


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
        return await self.provider.chat(prompt, system, max_tokens, temperature)
