from typing import Any, Dict, Optional

import httpx

from .base import BaseLLMProvider, LLMProviderError


class HttpLLMProvider(BaseLLMProvider):
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 10.0,
        api_key: Optional[str] = None,
        provider_type: str = "generic",
        model: Optional[str] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._provider_type = provider_type.lower()
        self._model = model
        headers = {"Accept": "application/json"}
        if self._provider_type == "openai":
            headers["Content-Type"] = "application/json"
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_seconds),
            headers=headers,
        )

    async def generate(self, prompt: str, purpose: str) -> str:
        payload = self._build_payload(prompt, purpose)
        try:
            response = await self._client.post(self._base_url, json=payload)
            response.raise_for_status()
        except httpx.ReadTimeout as exc:
            raise LLMProviderError(
                f"{purpose} timed out after {self._client.timeout.read_timeout} on {self._base_url}"
            ) from exc
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"LLM provider error: {exc}") from exc

        text = self._extract_text(response)
        if not text:
            text = f"{purpose} result unavailable from {self._base_url}"
        return text

    def _build_payload(self, prompt: str, purpose: str) -> Dict[str, Any]:
        if self._provider_type == "openai":
            return {
                "model": self._model or "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a concise assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 2048,
            }
        return {"prompt": prompt, "purpose": purpose}

    def _extract_text(self, response: httpx.Response) -> str:
        try:
            body = response.json()
        except ValueError:
            return response.text.strip()

        if isinstance(body, dict):
            if self._provider_type == "openai":
                choices = body.get("choices") or []
                if choices:
                    message = choices[0].get("message") or {}
                    return str(message.get("content", "")).strip()
            return str(body.get("output") or body.get("text") or body.get("result", "")).strip()
        return response.text.strip()
