#!/usr/bin/env bash
set -euo pipefail
# Untrack the model weights and macOS files. The files stay on disk.
git rm -r --cached --ignore-unmatch src/restaurant-model-finetuned src/restaurant-model-checkpoints
find . -name .DS_Store -not -path './.git/*' -print0 | xargs -0 git rm --cached --ignore-unmatch
