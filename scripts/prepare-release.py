#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
ONES = int(META["ones_count"])
VERSION = str(META["current"])

TEXT_TARGETS = (
    ROOT / "scripts/build-release.py",
    ROOT / "companion/game/index.html",
    ROOT / "companion/game/i18n.js",
    ROOT / "companion/sw.js",
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

for path in TEXT_TARGETS:
    if not path.is_file():
        continue
    before = path.read_text(encoding="utf-8")
    after = before
    for pattern, replacement in PATTERNS:
        after = re.sub(pattern, replacement, after)
    if after != before:
        path.write_text(after, encoding="utf-8")
        print(f"prepared {path.relative_to(ROOT)} for version {ONES}")

gallery_path = ROOT / "gallery/drinks.json"
if gallery_path.is_file():
    gallery = json.loads(gallery_path.read_text(encoding="utf-8"))
    if gallery.get("version") != VERSION:
        gallery["version"] = VERSION
        gallery_path.write_text(
            json.dumps(gallery, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"prepared {gallery_path.relative_to(ROOT)} for v{VERSION}")

manifest_path = ROOT / "publication/manifest.json"
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    previous_visual = str(manifest.get("visual_guide", ""))
    target_visual_rel = f"share/kvassistent-{VERSION}-comic.svg"
    target_visual = ROOT / target_visual_rel

    if not target_visual.is_file():
        source_visual = ROOT / previous_visual if previous_visual else None
        if source_visual is None or not source_visual.is_file():
            raise RuntimeError(
                f"Missing release comic {target_visual_rel} and no reusable visual guide: {previous_visual!r}"
            )
        target_visual.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_visual, target_visual)
        print(
            f"copied {source_visual.relative_to(ROOT)} to {target_visual.relative_to(ROOT)}"
        )

    changed = False
    for key, value in (
        ("version", VERSION),
        ("ones_count", ONES),
        ("visual_guide", target_visual_rel),
    ):
        if manifest.get(key) != value:
            manifest[key] = value
            changed = True

    if changed:
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"prepared {manifest_path.relative_to(ROOT)} for v{VERSION}")

print(f"KVASSISTENT release {ONES}: v{VERSION}")
