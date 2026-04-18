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
    def _parse_form_blob(blob: str) -> Dict[str, str]:
        json_payload = JobAgentService._extract_json_payload(blob)
        if json_payload:
            return JobAgentService._flatten_payload(json_payload)

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

    @staticmethod
    def _flatten_payload(payload: Any, parent_key: str = "") -> Dict[str, str]:
        data: Dict[str, str] = {}

        if isinstance(payload, dict):
            for key, value in payload.items():
                compound_key = f"{parent_key}.{key}" if parent_key else key
                data.update(JobAgentService._flatten_payload(value, compound_key))
        elif isinstance(payload, list):
            for idx, value in enumerate(payload):
                compound_key = f"{parent_key}[{idx}]" if parent_key else f"[{idx}]"
                data.update(JobAgentService._flatten_payload(value, compound_key))
        else:
            data[parent_key or "value"] = str(payload)

        return data
