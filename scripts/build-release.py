#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import shutil
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


def install_comic(version: str) -> Path:
    source = ROOT / f"share/kvassistent-{version}-comic.svg"
    if not source.is_file():
        raise RuntimeError(f"Missing comic source: {source}")

    target = ROOT / f"dist/site/v{version}/assets/kvassistent-{version}-comic.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def patch_landing(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    marker = '<section class="audience-section people" id="for-people">'
    if marker not in text:
        raise RuntimeError("Cannot find human section marker in landing page")

    css = """
.heat-release,
.comic-release { margin: 30px 0; padding: 26px; border-radius: 18px; }
.heat-release { border: 2px solid #d48a18; background: #fff5dc; }
.comic-release { border: 2px solid #493a8a; background: #f6f3ff; }
.heat-release h2,
.comic-release h2 { margin-top: 0; }
.heat-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 12px; }
.heat-grid article { padding: 14px; border-radius: 12px; background: #fffdf7; border: 1px solid #e7c98d; }
.heat-danger { margin-top: 15px; padding: 14px; border-left: 5px solid #a52b20; background: #fff0ea; }
.comic-release figure { margin: 22px 0 0; }
.comic-release img { display: block; width: min(100%, 860px); height: auto; margin: 0 auto; border: 3px solid #2b244d; border-radius: 18px; background: #f8efd7; box-shadow: 0 20px 55px rgba(43,36,77,.18); }
.comic-release figcaption { max-width: 860px; margin: 12px auto 0; color: var(--muted); }
"""
    text = text.replace("</style>", css + "</style>", 1)

    comic_name = f"kvassistent-{version}-comic.svg"
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

<section class="comic-release" id="comic-guide">
  <div class="eyebrow">Версия {version} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>Схема собрана по фотогалерее этой партии: подготовка сухарей, замачивание, перелив в бутыль, открытое брожение под тканью и проверка примерно через сутки при 28°C.</p>
  <p><strong>Главная мысль:</strong> не закупоривать первичное брожение, не держать бутыль на прямом солнце и перед розливом проверить запах, поверхность и вкус.</p>
  <figure>
    <a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="Схематический комикс КВАССИСТЕНТА: шесть этапов приготовления кваса" loading="lazy"></a>
    <figcaption>Векторная SVG-схема остаётся чёткой на телефоне и при увеличении. Нажми, чтобы открыть отдельно.</figcaption>
  </figure>
</section>
"""
    text = text.replace(marker, section + marker, 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    comic = ROOT / f"dist/site/v{version}/assets/kvassistent-{version}-comic.svg"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="hot-fermentation"',
        'id="comic-guide"',
        "При 28°C банку убрать с прямого солнца",
        "около 2,2–2,6%",
        "примерно 370 г",
        f"kvassistent-{version}-comic.svg",
        "Реальная партия — в простом комиксе",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")

    manifest = json.loads((ROOT / "publication/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("visual_guide") != f"share/kvassistent-{version}-comic.svg":
        raise RuntimeError("Manifest visual_guide does not match current release")
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
    install_comic(version)
    patch_landing(version)
    verify(version)
    print(f"Built КВАССИСТЕНТ {meta['display']} with heat research and comic guide")


if __name__ == "__main__":
    main()
