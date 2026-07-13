#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "release/version.json"
MANIFEST_FILE = ROOT / "publication/manifest.json"
GALLERY_FILE = ROOT / "gallery/drinks.json"
PACKAGE_FILE = ROOT / "package.json"
VERSION_MD = ROOT / "release/version.md"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_ones(version: str) -> int:
    parts = version.split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(f"Invalid numeric dotted version: {version}")
    return sum(part == "1" for part in parts)


def main() -> None:
    meta = read_json(VERSION_FILE)
    current = str(meta["current"])
    if current == "1.1.0":
        next_version = "1.1.1"
    else:
        next_version = f"{current}.1"

    ones_count = count_ones(next_version)
    following = f"{next_version}.1"

    meta.update(
        {
            "previous": current,
            "current": next_version,
            "ones_count": ones_count,
            "display": f"{next_version} · единиц: {ones_count}",
            "next": following,
        }
    )
    write_json(VERSION_FILE, meta)

    manifest = read_json(MANIFEST_FILE)
    manifest["version"] = next_version
    manifest["ones_count"] = ones_count
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
        f"Current release: {next_version}\n\n"
        f"Display: {next_version} · единиц: {ones_count}\n\n"
        f"Next release: {following}\n",
        encoding="utf-8",
    )

    release_notes = ROOT / f"release/RELEASE-{next_version}.md"
    if not release_notes.exists():
        release_notes.write_text(
            f"# КВАССИСТЕНТ {next_version}\n\n"
            f"Единиц в версии: **{ones_count}**.\n\n"
            "## Изменения\n\n"
            "- Заполнить перед публикацией.\n",
            encoding="utf-8",
        )

    print(meta["display"])
    print(f"Next: {following}")


if __name__ == "__main__":
    main()
