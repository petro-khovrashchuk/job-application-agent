import json
import re
from typing import Any, Dict

from fastapi import HTTPException

from ..llm.base import BaseLLMProvider, LLMProviderError
from ..schemas.request import ProcessRequest
from ..schemas.response import ProcessResponse
from .prompt_builder import PromptBuilder


class JobAgentService:
    def __init__(self, llm_provider: BaseLLMProvider, prompt_builder: PromptBuilder):
        self._provider = llm_provider
        self._prompt_builder = prompt_builder

    async def craft_application(self, request: ProcessRequest) -> ProcessResponse:
        prompts = self._prompt_builder.build(request)

        try:
            tailored_cv = await self._provider.generate(prompts["tailored_cv"], "tailored_cv")
            cover_letter = await self._provider.generate(prompts["cover_letter"], "cover_letter")
            form_blob = await self._provider.generate(prompts["form_data"], "form_data")
        except LLMProviderError as exc:
            raise HTTPException(status_code=503, detail=f"LLM provider failure: {exc}") from exc

        form_data = self._parse_form_blob(form_blob)

        return ProcessResponse(
            tailored_cv=tailored_cv,
            cover_letter=cover_letter,
            form_data=form_data,
        )

    @staticmethod
    def _parse_form_blob(blob: str) -> Dict[str, Any]:
        json_payload = JobAgentService._extract_json_payload(blob)
        if json_payload:
            return json_payload

        data: Dict[str, str] = {}
        for line in blob.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        return data

    @staticmethod
    def _extract_json_payload(blob: str) -> Any | None:
        match = re.search(r"```json\s*([\s\S]*?)```", blob, re.IGNORECASE)
        if not match:
            return None

        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
