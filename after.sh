#!/usr/bin/env bash
set -euo pipefail
# The patch moves the tracked files. Move the untracked model folders
# out of src/ into artifacts/ (git-ignored), then remove the empty src/.
mkdir -p artifacts
for d in src/restaurant-model-finetuned src/restaurant-model-checkpoints; do
  [ -d "$d" ] && mv "$d" artifacts/
done
find src -name .DS_Store -delete 2>/dev/null || true
rmdir src 2>/dev/null || true
