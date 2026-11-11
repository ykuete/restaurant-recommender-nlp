"""Ranking: the popularity baseline and the hybrid recommender."""

from __future__ import annotations

import pandas as pd

from recommender import config


def weighted_rating(restaurants: pd.DataFrame, quantile: float = config.BASELINE_QUANTILE) -> pd.Series:
    """Bayesian weighted rating from notebooks/03_baseline_model.ipynb.

        WR = v / (v + m) * R + m / (v + m) * C

    R = the restaurant's stars, v = its review count, C = the mean stars of
    all restaurants, m = the review-count quantile (90th by default).
    Restaurants with few reviews are pulled toward the mean.
    """
    v = restaurants["review_count"].astype(float)
    r = restaurants["stars"].astype(float)
    c = r.mean()
    m = v.quantile(quantile)
    return (v / (v + m)) * r + (m / (v + m)) * c


def popularity_baseline(
    restaurants: pd.DataFrame, k: int = 10, quantile: float = config.BASELINE_QUANTILE
) -> pd.DataFrame:
    """Top-k restaurants by weighted rating, among those with at least the
    quantile's review count (exactly the notebook's baseline)."""
    m = restaurants["review_count"].quantile(quantile)
    eligible = restaurants[restaurants["review_count"] >= m]
    scored = eligible.assign(weight_score=weighted_rating(restaurants, quantile).loc[eligible.index])
    return scored.sort_values("weight_score", ascending=False).head(k)
