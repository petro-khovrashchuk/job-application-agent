from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes import job_agent


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Job Application Agent Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(job_agent.router, prefix="")
    return app


app = create_app()
