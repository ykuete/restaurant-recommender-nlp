"""Step 3 of the offline pipeline: embeddings and the restaurant vector index.

Encodes the most recent reviews of each restaurant (plus one
"Restaurant categories: ..." line, the anchor format the model was trained
on), averages them into one vector per restaurant and stores a FAISS index.
It also keeps up to SNIPPETS_PER_RESTAURANT reviews per restaurant, with
float16 vectors, to pick the review that best matches a query.

Usage (from the repository root):
    python scripts/03_build_index.py
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from recommender import config, embeddings  # noqa: E402
from recommender.preprocessing import clean_reviews, latest_reviews  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the restaurant vector index.")
    parser.add_argument("--artifacts", default=str(config.ARTIFACTS_DIR))
    parser.add_argument("--per-restaurant", type=int, default=config.REVIEWS_PER_RESTAURANT)
    parser.add_argument("--snippets", type=int, default=config.SNIPPETS_PER_RESTAURANT)
    args = parser.parse_args()

    artifacts = Path(args.artifacts)
    restaurants = pd.read_parquet(artifacts / config.RESTAURANTS_FILE)
    reviews = clean_reviews(pd.read_parquet(artifacts / config.REVIEWS_FILE))
    reviews = latest_reviews(reviews, args.per_restaurant).reset_index(drop=True)
    restaurants = restaurants[restaurants["business_id"].isin(reviews["business_id"])]

    model = embeddings.load_model(embeddings.model_dir(artifacts))
    start = time.time()
    print(f"Encoding {len(reviews)} reviews for {len(restaurants)} restaurants...")
    review_vecs = embeddings.encode(model, reviews["text"].tolist(), progress=True)
    anchors = ("Restaurant categories: " + restaurants["categories"].fillna("")).tolist()
    anchor_vecs = embeddings.encode(model, anchors)

    ids, matrix = embeddings.restaurant_vectors(
        reviews["business_id"].tolist() + restaurants["business_id"].tolist(),
        np.vstack([review_vecs, anchor_vecs]),
    )
    embeddings.save_index(embeddings.build_index(matrix), ids, artifacts)

    # Snippet store: the most recent reviews already encoded above.
    snippet_rows = latest_reviews(reviews, args.snippets)
    snippet_vecs = review_vecs[snippet_rows.index.to_numpy()].astype(np.float16)
    snippets = snippet_rows[["business_id", "review_id", "stars", "date", "text"]].copy()
    snippets["text"] = snippets["text"].str.slice(0, 400)
    snippets.reset_index(drop=True).to_parquet(artifacts / config.REVIEW_SNIPPETS_FILE, index=False)
    np.save(artifacts / config.REVIEW_SNIPPET_VECTORS_FILE, snippet_vecs)

    size_mb = (
        sum(
            (artifacts / f).stat().st_size
            for f in (
                config.INDEX_FILE,
                config.REVIEW_SNIPPET_VECTORS_FILE,
                config.REVIEW_SNIPPETS_FILE,
            )
        )
        / 1e6
    )
    print(
        f"Indexed {len(ids)} restaurants and {len(snippets)} snippets "
        f"({size_mb:.0f} MB) in {time.time() - start:.0f} s"
    )


if __name__ == "__main__":
    main()
