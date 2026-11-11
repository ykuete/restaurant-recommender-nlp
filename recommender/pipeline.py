"""Review ingestion: Yelp Open Dataset JSON -> restaurant and review parquet.

Same logic as the original 01_data_pipeline.py, wrapped in functions so the
scripts and tests can call it with any paths.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RESTAURANT_COLUMNS = [
    "business_id",
    "name",
    "city",
    "state",
    "stars",
    "review_count",
    "is_open",
    "attributes",
    "categories",
]


def load_businesses(path: str | Path) -> pd.DataFrame:
    """Read the Yelp business file (one JSON object per line)."""
    return pd.read_json(path, lines=True)


def filter_restaurants(business: pd.DataFrame, city: str | None = None) -> pd.DataFrame:
    """Keep businesses whose categories mention 'Restaurant', optionally one city."""
    restaurants = business[business["categories"].str.contains("Restaurant", na=False)]
    if city:
        restaurants = restaurants[restaurants["city"].str.casefold() == city.casefold()]
    return restaurants[RESTAURANT_COLUMNS].reset_index(drop=True)


def load_reviews(
    path: str | Path, business_ids: set[str], chunk_size: int = 100_000
) -> pd.DataFrame:
    """Read the large review file in chunks, keeping reviews of the given businesses."""
    chunks = []
    for chunk in pd.read_json(path, lines=True, chunksize=chunk_size):
        chunks.append(chunk[chunk["business_id"].isin(business_ids)])
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, ignore_index=True)


def build_dataset(
    data_dir: str | Path,
    out_dir: str | Path,
    city: str | None = None,
    business_file: str = "yelp_academic_dataset_business.json",
    review_file: str = "yelp_academic_dataset_review.json",
    restaurants_name: str = "restaurants.parquet",
    reviews_name: str = "reviews.parquet",
) -> tuple[Path, Path]:
    """Run the full ingestion and return the two parquet paths it wrote."""
    data_dir, out_dir = Path(data_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    restaurants = filter_restaurants(load_businesses(data_dir / business_file), city)
    reviews = load_reviews(data_dir / review_file, set(restaurants["business_id"]))

    # attributes is a nested dict per row; store it as JSON text so parquet
    # keeps a stable schema.
    restaurants = restaurants.assign(
        attributes=restaurants["attributes"].apply(
            lambda a: json.dumps(a) if isinstance(a, dict) else None
        )
    )

    restaurants_path = out_dir / restaurants_name
    reviews_path = out_dir / reviews_name
    restaurants.to_parquet(restaurants_path, index=False)
    reviews.to_parquet(reviews_path, index=False)
    return restaurants_path, reviews_path
