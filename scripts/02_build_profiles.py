"""Step 2 of the offline pipeline: aspect-based sentiment profiles.

Reads reviews.parquet, applies the cleaning rules, scores the most recent
reviews of each restaurant per aspect, and writes aspect_profiles.parquet
and aspect_snippets.parquet.

Usage (from the repository root):
    python scripts/02_build_profiles.py                 # CPU
    python scripts/02_build_profiles.py --device 0      # first GPU (e.g. Colab)
    python scripts/02_build_profiles.py --max-restaurants 200   # quick test run
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from recommender import config  # noqa: E402
from recommender.preprocessing import clean_reviews  # noqa: E402
from recommender.sentiment import AspectSentimentScorer, build_profiles  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build aspect sentiment profiles.")
    parser.add_argument("--artifacts", default=str(config.ARTIFACTS_DIR))
    parser.add_argument("--device", type=int, default=-1, help="-1 = CPU, 0 = first GPU")
    parser.add_argument("--per-restaurant", type=int, default=config.REVIEWS_PER_RESTAURANT)
    parser.add_argument("--max-restaurants", type=int, default=None, help="limit for test runs")
    args = parser.parse_args()

    artifacts = Path(args.artifacts)
    reviews = clean_reviews(pd.read_parquet(artifacts / config.REVIEWS_FILE))
    if args.max_restaurants:
        keep = reviews["business_id"].drop_duplicates().head(args.max_restaurants)
        reviews = reviews[reviews["business_id"].isin(keep)]
    n = reviews["business_id"].nunique()
    print(f"Scoring aspects for {n} restaurants ({args.per_restaurant} reviews each at most)...")

    start = time.time()
    scorer = AspectSentimentScorer(device=args.device)
    profiles, snippets = build_profiles(reviews, scorer, per_restaurant=args.per_restaurant)

    profiles.to_parquet(artifacts / config.PROFILES_FILE, index=False)
    snippets.to_parquet(artifacts / config.ASPECT_SNIPPETS_FILE, index=False)
    print(f"Wrote {len(profiles)} profile rows and {len(snippets)} snippets "
          f"in {time.time() - start:.0f} s")


if __name__ == "__main__":
    main()
