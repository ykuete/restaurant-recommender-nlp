"""Aspect extraction and aspect-based sentiment.

1. tag_aspects(): tag each review sentence with the aspects it talks about,
   using keyword lists. Fast, transparent and easy to extend.
2. AspectSentimentScorer: score each (sentence, aspect) pair from -1
   (negative) to +1 (positive) with a pretrained aspect-based sentiment model.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from functools import lru_cache
from typing import Protocol

import pandas as pd

from recommender import config

# Display names used by the API and the frontend.
ASPECT_LABELS = {
    "food": "Food",
    "service": "Service",
    "ambience": "Ambience",
    "price": "Price",
    "noise": "Quiet (noise)",
    "wait_time": "Wait time",
    "dietary": "Dietary options",
}

# Keywords per aspect. Multi-word phrases are allowed. Matching is
# case-insensitive on word boundaries, with an optional plural "s".
# fmt: off
ASPECT_KEYWORDS: dict[str, list[str]] = {
    "food": [
        "food", "dish", "meal", "menu", "taste", "tasty", "delicious", "flavor",
        "flavour", "bland", "fresh", "pasta", "pizza", "burger", "sandwich",
        "taco", "sushi", "ramen", "noodle", "steak", "chicken", "salad",
        "dessert", "appetizer", "entree", "portion", "brunch", "breakfast",
        "lunch", "dinner", "coffee", "wine", "cocktail", "drink", "sauce",
        "seafood", "bread", "cheesesteak", "gnocchi", "lasagna", "risotto",
    ],
    "service": [
        "service", "server", "waiter", "waitress", "staff", "host", "hostess",
        "bartender", "manager", "friendly", "rude", "attentive", "polite",
        "welcoming", "helpful", "owner",
    ],
    "ambience": [
        "ambience", "ambiance", "atmosphere", "decor", "vibe", "romantic",
        "cozy", "cosy", "date night", "date-night", "date", "lighting",
        "candle", "music", "interior", "patio", "view", "intimate", "charming",
        "lively", "anniversary",
    ],
    "price": [
        "price", "pricey", "expensive", "cheap", "affordable", "overpriced",
        "value", "worth", "cost", "bill", "budget", "inexpensive", "deal",
        "reasonable", "dollar",
    ],
    "noise": [
        "noise", "noisy", "loud", "quiet", "calm", "peaceful", "hear each other",
        "shout", "shouting", "crowded", "packed", "conversation",
    ],
    "wait_time": [
        "wait", "waited", "waiting", "line", "queue", "seated", "slow", "fast",
        "quick", "quickly", "took forever", "reservation", "minutes", "hour",
    ],
    "dietary": [
        "vegan", "vegetarian", "gluten", "gluten-free", "halal", "kosher",
        "dairy-free", "allergy", "allergies", "plant-based", "keto",
    ],
}
# fmt: on


@lru_cache(maxsize=1)
def _patterns() -> dict[str, re.Pattern[str]]:
    compiled = {}
    for aspect, words in ASPECT_KEYWORDS.items():
        alternatives = "|".join(re.escape(w).replace(r"\ ", r"\s+") for w in words)
        compiled[aspect] = re.compile(rf"\b(?:{alternatives})s?\b", re.IGNORECASE)
    return compiled


def tag_aspects(sentence: str) -> list[str]:
    """Aspects a sentence mentions, in ASPECT_KEYWORDS order (may be empty)."""
    return [aspect for aspect, pattern in _patterns().items() if pattern.search(sentence)]


# Words given to the aspect-based sentiment model as the "aspect" input.
ASPECT_TERMS = {
    "food": "food",
    "service": "service",
    "ambience": "ambience",
    "price": "price",
    "noise": "noise level",
    "wait_time": "wait time",
    "dietary": "dietary options",
}


class Scorer(Protocol):
    def score_many(self, pairs: Sequence[tuple[str, str]]) -> list[float]: ...


def _polarity(scores: list[dict]) -> float:
    """Turn label probabilities into one number: P(positive) - P(negative)."""
    probs = {d["label"].lower(): d["score"] for d in scores}
    return float(probs.get("positive", 0.0) - probs.get("negative", 0.0))


class AspectSentimentScorer:
    """Aspect-based sentiment with a Hugging Face model.

    The default model (config.ABSA_MODEL, yangheng/deberta-v3-base-absa-v1.1)
    reads a sentence plus an aspect term and predicts Negative / Neutral /
    Positive for that aspect, so "great pasta, rude waiter" scores food
    positive and service negative.
    """

    def __init__(self, model_name: str = config.ABSA_MODEL, device: int = -1, batch_size: int = 32):
        from transformers import pipeline  # heavy import, only when scoring

        self.batch_size = batch_size
        self._pipe = pipeline("text-classification", model=model_name, device=device, top_k=None)

    def score_many(self, pairs: Sequence[tuple[str, str]]) -> list[float]:
        """Score (sentence, aspect key) pairs. Returns one value in [-1, 1] each."""
        if not pairs:
            return []
        inputs = [{"text": s, "text_pair": ASPECT_TERMS.get(a, a)} for s, a in pairs]
        outputs = self._pipe(inputs, batch_size=self.batch_size, truncation=True)
        return [_polarity(o) for o in outputs]


def score_sentences(sentences: Iterable[str], scorer: Scorer) -> list[dict]:
    """Tag every sentence and score each aspect it mentions.

    Returns one dict per (sentence, aspect): {"sentence", "aspect", "score"}.
    Sentences that mention no aspect are skipped.
    """
    pairs = [(s, a) for s in sentences for a in tag_aspects(s)]
    scores = scorer.score_many(pairs)
    return [
        {"sentence": s, "aspect": a, "score": sc} for (s, a), sc in zip(pairs, scores, strict=True)
    ]


# A sentence counts as positive / negative for an aspect beyond this margin.
POLARITY_MARGIN = 0.25


def build_profiles(
    reviews: pd.DataFrame,
    scorer: Scorer,
    per_restaurant: int = config.REVIEWS_PER_RESTAURANT,
    snippets_per_side: int = 2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aggregate sentence-level aspect sentiment into per-restaurant profiles.

    Uses the ``per_restaurant`` most recent reviews of each restaurant.

    Returns:
        profiles: one row per (business_id, aspect) with mentions,
            positive_share, negative_share and mean_score.
        snippets: the most positive and most negative sentences per
            (business_id, aspect), with the review's stars and date, for the
            detail page and the generated summary.
    """
    from recommender.preprocessing import latest_reviews, split_sentences

    recent = latest_reviews(reviews, per_restaurant)
    rows = []
    for review in recent.itertuples(index=False):
        for sentence in split_sentences(review.text):
            for aspect in tag_aspects(sentence):
                rows.append((review.business_id, review.stars, review.date, sentence, aspect))
    mentions = pd.DataFrame(rows, columns=["business_id", "stars", "date", "sentence", "aspect"])
    if mentions.empty:
        empty_profiles = pd.DataFrame(
            columns=[
                "business_id",
                "aspect",
                "mentions",
                "positive_share",
                "negative_share",
                "mean_score",
            ]
        )
        return empty_profiles, mentions.assign(score=pd.Series(dtype=float))

    pairs = list(zip(mentions["sentence"], mentions["aspect"], strict=True))
    mentions["score"] = scorer.score_many(pairs)
    mentions["positive"] = mentions["score"] > POLARITY_MARGIN
    mentions["negative"] = mentions["score"] < -POLARITY_MARGIN

    profiles = (
        mentions.groupby(["business_id", "aspect"])
        .agg(
            mentions=("score", "size"),
            positive_share=("positive", "mean"),
            negative_share=("negative", "mean"),
            mean_score=("score", "mean"),
        )
        .reset_index()
    )

    # Short, readable sentences make the best snippets.
    readable = mentions[mentions["sentence"].str.len().between(30, 300)]
    ordered = readable.sort_values("score")
    by_aspect = ordered.groupby(["business_id", "aspect"], group_keys=False)
    snippets = pd.concat(
        [
            by_aspect.head(snippets_per_side).query("negative"),
            by_aspect.tail(snippets_per_side).query("positive"),
        ]
    ).drop_duplicates(subset=["business_id", "aspect", "sentence"])
    snippets = snippets[["business_id", "aspect", "sentence", "score", "stars", "date"]]
    return profiles, snippets.reset_index(drop=True)
