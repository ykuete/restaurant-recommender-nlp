"""API routes, mounted under /api."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from api.schemas import (
    FeedbackIn,
    Health,
    RecommendRequest,
    RecommendResponse,
    RestaurantDetail,
)
from recommender.ranking import Engine, Filters, parse_query

router = APIRouter()


def get_engine(request: Request) -> Engine:
    return request.app.state.engine


def to_filters(req: RecommendRequest) -> Filters:
    return Filters(city=req.city, cuisine=req.cuisine, price=req.price, dietary=list(req.dietary))


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest, request: Request) -> RecommendResponse:
    """Ranked restaurants for a plain-language request."""
    engine = get_engine(request)
    filters = to_filters(req)
    results = engine.rank(req.query, filters, k=req.k)
    for r in results:
        r["summary"] = f"Matches {r['match']}% of your request."
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
def feedback(item: FeedbackIn, request: Request) -> dict:
    """Store a helpful / not helpful rating (in memory for now)."""
    log = getattr(request.app.state, "feedback", None)
    if log is None:
        log = request.app.state.feedback = []
    log.append(item.model_dump())
    return {"saved": True}


@router.get("/health", response_model=Health)
def health(request: Request) -> Health:
    """For the host's health check: is the engine loaded?"""
    engine = getattr(request.app.state, "engine", None)
    if engine is None:
        return Health(status="loading", restaurants=0)
    return Health(status="ok", restaurants=len(engine.restaurants))
