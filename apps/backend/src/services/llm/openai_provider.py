import os
import httpx
from typing import Dict, Any
from .llm_interface import LlmProvider


class OpenAIProvider(LlmProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.base_url = "https://api.openai.com/v1/chat/completions"

        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    async def chat(self, prompt: str, system: str = None, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(self.base_url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()

        return {
            "content": data["choices"][0]["message"]["content"],
            "model": self.model,
            "usage": data.get("usage", {}),
        }
