"""Review ingestion: Yelp Open Dataset JSON -> restaurant and review parquet.

Same logic as the original 01_data_pipeline.py, wrapped in functions so the
scripts and tests can call it with any paths.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
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


# Yelp spells some cities several ways. Map the variants to one name so the
# API's city filter matches the frontend's city list.
CITY_ALIASES = {
    "st. louis": "Saint Louis",
    "st louis": "Saint Louis",
    "saint louis": "Saint Louis",
}


def normalize_city(name: object) -> object:
    """Trim a city name and replace known spelling variants."""
    if not isinstance(name, str):
        return name
    clean = " ".join(name.split())
    return CITY_ALIASES.get(clean.casefold(), clean)


def unify_city_case(cities: pd.Series) -> pd.Series:
    """Spell each city the way most of its rows do: 'TAMPA' and 'tampa' become 'Tampa'."""
    valid = cities.dropna()
    if valid.empty:
        return cities
    keys = valid.str.casefold()
    best = valid.groupby(keys).agg(lambda names: names.value_counts().index[0])
    return cities.map(lambda c: best.get(c.casefold(), c) if isinstance(c, str) else c)


def as_city_list(city: str | Sequence[str] | None) -> list[str]:
    """Accept one city, several cities, or None (all cities)."""
    if city is None:
        return []
    if isinstance(city, str):
        return [city]
    return list(city)


def load_businesses(path: str | Path) -> pd.DataFrame:
    """Read the Yelp business file (one JSON object per line)."""
    return pd.read_json(path, lines=True)


def filter_restaurants(
    business: pd.DataFrame, city: str | Sequence[str] | None = None
) -> pd.DataFrame:
    """Keep businesses whose categories mention 'Restaurant', optionally only some cities.

    City names are normalized (see CITY_ALIASES) before filtering and in the output.
    """
    restaurants = business[business["categories"].str.contains("Restaurant", na=False)]
    restaurants = restaurants.assign(city=unify_city_case(restaurants["city"].map(normalize_city)))
    wanted = {normalize_city(c).casefold() for c in as_city_list(city)}
    if wanted:
        restaurants = restaurants[restaurants["city"].str.casefold().isin(wanted)]
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
    city: str | Sequence[str] | None = None,
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
