from typing import Dict

from pydantic import BaseModel, Field


class ProcessResponse(BaseModel):
    tailored_cv: str = Field(..., min_length=1)
    cover_letter: str = Field(..., min_length=1)
    form_data: Dict[str, str] = Field(default_factory=dict)
