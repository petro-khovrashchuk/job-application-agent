from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Defines the contract for LLM providers so the service can stay agnostic."""

    @abstractmethod
    async def generate(self, prompt: str, purpose: str) -> str:
        """Generate text for the given prompt and purpose."""
        raise NotImplementedError
