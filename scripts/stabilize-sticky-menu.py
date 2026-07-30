#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist/site"
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])

OLD_CSS = ".site-topbar{transition:padding .18s ease,border-radius .18s ease,box-shadow .18s ease}"
NEW_CSS = ".site-topbar{transition:none!important;transform:translateZ(0);backface-visibility:hidden;contain:paint}"

OLD_SCRIPT = '''  const sync = () => { if (!topbar) return; const compact = window.scrollY > 120; topbar.classList.toggle("is-compact", compact); if (!compact) setExpanded(false); };
  let last = 0;
  if (toggle) toggle.addEventListener("click", () => { const now = performance.now(); if (now-last < 450) return; last=now; setExpanded(topbar?.dataset.expanded !== "true"); });
  window.addEventListener("scroll", sync, {passive:true}); sync();'''

NEW_SCRIPT = '''  let compact = false;
  let scheduled = false;
  const ENTER_COMPACT_AT = 180;
  const LEAVE_COMPACT_AT = 72;
  const sync = () => {
    scheduled = false;
    if (!topbar) return;
    const y = Math.max(0, window.scrollY || document.documentElement.scrollTop || 0);
    const nextCompact = compact ? y > LEAVE_COMPACT_AT : y >= ENTER_COMPACT_AT;
    if (nextCompact === compact) return;
    compact = nextCompact;
    topbar.classList.toggle("is-compact", compact);
    if (!compact) setExpanded(false);
  };
  const scheduleSync = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(sync);
  };
  let last = 0;
  if (toggle) toggle.addEventListener("click", () => { const now = performance.now(); if (now-last < 450) return; last=now; setExpanded(topbar?.dataset.expanded !== "true"); });
  window.addEventListener("scroll", scheduleSync, {passive:true});
  window.addEventListener("resize", scheduleSync, {passive:true});
  sync();'''

changed = 0
for path in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    if not path.is_file():
        raise RuntimeError(f"Missing homepage: {path}")
    text = path.read_text(encoding="utf-8")
    if OLD_CSS not in text:
        raise RuntimeError(f"Cannot find unstable menu CSS in {path}")
    if OLD_SCRIPT not in text:
        raise RuntimeError(f"Cannot find unstable scroll script in {path}")
    text = text.replace(OLD_CSS, NEW_CSS, 1).replace(OLD_SCRIPT, NEW_SCRIPT, 1)
    path.write_text(text, encoding="utf-8")
    changed += 1

for path in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    text = path.read_text(encoding="utf-8")
    for marker in (
        "ENTER_COMPACT_AT = 180",
        "LEAVE_COMPACT_AT = 72",
        "requestAnimationFrame(sync)",
        "transition:none!important",
        "backface-visibility:hidden",
    ):
        if marker not in text:
            raise RuntimeError(f"Sticky-menu stabilization missing in {path}: {marker}")
    if "window.scrollY > 120" in text:
        raise RuntimeError(f"Old flickering threshold remains in {path}")

print(f"stabilized sticky menu in {changed} homepages for v{VERSION}")
