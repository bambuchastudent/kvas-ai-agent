#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

echo "Installing or updating Graphify and Serena..."
uv tool install --upgrade graphifyy
uv tool install --upgrade -p 3.13 serena-agent

echo "Connecting Graphify to Codex and Git..."
graphify codex install
graphify hook install

if [[ ! -f .serena/project.yml ]]; then
  echo "Creating Serena project configuration..."
  serena project create --name kvas-ai-agent --language python --language bash .
fi

echo "Connecting Serena to Codex..."
serena setup codex

echo "Building the local knowledge graph..."
if [[ -f graphify-out/graph.json ]]; then
  graphify update .
else
  graphify extract . --code-only --no-cluster
fi

echo "Indexing symbols for Serena..."
serena project index

echo "AI tooling is ready. Run: npm run ai:check"
