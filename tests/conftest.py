"""Shared fixtures: a tiny in-memory Engine, so tests need no model or data."""

import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from recommender.ranking import Engine


def fake_encoder(texts):
    """Bag-of-words hashing into 384 dims: same words -> similar vectors."""
    out = np.zeros((len(texts), 384), dtype=np.float32)
    for i, text in enumerate(texts):
        for word in text.lower().replace(",", " ").split():
            out[i, int(hashlib.md5(word.encode()).hexdigest(), 16) % 384] += 1
    norms = np.linalg.norm(out, axis=1, keepdims=True)
    return out / np.clip(norms, 1e-12, None)


RESTAURANTS = [
    # id, name, city, stars, reviews, price, categories, description used as its vector
    (
        "lume",
        "Trattoria Lume",
        "Philadelphia",
        4.5,
        612,
        3,
        "Italian, Restaurants",
        "quiet romantic pasta candle date night",
    ),
    (
        "verde",
        "Osteria Verde",
        "Philadelphia",
        4.0,
        389,
        2,
        "Italian, Wine Bars, Restaurants",
        "pasta wine cozy calm",
    ),
    (
        "forno",
        "Piccolo Forno",
        "Philadelphia",
        4.5,
        1024,
        2,
        "Italian, Pizza, Restaurants",
        "pasta pizza loud crowded busy",
    ),
    (
        "taco",
        "Taqueria Sol",
        "Philadelphia",
        4.0,
        210,
        1,
        "Mexican, Vegan, Restaurants",
        "cheap fast tacos vegan lunch",
    ),
    (
        "brunch",
        "Morning Lark",
        "Tampa",
        4.5,
        880,
        2,
        "Breakfast & Brunch, Cafes",
        "brunch coffee eggs pancakes",
    ),
]

PROFILES = [
    # id, aspect, mentions, positive_share, negative_share
    ("lume", "food", 40, 0.93, 0.04),
    ("lume", "noise", 12, 0.84, 0.10),
    ("lume", "ambience", 20, 0.91, 0.05),
    ("lume", "price", 15, 0.40, 0.45),
    ("verde", "food", 30, 0.90, 0.05),
    ("verde", "noise", 8, 0.70, 0.20),
    ("forno", "food", 60, 0.95, 0.02),
    ("forno", "noise", 25, 0.30, 0.65),
    ("taco", "price", 20, 0.90, 0.05),
    ("taco", "wait_time", 10, 0.80, 0.10),
    ("brunch", "food", 30, 0.85, 0.05),
]


@pytest.fixture
def engine() -> Engine:
    restaurants = pd.DataFrame(
        [
            {
                "business_id": b,
                "name": n,
                "city": c,
                "state": "PA",
                "stars": s,
                "review_count": v,
                "is_open": 1,
                "attributes": json.dumps({"RestaurantsPriceRange2": str(p)}),
                "categories": cat,
            }
            for b, n, c, s, v, p, cat, _ in RESTAURANTS
        ]
    )
    profiles = pd.DataFrame(
        [
            {
                "business_id": b,
                "aspect": a,
                "mentions": m,
                "positive_share": pos,
                "negative_share": neg,
                "mean_score": pos - neg,
            }
            for b, a, m, pos, neg in PROFILES
        ]
    )
    snippets = pd.DataFrame(
        [
            {
                "business_id": "lume",
                "aspect": "food",
                "sentence": "Best cacio e pepe of my year.",
                "score": 0.95,
                "stars": 5,
                "date": pd.Timestamp("2021-05-01"),
            },
            {
                "business_id": "lume",
                "aspect": "price",
                "sentence": "Delicious but very pricey.",
                "score": -0.7,
                "stars": 3,
                "date": pd.Timestamp("2021-06-01"),
            },
        ]
    )
    ids = np.array([r[0] for r in RESTAURANTS])
    matrix = fake_encoder([r[7] for r in RESTAURANTS])
    return Engine(restaurants, profiles, snippets, ids, matrix, fake_encoder)
