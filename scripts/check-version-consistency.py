#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
version = str(meta["current"])
ones = int(meta["ones_count"])
next_release = int(meta.get("next_release_number", ones + 1))
technical = f"v{version}"
human = f"Версия {ones}"
canonical_path = f"/{technical}/"

assert version.split(".") == ["1"] * ones, (version, ones)
assert meta["display"] == technical
assert meta["technical_label"] == technical
assert meta["human_label"] == human
assert meta["display_ru"] == human
assert meta["next"].split(".") == ["1"] * next_release
assert meta["immutable_url"].endswith(canonical_path)

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert f"**Текущий релиз:** {human}." in readme
assert f"**Следующий релиз:** Версия {next_release}." in readme
assert f"## Что изменилось в версии {ones}" in readme
assert f"Технический номер:** [`{technical}`]" in readme
assert "## Что изменилось в 1.1.1" not in readme

url_pattern = re.compile(r"https://kvassistent\.pages\.dev(/v(?:1\.)*1/)")
for source in (readme, (ROOT / f"release/RELEASE-{version}.md").read_text(encoding="utf-8")):
    found = url_pattern.findall(source)
    assert found, "Expected canonical immutable URL"
    assert all(path == canonical_path for path in found), (found, canonical_path)

finalizer = (ROOT / "scripts/finalize-release.py").read_text(encoding="utf-8")
assert "V25" not in finalizer
assert "релиза 25" not in finalizer
assert "safe-interactions-v25" not in finalizer
assert 'HUMAN = f"Версия {ONES}"' in finalizer
assert 'NEXT_RELEASE = int(META.get("next_release_number", ONES + 1))' in finalizer

builder = (ROOT / "scripts/build-release.py").read_text(encoding="utf-8")
assert 'version_text = f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}. Пересчитай:"' not in builder
assert 'version_text = f"Версия {ones_count}"' in builder

note = ROOT / f"release/RELEASE-{version}.md"
assert note.is_file()
note_text = note.read_text(encoding="utf-8")
assert note_text.startswith(f"# КВАССИСТЕНТ — {human}")
assert technical in note_text
assert f"Версия {next_release}" in note_text

feedback = (ROOT / "feedback/index.html").read_text(encoding="utf-8")
assert f"{human} · результат за полминуты" in feedback
assert f"задачей релиза {next_release}" in feedback
assert 'name="media_url"' in feedback
assert 'href="stories/"' in feedback
assert "Версия 23" not in feedback
assert "релиза 24" not in feedback
assert (ROOT / "feedback/stories/index.html").is_file()

story = (ROOT / "feedback/stories/index.html").read_text(encoding="utf-8")
for marker in ('width="1080" height="1920"', "navigator.canShare", "kvassistent-story.png"):
    assert marker in story, marker

game_i18n = (ROOT / "companion/game/i18n.js").read_text(encoding="utf-8")
for label in (f"КВАССИСТЕНТ {ones}", f"KVASSISTENT {ones}", f"ВЕРСИЯ {ones}", f"VERSION {ones}", f"VERSIÓN {ones}", f"第 {ones} 版", f"ΕΚΔΟΣΗ {ones}"):
    assert label in game_i18n, label
for stale in ("KVASSISTENT 16", "КВАССИСТЕНТ 16", "VERSION 20", "ВЕРСИЯ 20", "VERSIÓN 20", "第 16 版", "ΕΚΔΟΣΗ 20"):
    assert stale not in game_i18n, stale

prepare = (ROOT / "scripts/prepare-release.py").read_text(encoding="utf-8")
for pattern in (r"KVASSISTENT\s+\d+", r"КВАССИСТЕНТ\s+\d+", r"第\s*\d+\s*版"):
    assert pattern in prepare, pattern

assert (ROOT / "V2_PLAN.md").is_file()
print(f"version contract ok: {human} / {technical} / next Версия {next_release}; feedback, stories and game labels verified")
