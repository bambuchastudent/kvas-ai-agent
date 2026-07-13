#!/usr/bin/env python3
from __future__ import annotations

import base64
import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "scripts/build-publication.py"
VERSION_META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
CURRENT_VERSION = str(VERSION_META["current"])
ONES_COUNT = int(VERSION_META["ones_count"])
DISPLAY_VERSION = str(VERSION_META["display"])
NEXT_VERSION = str(VERSION_META["next"])
PROJECT_NAME = "КВАССИСТЕНТ"


def load_builder():
    spec = importlib.util.spec_from_file_location("kvas_publication_builder", ORIGINAL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {ORIGINAL}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def generated_card(path: Path) -> None:
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), (26, 18, 11))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            glow = max(0.0, 1.0 - ((x - 920) ** 2 + (y - 145) ** 2) ** 0.5 / 850)
            pixels[x, y] = (
                int(26 + 58 * glow),
                int(18 + 38 * glow),
                int(11 + 17 * glow),
            )

    draw = ImageDraw.Draw(image)
    title = find_font(76)
    subtitle = find_font(42)
    small = find_font(28)

    draw.rounded_rectangle(
        (55, 55, 1145, 575),
        radius=34,
        fill=(32, 24, 15),
        outline=(238, 181, 63),
        width=3,
    )
    draw.text((92, 105), PROJECT_NAME, font=title, fill=(255, 250, 237))
    draw.text((95, 220), "квас «Жижа» своими руками", font=subtitle, fill=(238, 181, 63))
    draw.text((95, 330), "ЛЮДЯМ + ИИ-АГЕНТАМ", font=subtitle, fill=(255, 250, 237))
    draw.text((95, 430), "PDF + WEB  ·  RU  EN  ES  DE  ZH-CN", font=small, fill=(215, 199, 174))
    draw.text((95, 495), DISPLAY_VERSION, font=small, fill=(238, 181, 63))

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=90, optimize=True, progressive=True)


def safe_build_share_image(root: Path, site: Path) -> None:
    output = site / f"assets/kvassistent-{CURRENT_VERSION}.jpg"
    parts = sorted((root / "share/assets").glob("card-1.0.4.b64.part*"))

    if parts:
        try:
            encoded = "".join(part.read_text(encoding="utf-8") for part in parts)
            encoded = re.sub(r"\s+", "", encoded)
            encoded += "=" * (-len(encoded) % 4)
            data = base64.b64decode(encoded, validate=False)
            if data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9"):
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
                print(f"Recovered Telegram JPEG from {len(parts)} Base64 chunks")
                return
            print("Warning: recovered share-card data is not a complete JPEG; generating fallback")
        except Exception as exc:
            print(f"Warning: cannot recover share-card chunks ({exc}); generating fallback")

    generated_card(output)
    print(f"Generated KVASSISTENT share card: {output}")


def extra_styles() -> str:
    return r"""
.people-quickstart,
.audience-section {
  margin-top: 34px;
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: rgba(255, 253, 247, .94);
  box-shadow: 0 18px 50px rgba(91, 54, 3, .12);
  backdrop-filter: blur(5px);
}
.people-quickstart > h2,
.audience-section > h2 { margin-top: 0; }
.section-kicker {
  display: inline-block;
  margin-bottom: 5px;
  color: var(--gold);
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.section-lead {
  max-width: 790px;
  color: var(--muted);
  font-size: 12.5pt;
}
.quick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 15px;
  margin-top: 22px;
}
.quick-card {
  padding: 19px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: #fffaf0;
}
.quick-card-number {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--gold);
  color: white;
  font-weight: 900;
}
.quick-card h3 { margin: 12px 0 7px; }
.quick-card p { margin: 0; }
.safety-callout {
  margin-top: 18px;
  padding: 16px 18px;
  border-left: 5px solid #9f2d20;
  border-radius: 10px;
  background: #fff0e9;
}
.audience-section.people { border-top: 8px solid #b47718; }
.audience-section.agents { border-top: 8px solid #403b7a; }
.audience-section.agents .section-kicker { color: #403b7a; }
.audience-section.agents .language-card { background: #f7f5ff; }
.audience-links {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 14px;
}
.version-counter {
  display: inline-block;
  margin-left: 7px;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(180, 119, 24, .15);
  color: #7a4c06;
  font-weight: 800;
}
@media (max-width: 640px) {
  .people-quickstart,
  .audience-section { padding: 20px; }
}
"""


def human_cards(manifest: dict[str, Any]) -> str:
    cards: list[str] = []
    for language in manifest["languages"]:
        code = language["code"]
        label = html.escape(language["label"])
        cards.append(
            f"""
<article class="language-card">
  <h2>{label}</h2>
  <p>Краткий рецепт, последовательность действий и правила безопасности для человека.</p>
  <div class="audience-links web-only">
    <a class="button primary" href="{code}/summary/">Открыть для человека</a>
    <a class="button" href="pdfs/kvas-summary-{code}-{CURRENT_VERSION}.pdf">PDF</a>
  </div>
</article>"""
        )
    return "\n".join(cards)


def agent_cards(manifest: dict[str, Any]) -> str:
    cards: list[str] = []
    for language in manifest["languages"]:
        code = language["code"]
        label = html.escape(language["label"])
        cards.append(
            f"""
<article class="language-card">
  <h2>{label}</h2>
  <p>Состояние партии, формат ответа, безопасность, воспроизводимость и передача между агентами.</p>
  <div class="audience-links web-only">
    <a class="button" href="{code}/instructions/">Инструкция ИИ-агента</a>
    <a class="button" href="pdfs/kvas-instructions-{code}-{CURRENT_VERSION}.pdf">PDF</a>
  </div>
</article>"""
        )
    return "\n".join(cards)


def make_selector_html(builder):
    def selector_html(manifest: dict[str, Any], gallery: dict[str, Any], gallery_root: Path) -> str:
        bubbles_html = builder.beer_background_html()
        gallery_section = builder.gallery_html(gallery, gallery_root)
        image_url = f"https://kvassistent.pages.dev/assets/kvassistent-{CURRENT_VERSION}.jpg"
        people = human_cards(manifest)
        agents = agent_cards(manifest)

        return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROJECT_NAME} — домашний квас «Жижа»</title>
<meta name="description" content="КВАССИСТЕНТ: лучшие инструкции для людей и отдельные инструкции для ИИ-агентов. Домашний квас «Жижа» шаг за шагом.">
<meta property="og:type" content="website">
<meta property="og:title" content="{PROJECT_NAME}">
<meta property="og:description" content="Сначала понятные инструкции человеку, затем отдельный раздел для ИИ-агентов.">
<meta property="og:url" content="https://kvassistent.pages.dev/v{CURRENT_VERSION}/">
<meta property="og:image" content="{image_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image_url}">
<style>{builder.stylesheet()}</style>
</head>
<body class="landing-page">
<div class="beer-background web-only" aria-hidden="true">{bubbles_html}</div>
<main>
  <section class="cover">
    <div class="eyebrow">{PROJECT_NAME} · {CURRENT_VERSION}<span class="version-counter">единиц: {ONES_COUNT}</span></div>
    <h1>{PROJECT_NAME}</h1>
    <div class="subtitle">Квас «Жижа» твоими руками.</div>
    <p class="hero-copy">Сначала — короткие и понятные действия для человека. Ниже — отдельная техническая часть для ИИ-агентов, которые ведут состояние партии и не выдумывают пропущенные данные.</p>
    <nav class="hero-actions web-only" aria-label="Быстрые действия">
      <a class="button primary" href="#for-people">Готовить человеку</a>
      <a class="button" href="#for-ai-agents">Инструкция ИИ-агенту</a>
      <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a>
    </nav>
  </section>

  <section class="people-quickstart" id="best-human-instructions">
    <span class="section-kicker">Сначала самое нужное</span>
    <h2>Лучшие инструкции для людей</h2>
    <p class="section-lead">Базовый безопасный путь на 3 литра. Для первой партии используются дрожжи; для следующих можно брать старый квас или осадок.</p>
    <div class="quick-grid">
      <article class="quick-card">
        <span class="quick-card-number">1</span>
        <h3>Собери основу</h3>
        <p>3 л воды, 180–220 г полностью сухих сухарей, 100–120 г сахара или панели. Для первой партии: 0,5–1 г сухих или 2–3 г свежих дрожжей.</p>
      </article>
      <article class="quick-card">
        <span class="quick-card-number">2</span>
        <h3>Сделай настой</h3>
        <p>Поджарь хлеб до тёмно-золотистого цвета, залей кипятком на 4–8 часов и тщательно процеди. Для брожения нужна жидкость, а не хлебная каша.</p>
      </article>
      <article class="quick-card">
        <span class="quick-card-number">3</span>
        <h3>Запусти брожение</h3>
        <p>Добавь сладость, остуди до 25–35°C, внеси закваску и оставь на 8–12 часов под тканью или неплотной крышкой. На жаре проверяй с 6 часов.</p>
      </article>
      <article class="quick-card">
        <span class="quick-card-number">4</span>
        <h3>Дай газ и охлади</h3>
        <p>При нормальном запахе и пузырьках разлей в пластиковые бутылки. Догазируй 2–6 часов. Как бутылка стала твёрдой — сразу в холодильник минимум на 8 часов.</p>
      </article>
    </div>
    <div class="safety-callout"><strong>Не пробовать и вылить:</strong> плесень, пушистый налёт, цветные пятна, слизь, запах гнили, ацетона, мяса или канализации. Основное брожение нельзя закрывать герметично.</div>
  </section>

  <section class="audience-section people" id="for-people">
    <span class="section-kicker">Часть 1</span>
    <h2>Для людей</h2>
    <p class="section-lead">Выбери язык. Здесь только практический рецепт, порядок действий, визуальная проверка и безопасность — без внутренней агентской механики.</p>
    <div class="language-grid">{people}</div>
  </section>

  <section class="audience-section agents" id="for-ai-agents">
    <span class="section-kicker">Часть 2</span>
    <h2>Для ИИ-агентов</h2>
    <p class="section-lead">Отдельный набор инструкций: явное состояние партии, поля `null` для неизвестного, одно следующее действие, safety flags и передача контекста другому агенту.</p>
    <div class="language-grid">{agents}</div>
    <div class="audience-links web-only">
      <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/agent-instructions/state.schema.json">JSON Schema состояния</a>
      <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/agent-instructions/state-example.json">Пример состояния</a>
    </div>
  </section>

  {gallery_section}
</main>
</body>
</html>"""

    return selector_html


def patch_source_reader(builder, source_version: str) -> None:
    original_read_source = builder.read_source

    def read_source(root: Path, rel_path: str, lang: str, doc_type: str):
        release_version = builder.VERSION
        builder.VERSION = source_version
        try:
            doc = original_read_source(root, rel_path, lang, doc_type)
        finally:
            builder.VERSION = release_version
        return builder.SourceDoc(
            doc.lang,
            doc.doc_type,
            doc.title,
            doc.subtitle,
            release_version,
            doc.markdown,
            doc.section_ids,
            doc.path,
        )

    builder.read_source = read_source


def patch_document_pages(builder) -> None:
    original_page_html = builder.page_html

    def page_html(doc, language, manifest):
        result = original_page_html(doc, language, manifest)
        result = result.replace("Kvas - Zhizha -", f"{PROJECT_NAME} ·")
        result = result.replace(
            f"Version {CURRENT_VERSION} · Source of truth:",
            f"Version {CURRENT_VERSION} · единиц: {ONES_COUNT} · Source of truth:",
        )
        return result

    builder.page_html = page_html


def postprocess_manifests(root: Path) -> None:
    paths = [
        root / f"dist/site/v{CURRENT_VERSION}/manifest.json",
        root / "dist/publication/manifest.json",
    ]
    release_data = {
        "version": CURRENT_VERSION,
        "display": DISPLAY_VERSION,
        "ones_count": ONES_COUNT,
        "next": NEXT_VERSION,
        "project": PROJECT_NAME,
    }
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["release"] = release_data
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    version_web = root / f"dist/site/v{CURRENT_VERSION}/version.json"
    version_web.write_text(json.dumps(VERSION_META, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manifest = json.loads((ROOT / "publication/manifest.json").read_text(encoding="utf-8"))
    source_version = str(manifest.get("source_version", CURRENT_VERSION))

    builder = load_builder()
    builder.VERSION = CURRENT_VERSION
    original_stylesheet = builder.stylesheet

    def stylesheet() -> str:
        css = original_stylesheet()
        css = css.replace("Kvas Zhizha 1.1.0", f"{PROJECT_NAME} {DISPLAY_VERSION}")
        return css + extra_styles()

    builder.stylesheet = stylesheet
    builder.selector_html = make_selector_html(builder)
    builder.build_share_image = safe_build_share_image
    patch_source_reader(builder, source_version)
    patch_document_pages(builder)
    builder.main()
    postprocess_manifests(ROOT)


if __name__ == "__main__":
    main()
