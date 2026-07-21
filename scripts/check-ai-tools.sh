#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failed=0

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'ok  %-10s %s\n' "$command_name" "$(command -v "$command_name")"
  else
    printf 'ERR %-10s not installed\n' "$command_name" >&2
    failed=1
  fi
}

check_file() {
  local file_path="$1"
  if [[ -f "$file_path" ]]; then
    printf 'ok  %s\n' "$file_path"
  else
    printf 'ERR %s is missing\n' "$file_path" >&2
    failed=1
  fi
}

check_command graphify
check_command serena
check_file AGENTS.md
check_file .serena/project.yml
check_file graphify-out/graph.json

if command -v graphify >/dev/null 2>&1; then
  graphify hook status || failed=1
fi

if command -v codex >/dev/null 2>&1; then
  mcp_list="$(codex mcp list 2>/dev/null || true)"
  if printf '%s\n' "$mcp_list" | grep -q '^serena[[:space:]]'; then
    echo "ok  Serena MCP is registered in Codex"
  else
    echo "ERR Serena MCP is not registered in Codex" >&2
    failed=1
  fi
else
  echo "note Codex CLI is unavailable; MCP registration was not checked"
fi

exit "$failed"
