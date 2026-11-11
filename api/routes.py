"""API routes, mounted under /api.

No `from __future__ import annotations` here: the rate-limit decorator
wraps the endpoints, and FastAPI must still see the real type objects.
"""

from fastapi import APIRouter, HTTPException, Request, status
from starlette.concurrency import run_in_threadpool

from api.db import save_feedback
from api.limits import RECOMMEND_LIMIT, limiter
from api.schemas import (
    FeedbackIn,
    Health,
    RecommendRequest,
    RecommendResponse,
    RestaurantDetail,
)
from recommender.ranking import Engine, Filters, parse_query
from recommender.summary import summarize

router = APIRouter()


def get_engine(request: Request) -> Engine:
    return request.app.state.engine


def to_filters(req: RecommendRequest) -> Filters:
    return Filters(city=req.city, cuisine=req.cuisine, price=req.price, dietary=list(req.dietary))


@router.post("/recommend", response_model=RecommendResponse)
@limiter.limit(RECOMMEND_LIMIT)
async def recommend(req: RecommendRequest, request: Request) -> RecommendResponse:
    """Ranked restaurants for a plain-language request, each with a summary."""
    engine = get_engine(request)
    filters = to_filters(req)
    # Ranking is CPU work: run it in a thread so the server stays responsive.
    results = await run_in_threadpool(engine.rank, req.query, filters, req.k)
    for result, summary in zip(results, await summarize(req.query, results), strict=True):
        result["summary"] = summary
    return RecommendResponse(
        query=req.query,
        query_aspects=parse_query(req.query),
        results=results,
        baseline=engine.baseline(filters, k=3),
    )


@router.get("/restaurants/{business_id}", response_model=RestaurantDetail)
def restaurant(business_id: str, request: Request) -> RestaurantDetail:
    """Aspect profile, review snippets and similar restaurants."""
    detail = get_engine(request).restaurant(business_id)
    if detail is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Restaurant not found")
    return detail


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
def feedback(item: FeedbackIn, request: Request) -> dict:
    """Store a helpful / not helpful rating for evaluation."""
    save_feedback(request.app.state.db, item.business_id, item.query, item.helpful)
    return {"saved": True}


@router.get("/health", response_model=Health)
def health(request: Request) -> Health:
    """For the host's health check: is the engine loaded?"""
    engine = getattr(request.app.state, "engine", None)
    if engine is None:
        return Health(status="loading", restaurants=0)
    return Health(status="ok", restaurants=len(engine.restaurants))
