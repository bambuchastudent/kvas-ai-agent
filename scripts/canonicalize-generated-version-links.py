#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist/site"
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
CANONICAL_PREFIX = f"/v{VERSION}/"
LANGUAGES = ("ru", "en", "es", "de", "zh-CN", "el")
TYPES = ("summary", "instructions")

if VERSION.split(".") != ["1"] * ONES:
    raise RuntimeError(f"Broken canonical version metadata: {VERSION} / {ONES}")
if not SITE.is_dir():
    raise RuntimeError(f"Generated site is missing: {SITE}")

language_group = "|".join(re.escape(value) for value in LANGUAGES)
type_group = "|".join(re.escape(value) for value in TYPES)
localized_route_pattern = re.compile(
    rf"/v(?P<old>(?:1\.)*1)/(?P<language>{language_group})/(?P<kind>{type_group})/"
)
version_prefix_pattern = re.compile(r"/v(?P<old>(?:1\.)*1)/")
language_payload_pattern = re.compile(
    r'(?P<open><script id="kvass-language-data"[^>]*>)(?P<body>.*?)(?P<close></script>)',
    re.S,
)

changed_files = 0
replacements = 0
stale_examples: list[str] = []

for path in SITE.rglob("*.html"):
    before = path.read_text(encoding="utf-8")

    def replace_localized_route(match: re.Match[str]) -> str:
        original = match.group(0)
        if match.group("old") == VERSION:
            return original
        stale_examples.append(original)
        return f"{CANONICAL_PREFIX}{match.group('language')}/{match.group('kind')}/"

    after = localized_route_pattern.sub(replace_localized_route, before)

    def replace_payload(payload_match: re.Match[str]) -> str:
        body = payload_match.group("body")

        def replace_prefix(version_match: re.Match[str]) -> str:
            original = version_match.group(0)
            if version_match.group("old") == VERSION:
                return original
            stale_examples.append(original)
            return CANONICAL_PREFIX

        canonical_body = version_prefix_pattern.sub(replace_prefix, body)
        return payload_match.group("open") + canonical_body + payload_match.group("close")

    after = language_payload_pattern.sub(replace_payload, after)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed_files += 1
        before_stale = [
            match.group(0)
            for match in version_prefix_pattern.finditer(before)
            if match.group("old") != VERSION
        ]
        after_stale = [
            match.group(0)
            for match in version_prefix_pattern.finditer(after)
            if match.group("old") != VERSION
        ]
        replacements += max(0, len(before_stale) - len(after_stale))

for path in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    text = path.read_text(encoding="utf-8")
    payload_match = language_payload_pattern.search(text)
    if payload_match:
        stale_payload = [
            match.group(0)
            for match in version_prefix_pattern.finditer(payload_match.group("body"))
            if match.group("old") != VERSION
        ]
        if stale_payload:
            raise RuntimeError(f"Stale immutable links remain in language payload {path}: {stale_payload[:5]}")
    stale_routes = [
        match.group(0)
        for match in localized_route_pattern.finditer(text)
        if match.group("old") != VERSION
    ]
    if stale_routes:
        raise RuntimeError(f"Stale localized routes remain in {path}: {stale_routes[:5]}")

print(
    f"canonicalized {replacements} embedded release links in {changed_files} files "
    f"for Версия {ONES}: v{VERSION}"
)
if stale_examples:
    print("replaced examples:", ", ".join(sorted(set(stale_examples))[:4]))
