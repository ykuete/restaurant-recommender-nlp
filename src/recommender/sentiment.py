"""Aspect extraction and aspect-based sentiment.

Step 1 (this module's lexicon): tag each review sentence with the aspects it
talks about, using keyword lists. Fast, transparent and easy to extend.
"""

from __future__ import annotations

import re
from functools import lru_cache

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
