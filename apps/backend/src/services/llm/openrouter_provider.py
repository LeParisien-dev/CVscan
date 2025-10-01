import os
import httpx
from typing import Dict, Any
from .llm_interface import LlmProvider


class OpenRouterProvider(LlmProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.referrer = os.getenv("OPENROUTER_REFERRER", "http://localhost:4000")
        self.title = os.getenv("OPENROUTER_TITLE", "CVScan")

        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

    async def chat(self, prompt: str, system: str = None, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.referrer,
            "X-Title": self.title,
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
