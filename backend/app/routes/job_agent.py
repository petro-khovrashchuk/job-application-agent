from fastapi import APIRouter, Depends

from ..llm.dependencies import get_llm_provider
from ..schemas.request import ProcessRequest
from ..schemas.response import ProcessResponse
from ..services.job_agent_service import JobAgentService
from ..services.prompt_builder import PromptBuilder

router = APIRouter()


def get_job_agent_service() -> JobAgentService:
    provider = get_llm_provider()
    builder = PromptBuilder()
    return JobAgentService(provider, builder)


@router.post("/process", response_model=ProcessResponse)
async def process_application(
    payload: ProcessRequest, service: JobAgentService = Depends(get_job_agent_service)
) -> ProcessResponse:
    return await service.craft_application(payload)
