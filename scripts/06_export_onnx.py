"""Step 6 of the offline pipeline: export the fine-tuned model to ONNX.

The API encodes queries with onnxruntime instead of PyTorch, which keeps
its Docker image and memory small. Run after the model is trained, then
re-run 05_upload_artifacts.py.

Needs the ML extras: pip install -r requirements-ml.txt

Usage (from the repository root):
    python scripts/06_export_onnx.py
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from recommender import config, embeddings

CHECK_SENTENCES = [
    "quiet date-night spot with great pasta",
    "fast, cheap lunch",
    "The waiter was rude but the tacos were amazing.",
    "brunch with great coffee and no long wait",
]


def main() -> None:
    from optimum.exporters.onnx import main_export

    parser = argparse.ArgumentParser(description="Export the model to ONNX.")
    parser.add_argument("--artifacts", default=str(config.ARTIFACTS_DIR))
    args = parser.parse_args()

    source = embeddings.check_model_dir(embeddings.model_dir(args.artifacts))
    target = embeddings.onnx_dir(args.artifacts)
    shutil.rmtree(target, ignore_errors=True)
    # Plain transformer graph (last_hidden_state); pooling happens in OnnxEncoder.
    main_export(str(source), output=target, task="feature-extraction", library_name="transformers")

    reference = embeddings.encode(embeddings.load_model(source), CHECK_SENTENCES)
    exported = embeddings.OnnxEncoder(target)(CHECK_SENTENCES)
    agreement = float(np.min(np.sum(reference * exported, axis=1)))
    print(f"Exported to {target}. Lowest cosine between PyTorch and ONNX vectors: {agreement:.5f}")
    if agreement < 0.999:
        sys.exit("ONNX vectors differ from the PyTorch model: do not upload this export.")


if __name__ == "__main__":
    main()
