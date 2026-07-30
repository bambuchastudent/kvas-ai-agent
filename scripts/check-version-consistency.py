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

print(f"version contract ok: {human} / {technical} / next Версия {next_release}")
