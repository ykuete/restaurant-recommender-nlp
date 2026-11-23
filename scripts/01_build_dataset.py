"""Step 1 of the offline pipeline: Yelp JSON -> restaurants/reviews parquet.

Usage (from the repository root):
    python scripts/01_build_dataset.py
    python scripts/01_build_dataset.py --city Philadelphia   # small dev dataset
    python scripts/01_build_dataset.py --city Philadelphia Tampa "New Orleans"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from recommender import config  # noqa: E402
from recommender.pipeline import build_dataset  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--data-dir", default=str(config.DATA_DIR), help="folder with the Yelp JSON"
    )
    parser.add_argument("--out", default=str(config.ARTIFACTS_DIR), help="output folder")
    parser.add_argument(
        "--city",
        nargs="+",
        default=None,
        help='keep only these cities, e.g. --city Philadelphia Tampa "New Orleans"',
    )
    args = parser.parse_args()

    print(f"Reading Yelp files from {args.data_dir} ...")
    restaurants, reviews = build_dataset(
        args.data_dir,
        args.out,
        city=args.city,
        business_file=config.BUSINESS_JSON,
        review_file=config.REVIEW_JSON,
        restaurants_name=config.RESTAURANTS_FILE,
        reviews_name=config.REVIEWS_FILE,
    )
    print(f"Wrote {restaurants} and {reviews}")
    counts = pd.read_parquet(restaurants, columns=["city"])["city"].value_counts()
    print("Restaurants per city:")
    print(counts.to_string())


if __name__ == "__main__":
    main()
