# Contract that every LLM provider must implement.

from typing import Dict, Any, Protocol

class LlmProvider(Protocol):
    async def chat(self, prompt: str, system: str = None, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
        ...
