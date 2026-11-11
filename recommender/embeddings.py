"""Sentence embeddings with the fine-tuned model.

The model is all-MiniLM-L6-v2 fine-tuned on (review, restaurant categories)
pairs in notebooks/finetune.ipynb. Vectors are 384-dimensional and
L2-normalized, so a dot product is the cosine similarity.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np

from recommender import config

# Files a sentence-transformers folder needs to load. The copy first
# committed to Git had only model.safetensors: a global *.json rule in
# .gitignore had silently dropped the rest.
REQUIRED_MODEL_FILES = ("modules.json", "config.json", "model.safetensors", "tokenizer.json")

Encoder = Callable[[Sequence[str]], np.ndarray]


def model_dir(artifacts_dir: str | Path = config.ARTIFACTS_DIR) -> Path:
    return Path(artifacts_dir) / config.MODEL_DIRNAME


def check_model_dir(path: str | Path) -> Path:
    """Raise a clear error if the model folder is incomplete."""
    path = Path(path)
    missing = [name for name in REQUIRED_MODEL_FILES if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(
            f"Model folder {path} is missing {', '.join(missing)}. Re-run the last cells of "
            "notebooks/finetune.ipynb, which save the full folder with model.save()."
        )
    return path


def load_model(path: str | Path | None = None):
    """Load the fine-tuned SentenceTransformer (needs PyTorch)."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(str(check_model_dir(path or model_dir())))


def encode(model, texts: Sequence[str], batch_size: int = 64, progress: bool = False) -> np.ndarray:
    """Encode texts into normalized float32 vectors of shape (n, 384)."""
    vectors = model.encode(
        list(texts),
        batch_size=batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=progress,
    )
    return np.asarray(vectors, dtype=np.float32)


def load_encoder(path: str | Path | None = None) -> Encoder:
    """Return a function texts -> vectors backed by the fine-tuned model."""
    model = load_model(path)
    return lambda texts: encode(model, texts)


# --- Restaurant index ---------------------------------------------------------
def normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return (matrix / np.clip(norms, 1e-12, None)).astype(np.float32)


def restaurant_vectors(
    business_ids: Sequence[str], vectors: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """One vector per restaurant: the normalized mean of its rows' vectors.

    Returns (ids, matrix) with ids sorted, matrix shape (n_restaurants, dim).
    """
    ids = np.asarray(business_ids)
    unique, inverse = np.unique(ids, return_inverse=True)
    sums = np.zeros((len(unique), vectors.shape[1]), dtype=np.float64)
    np.add.at(sums, inverse, vectors)
    counts = np.bincount(inverse).reshape(-1, 1)
    return unique, normalize(sums / counts)


def build_index(matrix: np.ndarray):
    """Exact inner-product index (= cosine on normalized vectors). A few
    thousand restaurants need no approximate index."""
    import faiss

    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(np.ascontiguousarray(matrix, dtype=np.float32))
    return index


def save_index(index, ids: np.ndarray, artifacts_dir: str | Path = config.ARTIFACTS_DIR) -> None:
    import faiss

    artifacts_dir = Path(artifacts_dir)
    faiss.write_index(index, str(artifacts_dir / config.INDEX_FILE))
    np.save(artifacts_dir / config.INDEX_IDS_FILE, ids.astype(str))


def load_index(artifacts_dir: str | Path = config.ARTIFACTS_DIR):
    import faiss

    artifacts_dir = Path(artifacts_dir)
    index = faiss.read_index(str(artifacts_dir / config.INDEX_FILE))
    ids = np.load(artifacts_dir / config.INDEX_IDS_FILE, allow_pickle=False)
    return index, ids


def search(index, ids: np.ndarray, query_vector: np.ndarray, k: int) -> list[tuple[str, float]]:
    """Top-k (business_id, cosine similarity) pairs for one query vector."""
    k = min(k, index.ntotal)
    scores, rows = index.search(query_vector.reshape(1, -1).astype(np.float32), k)
    return [(str(ids[r]), float(s)) for r, s in zip(rows[0], scores[0], strict=True) if r >= 0]
