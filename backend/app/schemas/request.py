from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    cv_markdown: str = Field(..., min_length=1)
    job_description_markdown: str = Field(..., min_length=1)
    user_wishes: str = Field(..., min_length=1)
