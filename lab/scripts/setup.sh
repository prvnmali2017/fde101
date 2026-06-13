#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> RetailCo FDE Lab Setup"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "    Created .env from .env.example"
fi

if [ ! -d .venv ]; then
  echo "==> Creating virtual environment"
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "==> Ingesting policy documents into ChromaDB"
export XDG_CACHE_HOME="$(pwd)/data/cache"
export CHROMA_CACHE_DIR="$(pwd)/data/chroma-cache"
mkdir -p "$XDG_CACHE_HOME" "$CHROMA_CACHE_DIR"
python -m src.ingest.rag

echo ""
echo "Setup complete. Run:"
echo "  source .venv/bin/activate"
echo "  uvicorn src.api.main:app --reload --port 8000"
echo ""
echo "Then open http://localhost:8000"
