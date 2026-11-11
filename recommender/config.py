"""Central settings for the pipeline, scripts and API.

Every value can be overridden with an environment variable (or a line in
.env). Paths are resolved relative to the current working directory, so run
scripts from the repository root.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _path(name: str, default: str) -> Path:
    return Path(_env(name, default)).expanduser()


# --- Paths -------------------------------------------------------------------
DATA_DIR = _path("DATA_DIR", "data")
ARTIFACTS_DIR = _path("ARTIFACTS_DIR", "artifacts")

BUSINESS_JSON = "yelp_academic_dataset_business.json"
REVIEW_JSON = "yelp_academic_dataset_review.json"

RESTAURANTS_FILE = "restaurants.parquet"
REVIEWS_FILE = "reviews.parquet"
PROFILES_FILE = "aspect_profiles.parquet"
ASPECT_SNIPPETS_FILE = "aspect_snippets.parquet"
INDEX_FILE = "restaurants.faiss"
INDEX_IDS_FILE = "restaurant_ids.npy"
REVIEW_SNIPPETS_FILE = "review_snippets.parquet"
REVIEW_SNIPPET_VECTORS_FILE = "review_snippet_vectors.npy"
MODEL_DIRNAME = "restaurant-model"
# ONNX export of the model, used by the API (no PyTorch needed)
ONNX_DIRNAME = "onnx"
MAX_SEQ_LENGTH = 256

# --- Data cleaning (rules from notebooks/02_EDA.ipynb) ------------------------
MIN_CHARS = int(_env("MIN_CHARS", "20"))
MIN_DATE = _env("MIN_DATE", "2015-01-01")
MIN_REVIEWS = int(_env("MIN_REVIEWS", "15"))

# --- NLP --------------------------------------------------------------------
BASE_MODEL = _env("BASE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
ABSA_MODEL = _env("ABSA_MODEL", "yangheng/deberta-v3-base-absa-v1.1")
EMBEDDING_DIM = 384
# Reviews per restaurant used for aspect profiles and restaurant vectors.
REVIEWS_PER_RESTAURANT = int(_env("REVIEWS_PER_RESTAURANT", "50"))
# Review snippets per restaurant kept with vectors for "why it matches".
SNIPPETS_PER_RESTAURANT = int(_env("SNIPPETS_PER_RESTAURANT", "10"))

# --- Ranking ----------------------------------------------------------------
# hybrid = semantic * w_semantic + aspect_fit * w_aspect + rating * w_rating
W_SEMANTIC = float(_env("W_SEMANTIC", "0.5"))
W_ASPECT = float(_env("W_ASPECT", "0.3"))
W_RATING = float(_env("W_RATING", "0.2"))
# Restaurants below this review-count quantile get pulled toward the mean
# rating (the notebook 03 baseline used the 90th percentile).
BASELINE_QUANTILE = float(_env("BASELINE_QUANTILE", "0.90"))
# How many nearest restaurants the vector search returns before re-ranking.
CANDIDATES = int(_env("CANDIDATES", "200"))

# --- Hugging Face Hub ---------------------------------------------------------
HF_REPO_ID = _env("HF_REPO_ID", "")
HF_TOKEN = _env("HF_TOKEN", "") or None

# --- Generative summary -------------------------------------------------------
LLM_PROVIDER = _env("LLM_PROVIDER", "none").lower()
LLM_MODEL = _env("LLM_MODEL", "")
LLM_TIMEOUT_S = float(_env("LLM_TIMEOUT_S", "8"))

# --- API ----------------------------------------------------------------------
ALLOWED_ORIGINS = [
    o.strip() for o in _env("ALLOWED_ORIGINS", "http://localhost:3000").split(",") if o.strip()
]
DATABASE_URL = _env("DATABASE_URL", "sqlite:///feedback.db")


def artifact(name: str) -> Path:
    """Path of a file inside ARTIFACTS_DIR."""
    return ARTIFACTS_DIR / name
