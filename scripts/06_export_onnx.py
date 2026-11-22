"""Step 6 of the offline pipeline: export the fine-tuned model to ONNX.

The API encodes queries with onnxruntime instead of PyTorch, which keeps
its Docker image and memory small. Run after the model is trained, then
re-run 05_upload_artifacts.py.

The export uses torch.onnx directly rather than optimum, whose exporter
does not import with transformers 5 (as installed on Colab).

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

INPUT_NAMES = ["input_ids", "attention_mask", "token_type_ids"]
TOKENIZER_FILES = [
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "vocab.txt",
    "config.json",
]
# onnxruntime 1.20 (the API's pinned version) reads ONNX IR versions up to 10.
MAX_IR_VERSION = 10
OPSET = 17


def export(source: Path, target: Path) -> None:
    """Write target/model.onnx (outputs last_hidden_state) and the tokenizer files.

    Pooling and normalization stay in OnnxEncoder, as with the sentence-transformers model.
    """
    import onnx
    import torch
    from transformers import AutoModel

    model = AutoModel.from_pretrained(source, attn_implementation="eager").eval()

    class LastHiddenState(torch.nn.Module):
        def __init__(self, inner):
            super().__init__()
            self.inner = inner

        def forward(self, input_ids, attention_mask, token_type_ids):
            out = self.inner(
                input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
            )
            return out.last_hidden_state

    target.mkdir(parents=True)
    onnx_path = target / "model.onnx"
    dummy = tuple(torch.ones(1, 8, dtype=torch.long) for _ in INPUT_NAMES)
    dynamic = {name: {0: "batch", 1: "tokens"} for name in [*INPUT_NAMES, "last_hidden_state"]}
    with torch.no_grad():
        torch.onnx.export(
            LastHiddenState(model),
            dummy,
            str(onnx_path),
            input_names=INPUT_NAMES,
            output_names=["last_hidden_state"],
            dynamic_axes=dynamic,
            opset_version=OPSET,
            dynamo=False,
        )

    graph = onnx.load(str(onnx_path))
    if graph.ir_version > MAX_IR_VERSION:
        graph.ir_version = MAX_IR_VERSION
        onnx.save(graph, str(onnx_path))

    for name in TOKENIZER_FILES:
        if (source / name).exists():
            shutil.copy(source / name, target / name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the model to ONNX.")
    parser.add_argument("--artifacts", default=str(config.ARTIFACTS_DIR))
    args = parser.parse_args()

    source = embeddings.check_model_dir(embeddings.model_dir(args.artifacts))
    target = embeddings.onnx_dir(args.artifacts)
    shutil.rmtree(target, ignore_errors=True)
    export(source, target)

    reference = embeddings.encode(embeddings.load_model(source), CHECK_SENTENCES)
    exported = embeddings.OnnxEncoder(target)(CHECK_SENTENCES)
    agreement = float(np.min(np.sum(reference * exported, axis=1)))
    print(f"Exported to {target}. Lowest cosine between PyTorch and ONNX vectors: {agreement:.5f}")
    if agreement < 0.999:
        sys.exit("ONNX vectors differ from the PyTorch model: do not upload this export.")


if __name__ == "__main__":
    main()
