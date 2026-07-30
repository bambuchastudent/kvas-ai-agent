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
pattern = re.compile(
    rf"/v(?P<old>(?:1\.)*1)/(?P<language>{language_group})/(?P<kind>{type_group})/"
)

changed_files = 0
replacements = 0
stale_examples: list[str] = []

for path in SITE.rglob("*.html"):
    before = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        nonlocal_replacement = match.group(0)
        old = match.group("old")
        if old == VERSION:
            return nonlocal_replacement
        stale_examples.append(nonlocal_replacement)
        return f"{CANONICAL_PREFIX}{match.group('language')}/{match.group('kind')}/"

    after, count = pattern.subn(replace, before)
    if count:
        actual = sum(1 for match in pattern.finditer(before) if match.group("old") != VERSION)
        if actual:
            path.write_text(after, encoding="utf-8")
            changed_files += 1
            replacements += actual

for path in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    text = path.read_text(encoding="utf-8")
    stale = [match.group(0) for match in pattern.finditer(text) if match.group("old") != VERSION]
    if stale:
        raise RuntimeError(f"Stale localized immutable links remain in {path}: {stale[:5]}")
    for language in LANGUAGES:
        for kind in TYPES:
            expected = f"{CANONICAL_PREFIX}{language}/{kind}/"
            if expected not in text:
                raise RuntimeError(f"Missing canonical localized link in {path}: {expected}")

print(
    f"canonicalized {replacements} localized release links in {changed_files} files "
    f"for Версия {ONES}: v{VERSION}"
)
if stale_examples:
    print("replaced examples:", ", ".join(sorted(set(stale_examples))[:4]))
