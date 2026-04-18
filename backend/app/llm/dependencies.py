from functools import lru_cache

from .base import BaseLLMProvider
from .mock_provider import MockLLMProvider
from .http_provider import HttpLLMProvider
from ..config import get_settings


@lru_cache()
def get_llm_provider() -> BaseLLMProvider:
    settings = get_settings()
    if settings.llm_provider_url:
        return HttpLLMProvider(
            str(settings.llm_provider_url),
            timeout_seconds=settings.llm_provider_timeout_seconds,
            api_key=settings.llm_provider_api_key,
            provider_type=settings.llm_provider_type,
            model=settings.llm_provider_model,
        )
    return MockLLMProvider()
