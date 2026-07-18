#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts/build-publication-safe.py"


def load_core():
    spec = importlib.util.spec_from_file_location("kvassistent_publication_core", CORE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {CORE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def patch_landing(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    marker = '<section class="audience-section people" id="for-people">'
    if marker not in text:
        raise RuntimeError("Cannot find human section marker in landing page")

    css = """
.heat-release { margin: 30px 0; padding: 26px; border: 2px solid #d48a18; border-radius: 18px; background: #fff5dc; }
.heat-release h2 { margin-top: 0; }
.heat-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 12px; }
.heat-grid article { padding: 14px; border-radius: 12px; background: #fffdf7; border: 1px solid #e7c98d; }
.heat-danger { margin-top: 15px; padding: 14px; border-left: 5px solid #a52b20; background: #fff0ea; }
"""
    text = text.replace("</style>", css + "</style>", 1)

    section = f"""
<section class="heat-release" id="hot-fermentation">
  <div class="eyebrow">Версия {version} · жара и солнце</div>
  <h2>При 28°C банку убрать с прямого солнца</h2>
  <p>28°C в тени — быстрый рабочий режим. Солнце может нагреть жидкость выше температуры воздуха. Измеряй именно жидкость и проверяй квас через 4–6 часов.</p>
  <div class="heat-grid">
    <article><strong>18–24°C</strong><br>спокойный режим</article>
    <article><strong>25–27°C</strong><br>проверка с 6 часов</article>
    <article><strong>28–30°C</strong><br>только тень, проверка с 4 часов</article>
    <article><strong>31°C+</strong><br>переставить в прохладу</article>
  </div>
  <p><strong>Про «8% за две недели»:</strong> жара и время не создают алкоголь без сахара. Для 3 л 100–120 г сахара дают теоретический максимум около 2,2–2,6% об. только из добавленного сахара; для теоретических 8% нужно примерно 370 г ферментируемого сахара.</p>
  <div class="heat-danger"><strong>Сейчас:</strong> убрать банку с солнца, прикрыть чистой тканью или неплотной крышкой и измерить температуру жидкости.</div>
</section>
"""
    text = text.replace(marker, section + marker, 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="hot-fermentation"',
        "При 28°C банку убрать с прямого солнца",
        "около 2,2–2,6%",
        "примерно 370 г",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses heat release content: {missing}")

    manifest = json.loads((ROOT / "publication/manifest.json").read_text(encoding="utf-8"))
    for language in manifest["languages"]:
        for key in ("summary", "instructions"):
            source = (ROOT / language[key]).read_text(encoding="utf-8")
            if "<!-- section:heat -->" not in source or "<!-- section:alcohol -->" not in source:
                raise RuntimeError(f"Missing heat/alcohol sections: {language[key]}")


def main() -> None:
    meta = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
    version = str(meta["current"])
    core = load_core()
    core.main()
    patch_landing(version)
    verify(version)
    print(f"Built КВАССИСТЕНТ {meta['display']} with heat and alcohol boundaries")


if __name__ == "__main__":
    main()
