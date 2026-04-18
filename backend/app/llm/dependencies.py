from functools import lru_cache

from .base import BaseLLMProvider
from .mock_provider import MockLLMProvider


@lru_cache()
def get_llm_provider() -> BaseLLMProvider:
    return MockLLMProvider()
