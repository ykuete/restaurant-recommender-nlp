"""Download the API's artifacts from the private Hugging Face Hub repo.

The API container starts empty: on startup it fetches the files below into
ARTIFACTS_DIR, unless they are already there (local runs, docker-compose
with a mounted artifacts/ folder).
"""

from __future__ import annotations

from pathlib import Path

from recommender import config

# Data files the API reads (also what 05_upload_artifacts.py uploads).
DATA_FILES = [
    config.RESTAURANTS_FILE,
    config.PROFILES_FILE,
    config.ASPECT_SNIPPETS_FILE,
    config.INDEX_FILE,
    config.INDEX_IDS_FILE,
    config.REVIEW_SNIPPETS_FILE,
    config.REVIEW_SNIPPET_VECTORS_FILE,
]
# The API encodes queries with the ONNX export only.
API_PATTERNS = [*DATA_FILES, f"{config.ONNX_DIRNAME}/*"]
# The upload also keeps the full model, for retraining and the ONNX export.
UPLOAD_PATTERNS = [*API_PATTERNS, f"{config.MODEL_DIRNAME}/**"]


def missing(artifacts_dir: str | Path) -> list[str]:
    a = Path(artifacts_dir)
    needed = [*DATA_FILES, f"{config.ONNX_DIRNAME}/model.onnx"]
    return [name for name in needed if not (a / name).exists()]


def ensure_artifacts(
    artifacts_dir: str | Path = config.ARTIFACTS_DIR,
    repo_id: str = config.HF_REPO_ID,
    token: str | None = config.HF_TOKEN,
) -> Path:
    """Make sure the API's files are in artifacts_dir, downloading if needed."""
    artifacts_dir = Path(artifacts_dir)
    if not missing(artifacts_dir):
        return artifacts_dir
    if not repo_id:
        raise RuntimeError(
            f"Missing {', '.join(missing(artifacts_dir))} in {artifacts_dir} and HF_REPO_ID is "
            "not set. Run the scripts in scripts/ or set HF_REPO_ID and HF_TOKEN."
        )
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id=repo_id,
        local_dir=artifacts_dir,
        allow_patterns=API_PATTERNS,
        token=token,
    )
    if still := missing(artifacts_dir):
        raise RuntimeError(f"{repo_id} does not contain {', '.join(still)}")
    return artifacts_dir
