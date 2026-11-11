"""Ranking: the popularity baseline and the hybrid recommender."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from recommender import config
from recommender.sentiment import ASPECT_LABELS, tag_aspects


def weighted_rating(
    restaurants: pd.DataFrame, quantile: float = config.BASELINE_QUANTILE
) -> pd.Series:
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
    scored = eligible.assign(
        weight_score=weighted_rating(restaurants, quantile).loc[eligible.index]
    )
    return scored.sort_values("weight_score", ascending=False).head(k)


# --- Hybrid recommender -----------------------------------------------------------

DIETARY_TERMS = {
    "vegetarian": "vegetarian",
    "vegan": "vegan",
    "gluten-free": "gluten",
    "halal": "halal",
    "kosher": "kosher",
}
MIN_MENTIONS = 2  # fewer mentions than this = no reliable signal for an aspect
NEUTRAL = 0.5


@dataclass
class Filters:
    city: str | None = None
    cuisine: str | None = None
    price: list[int] = field(default_factory=list)  # Yelp price levels 1-4 ($ to $$$$)
    dietary: list[str] = field(default_factory=list)  # keys of DIETARY_TERMS


def price_level(attributes: str | None) -> int | None:
    """Yelp's RestaurantsPriceRange2 attribute (1-4) from the JSON text."""
    if not attributes:
        return None
    try:
        value = json.loads(attributes).get("RestaurantsPriceRange2")
        return int(str(value).strip("u'\" "))
    except (ValueError, TypeError, AttributeError):
        return None


def apply_filters(restaurants: pd.DataFrame, filters: Filters | None) -> pd.DataFrame:
    if filters is None:
        return restaurants
    df = restaurants
    if filters.city:
        df = df[df["city"].str.casefold() == filters.city.casefold()]
    if filters.cuisine:
        df = df[df["categories"].fillna("").str.contains(filters.cuisine, case=False, regex=False)]
    if filters.price:
        df = df[df["price"].isin(filters.price)]
    for diet in filters.dietary:
        term = DIETARY_TERMS.get(diet.lower(), diet.lower())
        text = (df["categories"].fillna("") + " " + df["attributes"].fillna("")).str.lower()
        df = df[text.str.contains(term, regex=False)]
    return df


def parse_query(text: str) -> list[str]:
    """Aspects a user request asks about, e.g. 'quiet pasta place' ->
    ['food', 'noise']. Uses the same lexicon as the review tagger."""
    return tag_aspects(text)


class Engine:
    """Everything the API needs to rank restaurants, loaded once.

    hybrid = W_SEMANTIC * semantic + W_ASPECT * aspect_fit + W_RATING * rating
    where each part is scaled to 0-1:
      semantic   = cosine(query, restaurant vector), min-max scaled over the
                   restaurants left after filtering
      aspect_fit = mean positive share of the aspects the query asks about
      rating     = weighted rating (the baseline), min-max scaled
    """

    def __init__(
        self,
        restaurants: pd.DataFrame,
        profiles: pd.DataFrame,
        aspect_snippets: pd.DataFrame,
        restaurant_ids: np.ndarray,
        restaurant_matrix: np.ndarray,
        encoder,
        review_snippets: pd.DataFrame | None = None,
        review_snippet_vectors: np.ndarray | None = None,
        weights: tuple[float, float, float] = (config.W_SEMANTIC, config.W_ASPECT, config.W_RATING),
    ):
        self.encoder = encoder
        self.weights = weights
        row_of = {str(b): i for i, b in enumerate(restaurant_ids)}
        df = restaurants[restaurants["business_id"].isin(row_of)].copy()
        df["row"] = df["business_id"].map(row_of)
        df["price"] = df["attributes"].map(price_level)
        wr = weighted_rating(df)
        df["rating_score"] = (wr - wr.min()) / max(wr.max() - wr.min(), 1e-9)
        self.restaurants = df.set_index("business_id", drop=False)
        self.matrix = np.asarray(restaurant_matrix, dtype=np.float32)

        self.profiles: dict[str, dict[str, dict]] = {}
        for p in profiles.itertuples(index=False):
            self.profiles.setdefault(p.business_id, {})[p.aspect] = {
                "positive_share": float(p.positive_share),
                "negative_share": float(p.negative_share),
                "mentions": int(p.mentions),
            }
        self.aspect_snippets = aspect_snippets
        self.review_snippets = review_snippets
        self.review_snippet_vectors = review_snippet_vectors
        if review_snippets is not None:
            self._snippet_rows = review_snippets.groupby("business_id").indices
        else:
            self._snippet_rows = {}

    # -- loading -------------------------------------------------------------
    @classmethod
    def load(cls, artifacts_dir: str | Path = config.ARTIFACTS_DIR, encoder=None) -> Engine:
        from recommender import embeddings

        a = Path(artifacts_dir)
        index, ids = embeddings.load_index(a)
        snippets_path = a / config.REVIEW_SNIPPETS_FILE
        has_snippets = snippets_path.exists()
        return cls(
            restaurants=pd.read_parquet(a / config.RESTAURANTS_FILE),
            profiles=pd.read_parquet(a / config.PROFILES_FILE),
            aspect_snippets=pd.read_parquet(a / config.ASPECT_SNIPPETS_FILE),
            restaurant_ids=ids,
            restaurant_matrix=index.reconstruct_n(0, index.ntotal),
            encoder=encoder or embeddings.load_encoder(a),
            review_snippets=pd.read_parquet(snippets_path) if has_snippets else None,
            review_snippet_vectors=(
                np.load(a / config.REVIEW_SNIPPET_VECTORS_FILE).astype(np.float32)
                if has_snippets
                else None
            ),
        )

    # -- scoring -------------------------------------------------------------
    def aspect_fit(self, business_id: str, aspects: list[str]) -> float:
        profile = self.profiles.get(business_id, {})
        keys = aspects or list(profile)
        values = [
            profile[a]["positive_share"]
            if a in profile and profile[a]["mentions"] >= MIN_MENTIONS
            else NEUTRAL
            for a in keys
        ]
        return float(np.mean(values)) if values else NEUTRAL

    def rank(self, query: str, filters: Filters | None = None, k: int = 10) -> list[dict]:
        """Ranked restaurants for a free-text query, best first."""
        candidates = apply_filters(self.restaurants, filters)
        if candidates.empty:
            return []
        query_vec = self.encoder([query])[0]
        cosine = self.matrix[candidates["row"].to_numpy()] @ query_vec
        lo, hi = float(np.percentile(cosine, 5)), float(cosine.max())
        semantic = np.clip((cosine - lo) / max(hi - lo, 1e-9), 0, 1)

        aspects = parse_query(query)
        fit = np.array([self.aspect_fit(b, aspects) for b in candidates.index])
        rating = candidates["rating_score"].to_numpy()
        w_sem, w_asp, w_rat = self.weights
        hybrid = w_sem * semantic + w_asp * fit + w_rat * rating

        order = np.argsort(-hybrid)[:k]
        results = []
        for i in order:
            business_id = candidates.index[i]
            result = self._card(business_id)
            result.update(
                match=int(round(100 * hybrid[i])),
                scores={
                    "semantic": round(float(semantic[i]), 3),
                    "aspect_fit": round(float(fit[i]), 3),
                    "rating": round(float(rating[i]), 3),
                },
                query_aspects=aspects,
                snippet=self.best_snippet(business_id, query_vec, aspects),
            )
            results.append(result)
        return results

    def baseline(self, filters: Filters | None = None, k: int = 3) -> list[dict]:
        """Popularity baseline restricted to the same filters."""
        candidates = apply_filters(self.restaurants, filters)
        top = popularity_baseline(candidates, k=k) if len(candidates) else candidates
        return [self._card(b) for b in top.index]

    # -- presentation ----------------------------------------------------------
    def aspect_list(self, business_id: str) -> list[dict]:
        profile = self.profiles.get(business_id, {})
        return [
            {
                "key": a,
                "label": ASPECT_LABELS[a],
                "positive": int(round(100 * p["positive_share"])),
                "negative": int(round(100 * p["negative_share"])),
                "mentions": p["mentions"],
            }
            for a, p in sorted(profile.items(), key=lambda kv: -kv[1]["mentions"])
            if a in ASPECT_LABELS
        ]

    def _card(self, business_id: str) -> dict:
        r = self.restaurants.loc[business_id]
        price = None if pd.isna(r["price"]) else int(r["price"])
        return {
            "business_id": business_id,
            "name": r["name"],
            "city": r["city"],
            "state": r["state"],
            "categories": [c.strip() for c in (r["categories"] or "").split(",") if c.strip()],
            "price": price,
            "stars": float(r["stars"]),
            "review_count": int(r["review_count"]),
            "aspects": self.aspect_list(business_id),
        }

    def best_snippet(
        self, business_id: str, query_vec: np.ndarray, aspects: list[str]
    ) -> dict | None:
        """The stored review closest to the query, else a positive aspect snippet."""
        rows = self._snippet_rows.get(business_id)
        if rows is not None and self.review_snippet_vectors is not None:
            best = rows[int(np.argmax(self.review_snippet_vectors[rows] @ query_vec))]
            s = self.review_snippets.iloc[best]
            return {"text": s["text"], "stars": int(s["stars"]), "aspect": None}
        snippets = self.snippets_for(business_id)
        preferred = [s for s in snippets if s["aspect"] in aspects and s["sentiment"] == "positive"]
        pick = (preferred or snippets or [None])[0]
        return pick and {"text": pick["text"], "stars": pick["stars"], "aspect": pick["aspect"]}

    def snippets_for(self, business_id: str) -> list[dict]:
        rows = self.aspect_snippets[self.aspect_snippets["business_id"] == business_id]
        return [
            {
                "aspect": s.aspect,
                "label": ASPECT_LABELS.get(s.aspect, s.aspect),
                "text": s.sentence,
                "sentiment": "positive" if s.score > 0 else "negative",
                "stars": int(s.stars),
                "year": int(pd.Timestamp(s.date).year),
            }
            for s in rows.sort_values("score", ascending=False).itertuples(index=False)
        ]

    def restaurant(self, business_id: str, similar: int = 3) -> dict | None:
        """Everything the detail page shows, or None if unknown."""
        if business_id not in self.restaurants.index:
            return None
        detail = self._card(business_id)
        vec = self.matrix[int(self.restaurants.loc[business_id, "row"])]
        sims = self.matrix @ vec
        rows = [r for r in np.argsort(-sims) if r != self.restaurants.loc[business_id, "row"]]
        by_row = self.restaurants.set_index("row")["business_id"]
        detail["snippets"] = self.snippets_for(business_id)
        detail["similar"] = [self._card(by_row[r]) for r in rows[:similar] if r in by_row.index]
        return detail
