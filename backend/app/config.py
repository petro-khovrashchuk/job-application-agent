from functools import lru_cache
from typing import List, Optional

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    dev_origin: HttpUrl = Field("http://localhost:3000", env="DEV_ORIGIN")
    chrome_extension_id: str = Field(..., env="CHROME_EXTENSION_ID")
    llm_provider_url: Optional[HttpUrl] = Field(None, env="LLM_PROVIDER_URL")
    llm_provider_timeout_seconds: float = Field(30.0, env="LLM_PROVIDER_TIMEOUT_SECONDS")

    @property
    def extension_origin(self) -> str:
        return f"chrome-extension://{self.chrome_extension_id}"

    @property
    def cors_origins(self) -> List[str]:
        return [str(self.dev_origin), self.extension_origin]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
