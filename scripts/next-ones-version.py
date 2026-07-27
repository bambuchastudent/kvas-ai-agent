#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "release/version.json"
MANIFEST_FILE = ROOT / "publication/manifest.json"
GALLERY_FILE = ROOT / "gallery/drinks.json"
PACKAGE_FILE = ROOT / "package.json"
VERSION_MD = ROOT / "release/version.md"
PUBLIC_BASE = "https://kvassistent.pages.dev"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_ones(version: str) -> int:
    parts = version.split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(f"Invalid numeric dotted version: {version}")
    return sum(part == "1" for part in parts)


def russian_display(version: str, ones_count: int) -> str:
    return f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}. Пересчитай: v{version}"


def main() -> None:
    meta = read_json(VERSION_FILE)
    current = str(meta["current"])
    next_version = "1.1.1" if current == "1.1.0" else f"{current}.1"
    ones_count = count_ones(next_version)
    following = f"{next_version}.1"
    immutable_url = f"{PUBLIC_BASE}/v{next_version}/"

    meta.update(
        {
            "previous": current,
            "current": next_version,
            "ones_count": ones_count,
            "display": f"v{next_version}",
            "display_ru": russian_display(next_version, ones_count),
            "latest_url": f"{PUBLIC_BASE}/",
            "immutable_url": immutable_url,
            "game_url": f"{PUBLIC_BASE}/game/",
            "companion_url": f"{PUBLIC_BASE}/companion/",
            "next": following,
        }
    )
    write_json(VERSION_FILE, meta)

    manifest = read_json(MANIFEST_FILE)
    manifest["version"] = next_version
    manifest["ones_count"] = ones_count
    manifest["latest_urls"] = {
        "home": f"{PUBLIC_BASE}/",
        "game": f"{PUBLIC_BASE}/game/",
        "companion": f"{PUBLIC_BASE}/companion/",
        "feedback": f"{PUBLIC_BASE}/feedback/",
    }
    visual_guide = manifest.get("visual_guide")
    if isinstance(visual_guide, str) and visual_guide:
        source_guide = ROOT / visual_guide
        next_guide = Path("share") / f"kvassistent-{next_version}-comic.svg"
        if not source_guide.is_file():
            raise FileNotFoundError(f"Missing current visual guide: {source_guide}")
        shutil.copy2(source_guide, ROOT / next_guide)
        manifest["visual_guide"] = next_guide.as_posix()
    write_json(MANIFEST_FILE, manifest)

    gallery = read_json(GALLERY_FILE)
    gallery["version"] = next_version
    write_json(GALLERY_FILE, gallery)

    package = read_json(PACKAGE_FILE)
    package["kvassistentRelease"] = next_version
    package["onesCount"] = ones_count
    write_json(PACKAGE_FILE, package)

    VERSION_MD.write_text(
        "# Version\n\n"
        f"Current immutable release: `v{next_version}`\n\n"
        f"> {russian_display(next_version, ones_count)}\n\n"
        f"Latest: `{PUBLIC_BASE}/`\n\n"
        f"Game: `{PUBLIC_BASE}/game/`\n\n"
        f"Live batch: `{PUBLIC_BASE}/companion/`\n\n"
        f"Next immutable release: `v{following}`\n",
        encoding="utf-8",
    )

    release_notes = ROOT / f"release/RELEASE-{next_version}.md"
    if not release_notes.exists():
        release_notes.write_text(
            f"# КВАССИСТЕНТ {next_version}\n\n"
            f"**{russian_display(next_version, ones_count)}**\n\n"
            "## Изменения\n\n"
            "- Заполнить перед публикацией.\n",
            encoding="utf-8",
        )

    print(meta["display_ru"])
    print(f"Latest: {meta['latest_url']}")
    print(f"Immutable: {meta['immutable_url']}")
    print(f"Next: {following}")


if __name__ == "__main__":
    main()
