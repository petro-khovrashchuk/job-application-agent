from typing import Dict

from .base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Deterministic mock that reads the prompt context to return believable text."""

    async def generate(self, prompt: str, purpose: str) -> str:
        if purpose == "tailored_cv":
            return self._tailored_cv(prompt)
        if purpose == "cover_letter":
            return self._cover_letter(prompt)
        if purpose == "form_data":
            return self._form_data(prompt)
        return "Unable to generate content for the requested purpose."

    def _tailored_cv(self, prompt: str) -> str:
        return (
            "## Tailored CV Snapshot\n"
            "- Highlight: Demonstrated experience matching the job requirements.\n"
            "- Value props: Deep understanding of the problem space and strong alignment "
            "with the requested skills.\n"
            f"- Prompt recap: {prompt[:150]}..."
        )

    def _cover_letter(self, prompt: str) -> str:
        return (
            "Dear Hiring Team,\n\n"
            "I am excited by this opportunity because it aligns with my experience "
            "delivering results similar to the ones described above.\n\n"
            "I am confident we would be an excellent match due to my commitment to "
            "the mission and my ability to deliver under tight deadlines.\n\n"
            "Best regards,\n"
            "A Dev Advocate\n"
            f"({prompt[:100]}...)"
        )

    def _form_data(self, prompt: str) -> str:
        data: Dict[str, str] = {
            "desired_role": "Product-focused Developer",
            "availability": "Immediately",
            "key_strength": "Translating requirements into polished deliverables",
        }
        lines = [f"{key}: {value}" for key, value in data.items()]
        lines.append(f"source_reference: {prompt[:80]}...")
        return "\n".join(lines)
