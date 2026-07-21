#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts/build-publication-safe.py"
COMPANION = ROOT / "companion"


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


def install_companion(version: str) -> Path:
    required = ("index.html", "styles.css", "engine.js", "app.js", "manifest.webmanifest", "icon.svg", "sw.js")
    missing = [name for name in required if not (COMPANION / name).is_file()]
    if missing:
        raise RuntimeError(f"Missing live-batch companion assets: {missing}")

    target = ROOT / f"dist/site/v{version}/companion"
    shutil.copytree(COMPANION, target, dirs_exist_ok=True)
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
.companion-release { margin: 30px 0; padding: clamp(26px,5vw,46px); border-radius: 24px; color: #f6f0df; background: radial-gradient(circle at 90% 5%,rgba(240,187,69,.2),transparent 36%),#17130d; border: 1px solid #67522a; overflow: hidden; }
.companion-release .eyebrow { color: #f0bb45; }
.companion-release h2 { max-width: 780px; margin: 14px 0; color: #fff8e8; font-size: clamp(34px,6vw,64px); line-height: .98; }
.companion-release p { max-width: 720px; color: #c8bea8; }
.companion-benefits { display: grid; grid-template-columns: repeat(auto-fit,minmax(170px,1fr)); gap: 10px; margin: 26px 0; }
.companion-benefits article { padding: 16px; border: 1px solid #433a2c; border-radius: 14px; background: rgba(255,255,255,.035); color: #c8bea8; }
.companion-benefits strong { display: block; margin-bottom: 5px; color: #fff8e8; }
.companion-cta { display: inline-flex; align-items: center; gap: 18px; margin-top: 4px; padding: 15px 20px; border-radius: 999px; color: #17130d; background: #f0bb45; text-decoration: none; font-weight: 850; }
.companion-cta:hover { filter: brightness(1.06); transform: translateY(-1px); }
.companion-actions { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.companion-secondary { color: #f0bb45; font-weight: 750; }
"""
    text = text.replace("</style>", css + "</style>", 1)

    comic_name = f"kvassistent-{version}-comic.svg"
    section = f"""
<section class="companion-release" id="live-batch">
  <div class="eyebrow">Apps for Your Life · ИИ-агент на кухне</div>
  <h2>Один ИИ-агент — одна понятная партия кваса</h2>
  <p>КВАССИСТЕНТ даёт агенту простой рецепт, явное состояние партии и честные правила безопасности. Человек делает квас руками, агент держит контекст и предлагает только следующий шаг.</p>
  <div class="companion-benefits">
    <article><strong>Простой рецепт</strong>Сухари, вода, сахар, температура и семь коротких шагов для первой партии на 3 л.</article>
    <article><strong>Живая партия</strong>Один check-in превращает температуру, запах и поверхность в следующее действие.</article>
    <article><strong>Передача ИИ</strong>Структурированный handoff сохраняет подтверждённые факты и неизвестные, а не выдуманный контекст.</article>
  </div>
  <div class="companion-actions"><a class="companion-cta" href="companion/">Открыть живую партию <span aria-hidden="true">→</span></a><a class="companion-secondary" href="ru/instructions/">Инструкция для ИИ-агента →</a></div>
</section>

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
    companion = ROOT / f"dist/site/v{version}/companion"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="live-batch"',
        'href="companion/"',
        "Один ИИ-агент — одна понятная партия кваса",
        'href="ru/instructions/"',
        "Простой рецепт",
        'id="hot-fermentation"',
        'id="comic-guide"',
        "При 28°C банку убрать с прямого солнца",
        f"kvassistent-{version}-comic.svg",
        "Реальная партия — в простом комиксе",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")
    companion_required = ("index.html", "styles.css", "engine.js", "app.js", "manifest.webmanifest", "icon.svg", "sw.js")
    missing_companion = [name for name in companion_required if not (companion / name).is_file()]
    if missing_companion:
        raise RuntimeError(f"Companion assets were not copied: {missing_companion}")
    companion_text = (companion / "index.html").read_text(encoding="utf-8")
    if "Живая партия" not in companion_text or "Простой квас без догадок" not in companion_text:
        raise RuntimeError("Companion entry point misses the feature title")

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
    install_companion(version)
    patch_landing(version)
    verify(version)
    print(f"Built КВАССИСТЕНТ {meta['display']} with live-batch companion, heat research, and comic guide")


if __name__ == "__main__":
    main()
