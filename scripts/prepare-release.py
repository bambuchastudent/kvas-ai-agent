#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
ONES = int(META["ones_count"])
VERSION = str(META["current"])

TARGETS = (
    ROOT / "scripts/build-release.py",
    ROOT / "companion/game/index.html",
    ROOT / "companion/game/i18n.js",
    ROOT / "companion/sw.js",
    ROOT / "gallery/drinks.json",
)

PATTERNS = (
    (r"VERSION\s+\d+", f"VERSION {ONES}"),
    (r"ВЕРСИЯ\s+\d+", f"ВЕРСИЯ {ONES}"),
    (r"VERSIÓN\s+\d+", f"VERSIÓN {ONES}"),
    (r"版本\s*\d+", f"版本 {ONES}"),
    (r"ΕΚΔΟΣΗ\s+\d+", f"ΕΚΔΟΣΗ {ONES}"),
    (r"kvassistent-live-v\d+", f"kvassistent-live-v{ONES}"),
    (r"release\s+\d+\s+content", f"release {ONES} content"),
)

for path in TARGETS:
    if not path.is_file():
        continue
    before = path.read_text(encoding="utf-8")
    after = before
    for pattern, replacement in PATTERNS:
        after = re.sub(pattern, replacement, after)
    if path.name == "drinks.json":
        after = re.sub(r'("version"\s*:\s*)\d+', rf'\g<1>{ONES}', after)
        after = re.sub(r'("release"\s*:\s*")[^"]+("\s*)', rf'\g<1>{VERSION}\2', after)
    if after != before:
        path.write_text(after, encoding="utf-8")
        print(f"prepared {path.relative_to(ROOT)} for version {ONES}")

print(f"KVASSISTENT release {ONES}: v{VERSION}")
