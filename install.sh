#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="environment.yml"
ENV_NAME=$(grep -E '^name:' "$ENV_FILE" | awk '{print $2}')

echo "[INFO] Creating conda environment '$ENV_NAME'..."
conda env create -f "$ENV_FILE" || {
  echo "[WARN] Environment may already exist. Updating instead..."
  conda env update -f "$ENV_FILE" --prune
}

# Print interpreter path for VS Code setting
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
echo "[INFO] Python interpreter:"
python -c 'import sys; print(sys.executable)'

echo
echo "[DONE] Environment '$ENV_NAME' ready."
echo "       Activate with: conda activate $ENV_NAME"