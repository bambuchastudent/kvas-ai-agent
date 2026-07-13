#!/usr/bin/env bash
set -euo pipefail

VERSION="1.1.0"
NAME="kvas"
BRAND="zhizha"
PACKAGE_DIR="dist/${NAME}-${VERSION}"
ARCHIVE_BASENAME="${NAME}-${VERSION}"
FORMAT="${1:-all}"

rm -rf dist
mkdir -p "${PACKAGE_DIR}"

copy_if_exists() {
  local path="$1"
  if [ -e "$path" ]; then
    mkdir -p "${PACKAGE_DIR}/$(dirname "$path")"
    cp -R "$path" "${PACKAGE_DIR}/$path"
  fi
}

copy_if_exists README.md
copy_if_exists README.zh-CN.md
copy_if_exists CHANGELOG.md
copy_if_exists CONTRIBUTING.md
copy_if_exists package.json
copy_if_exists agent-instructions
copy_if_exists recipes
copy_if_exists safety
copy_if_exists docs
copy_if_exists share
copy_if_exists gallery
copy_if_exists release

cat > "${PACKAGE_DIR}/PACKAGE.md" <<EOF
# Kvas ${VERSION}

Brand: Zhizha

This package contains:

- the reproducible kvass protocol;
- Russian and Simplified Chinese project descriptions;
- fermentation safety guidance;
- batch logs and visual-control notes;
- stateful AI-agent instructions in Russian, English, Spanish, German, and Simplified Chinese;
- JSON Schema and example state for agent handoff;
- the Telegram share landing page and Open Graph card source;
- the successful-drinks gallery data and contribution guide;
- release and contribution documents.

Repository: https://github.com/bambuchastudent/kvas-ai-agent
Telegram share page: https://kvassistent.pages.dev/v1.1.0/
EOF

(
  cd dist
  if [ "${FORMAT}" = "zip" ] || [ "${FORMAT}" = "all" ]; then
    zip -r "${ARCHIVE_BASENAME}.zip" "${NAME}-${VERSION}" >/dev/null
  fi
  if [ "${FORMAT}" = "tar" ] || [ "${FORMAT}" = "all" ]; then
    tar -czf "${ARCHIVE_BASENAME}.tar.gz" "${NAME}-${VERSION}"
  fi
)

echo "Package built in dist/:"
ls -la dist
