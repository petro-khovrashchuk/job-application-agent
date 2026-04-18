from typing import Dict, Optional

import httpx

from .base import BaseLLMProvider


class HttpLLMProvider(BaseLLMProvider):
    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def generate(self, prompt: str, purpose: str) -> str:
        payload: Dict[str, str] = {"prompt": prompt, "purpose": purpose}
        response = await self._client.post(self._base_url, json=payload)
        response.raise_for_status()

        text = ""
        try:
            body = response.json()
            if isinstance(body, dict):
                text = str(body.get("output") or body.get("text") or body.get("result", ""))
        except ValueError:
            pass

        if not text:
            text = response.text.strip()

        if not text:
            text = f"{purpose} result unavailable from {self._base_url}"

        return text
