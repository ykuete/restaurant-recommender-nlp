"""JSON contract between the API and the frontend.

The frontend mirrors these models as TypeScript types in frontend/lib/types.ts.
Change both together.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

DietaryOption = Literal["vegetarian", "vegan", "gluten-free", "halal", "kosher"]


MAX_QUERY_CHARS = 300
MAX_RESULTS = 20


class RecommendRequest(BaseModel):
    query: str = Field(
        ..., min_length=2, max_length=MAX_QUERY_CHARS,
        examples=["quiet date-night spot with great pasta"],
    )
    city: str | None = Field(None, max_length=80, examples=["Philadelphia"])
    cuisine: str | None = Field(None, max_length=80, examples=["Italian"])
    price: list[Annotated[int, Field(ge=1, le=4)]] = Field(
        default_factory=list, max_length=4, description="Yelp price levels 1-4 ($-$$$$)"
    )
    dietary: list[DietaryOption] = Field(default_factory=list, max_length=5)
    k: int = Field(10, ge=1, le=MAX_RESULTS)


class AspectScore(BaseModel):
    key: str
    label: str
    positive: int = Field(..., description="% of mentions that are positive")
    negative: int = Field(..., description="% of mentions that are negative")
    mentions: int


class Snippet(BaseModel):
    text: str
    stars: int
    aspect: str | None = None


class MatchScores(BaseModel):
    semantic: float
    aspect_fit: float
    rating: float


class RestaurantCard(BaseModel):
    business_id: str
    name: str
    city: str
    state: str
    categories: list[str]
    price: int | None
    stars: float
    review_count: int
    aspects: list[AspectScore]


class RestaurantResult(RestaurantCard):
    match: int = Field(..., description="0-100 hybrid score")
    scores: MatchScores
    query_aspects: list[str]
    snippet: Snippet | None
    summary: str


class RecommendResponse(BaseModel):
    query: str
    query_aspects: list[str]
    results: list[RestaurantResult]
    baseline: list[RestaurantCard]


class AspectSnippet(BaseModel):
    aspect: str
    label: str
    text: str
    sentiment: Literal["positive", "negative"]
    stars: int
    year: int


class RestaurantDetail(RestaurantCard):
    snippets: list[AspectSnippet]
    similar: list[RestaurantCard]


class FeedbackIn(BaseModel):
    business_id: str = Field(..., max_length=64)
    query: str = Field(..., max_length=MAX_QUERY_CHARS)
    helpful: bool


class Health(BaseModel):
    status: Literal["ok", "loading"]
    restaurants: int
