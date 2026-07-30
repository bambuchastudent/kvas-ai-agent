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

    visual_text = target_visual.read_text(encoding="utf-8")
    prepared_visual = re.sub(r"VERSION\s+\d+", f"VERSION {ONES}", visual_text)
    prepared_visual = re.sub(r"version\s+\d+", f"version {ONES}", prepared_visual)
    prepared_visual = re.sub(r"Версия\s+\d+", f"Версия {ONES}", prepared_visual)
    if prepared_visual != visual_text:
        target_visual.write_text(prepared_visual, encoding="utf-8")
        print(f"prepared {target_visual.relative_to(ROOT)} labels for version {ONES}")

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

package_path = ROOT / "package.json"
if package_path.is_file():
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package["kvassistentRelease"] = VERSION
    package["onesCount"] = ONES
    package["description"] = (
        "KVASSISTENT: human-first AI for manual kvass craft with simple language routing, "
        "a compact mobile menu, GitHub coding-agent context, and Telegram feedback via Cloudflare Pages."
    )
    package.setdefault("scripts", {})["finalize:release"] = "python scripts/finalize-release.py"
    files = package.setdefault("files", [])
    for required in (
        "PROJECT_GOAL.md",
        ".github/copilot-instructions.md",
        "scripts/finalize-release.py",
    ):
        if required not in files:
            files.append(required)
    package_path.write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"prepared {package_path.relative_to(ROOT)} for v{VERSION}")

finalizer = ROOT / "scripts/finalize-release.py"
enhancer = ROOT / "scripts/enhance-release.py"
hook_marker = "# KVASSISTENT_FINALIZE_HOOK"
if finalizer.is_file() and enhancer.is_file():
    finalizer_text = finalizer.read_text(encoding="utf-8")
    strict_head_guard = '''    if "</head>" not in text:
        raise RuntimeError(f"HTML page has no closing head: {path}")
    text = text.replace("</head>", metadata + "</head>", 1)
'''
    redirect_safe_guard = '''    if "</head>" not in text:
        # Redirect wrappers intentionally omit a full document head.
        # Their canonical destination receives discovery and social metadata.
        return
    text = text.replace("</head>", metadata + "</head>", 1)
'''
    if strict_head_guard in finalizer_text:
        finalizer_text = finalizer_text.replace(strict_head_guard, redirect_safe_guard, 1)
        finalizer.write_text(finalizer_text, encoding="utf-8")
        print("prepared finalizer to skip metadata injection for redirect wrappers")
    elif redirect_safe_guard not in finalizer_text:
        raise RuntimeError("Cannot locate redirect metadata head guard in finalizer")

    compile(finalizer_text, str(finalizer), "exec")
    enhancer_text = enhancer.read_text(encoding="utf-8")
    if hook_marker not in enhancer_text:
        enhancer_text += (
            "\n\n"
            + hook_marker
            + "\nimport runpy as _kvassistent_runpy\n"
            + '_kvassistent_runpy.run_path(str(ROOT / "scripts/finalize-release.py"), '
            + 'run_name="__kvassistent_finalize__")\n'
        )
        enhancer.write_text(enhancer_text, encoding="utf-8")
        print("attached release finalizer to scripts/enhance-release.py")

print(f"KVASSISTENT release {ONES}: v{VERSION}")
