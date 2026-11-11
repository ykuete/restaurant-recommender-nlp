"""FastAPI application.

Run locally from the repository root:
    uvicorn api.main:app --reload
then open http://localhost:8000/docs
"""

from __future__ import annotations

from collections.abc import Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recommender import config
from recommender.ranking import Engine


def default_engine() -> Engine:
    return Engine.load(config.ARTIFACTS_DIR)


def create_app(engine_factory: Callable[[], Engine] = default_engine) -> FastAPI:
    """Build the app. Tests pass a factory that returns a small fake engine."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load the model, index and profiles once, not on every request.
        app.state.engine = engine_factory()
        yield

    app = FastAPI(
        title="TasteLens API",
        version="0.1.0",
        description="Restaurant recommendations from review text.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    return app


app = create_app()
