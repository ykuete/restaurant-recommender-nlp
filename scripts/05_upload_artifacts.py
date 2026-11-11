"""Step 5 of the offline pipeline: publish the artifacts to a PRIVATE
Hugging Face Hub repo, so the API can download them at startup.

The repo must stay private: the parquet files and snippets contain Yelp
review text, and the Yelp licence forbids redistributing the dataset.

Usage (from the repository root, with HF_REPO_ID and a WRITE token in .env):
    python scripts/05_upload_artifacts.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from recommender import config  # noqa: E402

# Only what the API needs. The raw reviews.parquet stays local.
API_FILES = [
    config.RESTAURANTS_FILE,
    config.PROFILES_FILE,
    config.ASPECT_SNIPPETS_FILE,
    config.INDEX_FILE,
    config.INDEX_IDS_FILE,
    config.REVIEW_SNIPPETS_FILE,
    config.REVIEW_SNIPPET_VECTORS_FILE,
    f"{config.MODEL_DIRNAME}/**",
    f"{config.ONNX_DIRNAME}/**",
]


def main() -> None:
    from huggingface_hub import HfApi

    parser = argparse.ArgumentParser(description="Upload artifacts to a private Hub repo.")
    parser.add_argument("--artifacts", default=str(config.ARTIFACTS_DIR))
    parser.add_argument("--repo-id", default=config.HF_REPO_ID)
    args = parser.parse_args()
    if not args.repo_id:
        sys.exit("Set HF_REPO_ID in .env (e.g. your-username/tastelens-artifacts).")

    api = HfApi(token=config.HF_TOKEN)
    api.create_repo(args.repo_id, repo_type="model", private=True, exist_ok=True)
    if not api.repo_info(args.repo_id).private:
        sys.exit(f"{args.repo_id} is public. Make it private on the Hub before uploading.")

    api.upload_folder(
        repo_id=args.repo_id,
        folder_path=args.artifacts,
        allow_patterns=API_FILES,
        commit_message="Update recommender artifacts",
    )
    print(f"Uploaded artifacts to https://huggingface.co/{args.repo_id} (private)")


if __name__ == "__main__":
    main()
