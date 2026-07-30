#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
NEXT_RELEASE = int(META.get("next_release_number", ONES + 1))
TECHNICAL = f"v{VERSION}"
HUMAN = f"Версия {ONES}"
IMMUTABLE = f"https://kvassistent.pages.dev/{TECHNICAL}/"

if ONES != 26 or VERSION.split(".") != ["1"] * ONES:
    raise RuntimeError(f"Expected release 26 with 26 ones, got {ONES}: {VERSION}")

finalizer = ROOT / "scripts/finalize-release.py"
text = finalizer.read_text(encoding="utf-8")
replacements = {
    '/* kvassistent-safe-interactions-v25 */': '/* kvassistent-safe-interactions */',
    'picker = \'<span class="header-version-badge" id="header-version-badge" aria-label="KVASSISTENT version 25">V25</span>\' + language_markup()':
        'picker = f\'<span class="header-version-badge" id="header-version-badge" aria-label="KVASSISTENT {HUMAN}">{HUMAN}</span>\' + language_markup()',
    'marker = "kvassistent-safe-interactions-v25"': 'marker = "kvassistent-safe-interactions"',
    '<p>Новые идеи и фотографии становятся задачами релиза 25.</p>':
        '<p>Новые идеи и фотографии становятся задачами релиза {NEXT_RELEASE}.</p>',
    '"kvassistent-safe-interactions-v25"': '"kvassistent-safe-interactions"',
    '"релиза 25"': 'f"релиза {NEXT_RELEASE}"',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Missing finalizer marker: {old}")
    text = text.replace(old, new)
if 'HUMAN = f"Версия {ONES}"' not in text:
    text = text.replace(
        'REPO_URL = "https://github.com/bambuchastudent/kvas-ai-agent"\n',
        'REPO_URL = "https://github.com/bambuchastudent/kvas-ai-agent"\n'
        'HUMAN = f"Версия {ONES}"\n'
        'TECHNICAL = f"v{VERSION}"\n'
        'NEXT_RELEASE = int(META.get("next_release_number", ONES + 1))\n',
        1,
    )
finalizer.write_text(text, encoding="utf-8")

builder = ROOT / "scripts/build-release.py"
text = builder.read_text(encoding="utf-8")
old = 'version_text = f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}. Пересчитай:"\n    version_html = f\'{version_text} <a class="version-link" href="{immutable_path}">v{version}</a>\''
new = 'version_text = f"Версия {ones_count}"\n    version_html = f\'{version_text} · технический номер: <a class="version-link" href="{immutable_path}">v{version}</a>\''
if old not in text:
    raise RuntimeError("Missing verbose landing version text")
builder.write_text(text.replace(old, new), encoding="utf-8")

release_note = ROOT / f"release/RELEASE-{VERSION}.md"
release_note.write_text(
    f"""# КВАССИСТЕНТ — Версия {ONES}

**Технический номер:** `{TECHNICAL}`  
**Следующий релиз:** Версия {NEXT_RELEASE}  
**Immutable release:** `{IMMUTABLE}`

## Что изменилось

- человекочитаемый формат везде: **«Версия {ONES}»**;
- полный номер `{TECHNICAL}` используется только для тега, immutable URL, файлов и машинных метаданных;
- следующий невыпущенный релиз показывается только как **«Версия {NEXT_RELEASE}»**;
- README очищен от старого описания и ссылок версии 9;
- шапка сайта, release notes и Telegram-страница получают номер из `release/version.json`;
- удалены захардкоженные `V25`, «релиза 25» и укороченные immutable URL;
- CI пересчитывает каждый immutable URL и требует ровно {ONES} единиц.

## Канонические формы

- для человека: **Версия {ONES}**;
- технически: `{TECHNICAL}`;
- следующий релиз: **Версия {NEXT_RELEASE}**;
- неизменяемый адрес: `{IMMUTABLE}`.
""",
    encoding="utf-8",
)

checker = ROOT / "scripts/check-version-consistency.py"
checker.write_text(
    r'''#!/usr/bin/env python3
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
assert "потому что в ней единиц" not in builder
assert 'version_text = f"Версия {ones_count}"' in builder

note = ROOT / f"release/RELEASE-{version}.md"
assert note.is_file()
note_text = note.read_text(encoding="utf-8")
assert note_text.startswith(f"# КВАССИСТЕНТ — {human}")
assert technical in note_text
assert f"Версия {next_release}" in note_text

print(f"version contract ok: {human} / {technical} / next Версия {next_release}")
''',
    encoding="utf-8",
)

changelog = ROOT / "AI_CHANGELOG.md"
existing = changelog.read_text(encoding="utf-8")
entry = f"""# AI-readable change log

## 2026-07-30 — KVASSISTENT website release {ONES}

- **Version or scope:** release {ONES}, `{TECHNICAL}`.
- **Changed:** normalized human, technical, next-release and immutable URL representations; replaced stale release-9 README links; made the homepage badge and Telegram wording dynamic; added strict URL-length validation.
- **Why:** the project mixed raw versions, `v`-prefixed versions, short `V25`, stale release-9 headings and shortened immutable URLs such as a 16-unit path.
- **Behavior:** users see `Версия {ONES}`; technical links always use the exact {ONES}-unit `{TECHNICAL}`; the unreleased successor is only `Версия {NEXT_RELEASE}`.
- **Files and systems:** `release/version.json`, `README.md`, `scripts/build-release.py`, `scripts/finalize-release.py`, `scripts/check-version-consistency.py`, release notes, publication CI and generated site.
- **Verification:** exact segment recount, regex validation of every current immutable URL, generator hardcode checks, Python compile and full publication workflow.
- **Deployment:** merge to `develop` publishes release {ONES}.
- **Remaining work:** backend/Telegram repository must report release {ONES} and collect feedback for release {NEXT_RELEASE} before final live verification.

---

"""
if existing.startswith("# AI-readable change log\n"):
    existing = existing[len("# AI-readable change log\n"):].lstrip("\n")
changelog.write_text(entry + existing, encoding="utf-8")

print(f"applied consistent version contract: {HUMAN} / {TECHNICAL}")
