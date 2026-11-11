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
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api import db
from api.limits import limiter
from api.routes import router
from recommender import config
from recommender.artifacts import ensure_artifacts
from recommender.ranking import Engine


def default_engine() -> Engine:
    # In production the container starts empty: fetch the model and data
    # from the private Hub repo first (no-op when they are already there).
    return Engine.load(ensure_artifacts(config.ARTIFACTS_DIR))


def create_app(
    engine_factory: Callable[[], Engine] = default_engine,
    database_url: str = config.DATABASE_URL,
) -> FastAPI:
    """Build the app. Tests pass a fake engine factory and a temporary database."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load the model, index and profiles once, not on every request.
        app.state.engine = engine_factory()
        app.state.db = db.connect(database_url)
        yield
        app.state.db.dispose()

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
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.include_router(router, prefix="/api")
    return app


app = create_app()
