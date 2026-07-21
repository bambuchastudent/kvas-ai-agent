#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import shutil
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mistune
from pypdf import PdfReader
from weasyprint import CSS, HTML

SECTION_RE = re.compile(r"<!--\s*section:([a-z0-9-]+)\s*-->")
VERSION = "1.1.0"
DOC_TYPES = ("summary", "instructions")


@dataclass(frozen=True)
class SourceDoc:
    lang: str
    doc_type: str
    title: str
    subtitle: str
    version: str
    markdown: str
    section_ids: tuple[str, ...]
    path: Path


def parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML-like front matter")
    try:
        _, front, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{path}: invalid front matter") from exc
    meta: dict[str, str] = {}
    for line in front.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}: invalid front matter line: {line}")
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.strip() + "\n"


def read_source(root: Path, rel_path: str, lang: str, doc_type: str) -> SourceDoc:
    path = root / rel_path
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text, path)
    expected = {
        "lang": lang,
        "doc_type": doc_type,
        "version": VERSION,
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            raise ValueError(f"{path}: {key}={meta.get(key)!r}, expected {value!r}")
    title = meta.get("title", "").strip()
    subtitle = meta.get("subtitle", "").strip()
    if not title or not subtitle:
        raise ValueError(f"{path}: title and subtitle are required")
    section_ids = tuple(SECTION_RE.findall(body))
    if not section_ids:
        raise ValueError(f"{path}: no section markers found")
    if len(section_ids) != len(set(section_ids)):
        raise ValueError(f"{path}: duplicate section markers")
    clean = SECTION_RE.sub("", body)
    return SourceDoc(lang, doc_type, title, subtitle, VERSION, clean, section_ids, path)


def validate_parity(docs: list[SourceDoc], languages: list[dict[str, str]]) -> None:
    expected_langs = [item["code"] for item in languages]
    if expected_langs != ["ru", "en", "es", "de", "zh-CN", "el"]:
        raise ValueError(f"Unexpected language order: {expected_langs}")

    for doc_type in DOC_TYPES:
        typed = [doc for doc in docs if doc.doc_type == doc_type]
        if [doc.lang for doc in typed] != expected_langs:
            raise ValueError(f"Missing or misordered {doc_type} documents")
        baseline = typed[0].section_ids
        for doc in typed[1:]:
            if doc.section_ids != baseline:
                raise ValueError(
                    f"Section mismatch in {doc.path}: {doc.section_ids} != {baseline}"
                )


def stylesheet() -> str:
    return r"""
@page {
  size: A4;
  margin: 20mm 18mm 22mm;
  @bottom-left {
    content: "Kvas Zhizha 1.1.0";
    font-size: 8.5pt;
    color: #746856;
  }
  @bottom-right {
    content: "Page " counter(page) " / " counter(pages);
    font-size: 8.5pt;
    color: #746856;
  }
}
:root {
  --ink: #2a2118;
  --muted: #6f6252;
  --gold: #b47718;
  --paper: #fffdf7;
  --soft: #f4ead7;
  --border: #dbc9a9;
}
* { box-sizing: border-box; }
html { background: var(--paper); }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: "Noto Sans", "Noto Sans CJK SC", "DejaVu Sans", sans-serif;
  font-size: 11pt;
  line-height: 1.55;
}
main { max-width: 920px; margin: 0 auto; padding: 30px; }
.cover {
  border: 1px solid var(--border);
  border-top: 8px solid var(--gold);
  background: linear-gradient(145deg, #fffdf7, #f8efdd);
  padding: 34px;
  margin-bottom: 30px;
  border-radius: 14px;
}
.eyebrow { color: var(--gold); font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
h1 { font-size: 30pt; line-height: 1.08; margin: 12px 0; }
.subtitle { color: var(--muted); font-size: 15pt; }
.hero-copy {
  max-width: 760px;
  margin: 16px 0 0;
  font-size: 12.5pt;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}
.button.primary {
  border-color: var(--gold);
  background: var(--gold);
  color: #fffdf7;
}
.meta { color: var(--muted); margin-top: 18px; font-size: 9.5pt; }
h2 {
  font-size: 18pt;
  margin-top: 28px;
  padding-bottom: 6px;
  border-bottom: 2px solid var(--soft);
  break-after: avoid;
}
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 24px; }
li { margin: 4px 0; }
code {
  font-family: "Noto Sans Mono", "DejaVu Sans Mono", monospace;
  font-size: .9em;
  background: #f1e7d6;
  padding: 1px 4px;
  border-radius: 4px;
}
pre {
  background: #211a13;
  color: #fff8e8;
  padding: 14px;
  border-radius: 8px;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}
a { color: #8c5600; }
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0 30px;
}
.nav a, .button {
  display: inline-block;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 9px;
  text-decoration: none;
  background: #fffaf0;
  color: var(--ink);
  font-weight: 700;
}
.language-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
.language-card {
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  background: #fffaf0;
}
.language-card h2 { margin-top: 0; border: 0; }
.downloads { margin-top: 14px; }
.landing-page {
  min-height: 100vh;
  background: #f2b632;
}
.landing-page main {
  position: relative;
  z-index: 2;
}
.landing-page .cover,
.landing-page .language-card,
.landing-page .gallery {
  background: rgba(255, 253, 247, .91);
  box-shadow: 0 18px 50px rgba(91, 54, 3, .13);
  backdrop-filter: blur(5px);
}
.beer-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background:
    radial-gradient(circle at 50% -10%, rgba(255, 246, 166, .95), transparent 38%),
    linear-gradient(180deg, #ffd969 0%, #efb42f 54%, #d99113 100%);
}
.beer-bubble {
  position: absolute;
  left: var(--x);
  bottom: -14vh;
  width: var(--size);
  height: var(--size);
  border: 2px solid rgba(255, 255, 235, .72);
  border-radius: 50%;
  background: rgba(255, 247, 190, .18);
  box-shadow: inset 3px 3px 6px rgba(255, 255, 255, .42), 0 0 14px rgba(255, 244, 164, .2);
  animation: bubble-rise var(--duration) linear var(--delay) infinite;
}
@keyframes bubble-rise {
  0% { transform: translate3d(0, 0, 0) scale(.7); opacity: 0; }
  10% { opacity: .8; }
  55% { transform: translate3d(var(--drift), -58vh, 0) scale(1); }
  100% { transform: translate3d(0, -125vh, 0) scale(1.12); opacity: 0; }
}
.gallery {
  margin-top: 46px;
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: 18px;
}
.gallery > h2 { margin-top: 0; }
.gallery-intro { max-width: 760px; color: var(--muted); font-size: 12pt; }
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 18px;
  margin-top: 22px;
}
.gallery-card,
.gallery-empty {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: #fffaf0;
}
.gallery-card img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
.gallery-card-content { padding: 18px; }
.gallery-card h3 { margin: 0 0 8px; }
.gallery-empty {
  display: grid;
  grid-template-columns: minmax(210px, .8fr) minmax(260px, 1.2fr);
  grid-column: 1 / -1;
}
.gallery-empty-visual {
  display: grid;
  place-items: center;
  min-height: 250px;
  background: linear-gradient(160deg, #ffd95f, #c9780c);
}
.kvass-glass {
  position: relative;
  width: 92px;
  height: 150px;
  border: 5px solid rgba(255,255,255,.88);
  border-top-width: 2px;
  border-radius: 8px 8px 24px 24px;
  background: linear-gradient(180deg, #8b4a0a 0%, #4d2207 100%);
  box-shadow: inset 12px 0 18px rgba(255, 206, 82, .22), 0 15px 26px rgba(62, 28, 2, .3);
}
.kvass-glass::before {
  content: "";
  position: absolute;
  inset: 7px 5px auto;
  height: 18px;
  border-radius: 50%;
  background: #f7d88a;
  box-shadow: 0 4px 0 rgba(255,255,255,.35);
}
.kvass-glass::after {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  left: 24px;
  bottom: 32px;
  border: 2px solid rgba(255,255,255,.62);
  border-radius: 50%;
  box-shadow: 30px -22px 0 -2px rgba(255,255,255,.62), 14px -52px 0 -3px rgba(255,255,255,.62);
}
.gallery-empty-copy { padding: 28px; align-self: center; }
.gallery-empty-copy h3 { margin-top: 0; font-size: 17pt; }
.gallery-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
@media (max-width: 640px) {
  main { padding: 16px; }
  .cover { padding: 24px; }
  .gallery-empty { grid-template-columns: 1fr; }
  .gallery-empty-visual { min-height: 190px; }
}
@media (prefers-reduced-motion: reduce) {
  .beer-bubble { animation: none; opacity: .42; transform: translateY(-35vh); }
}
@media print {
  main { padding: 0; }
  .web-only { display: none !important; }
  .cover { break-after: page; }
}
"""


def render_markdown(md: str) -> str:
    renderer = mistune.create_markdown(plugins=["table", "strikethrough", "url"])
    return renderer(md)


def page_html(doc: SourceDoc, language: dict[str, str], manifest: dict[str, Any]) -> str:
    lang = language["code"]
    label = language["label"]
    other = "instructions" if doc.doc_type == "summary" else "summary"
    other_label = "Instructions" if other == "instructions" else "Summary"
    pdf_name = f"kvas-{doc.doc_type}-{lang}-{VERSION}.pdf"
    title = html.escape(doc.title)
    subtitle = html.escape(doc.subtitle)
    body = render_markdown(doc.markdown)
    canonical = f"https://kvassistent.pages.dev/v{VERSION}/{lang}/{doc.doc_type}/"
    return f"""<!doctype html>
<html lang="{html.escape(language['html_lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{subtitle}">
<link rel="canonical" href="{canonical}">
<style>{stylesheet()}</style>
</head>
<body>
<main>
  <section class="cover">
    <div class="eyebrow">Kvas - Zhizha - {html.escape(label)}</div>
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
    <div class="meta">Version {VERSION} · Source of truth: publication/{lang}/{doc.doc_type}.md</div>
  </section>
  <nav class="nav web-only">
    <a href="../../">Languages</a>
    <a href="../{other}/">{other_label}</a>
    <a href="../../pdfs/{pdf_name}">PDF</a>
    <a href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a>
  </nav>
  <article>{body}</article>
</main>
</body>
</html>"""


def beer_background_html() -> str:
    bubbles = (
        (4, 18, -2, 17, 22), (10, 34, -8, 23, -28), (17, 12, -4, 14, 18),
        (23, 52, -15, 28, 34), (31, 24, -11, 18, -21), (39, 15, -5, 16, 26),
        (47, 42, -19, 25, -35), (54, 20, -7, 15, 19), (61, 31, -14, 22, 30),
        (69, 13, -3, 13, -16), (75, 47, -21, 27, 38), (82, 22, -9, 18, -24),
        (89, 36, -16, 24, 31), (95, 16, -6, 15, -18),
    )
    return "".join(
        f'<span class="beer-bubble" style="--x:{x}%;--size:{size}px;--delay:{delay}s;--duration:{duration}s;--drift:{drift}px"></span>'
        for x, size, delay, duration, drift in bubbles
    )


def gallery_html(gallery: dict[str, Any], gallery_root: Path) -> str:
    drinks = gallery.get("drinks", [])
    cards: list[str] = []
    for drink in drinks:
        title = html.escape(str(drink.get("title", "Удачная партия")))
        description = html.escape(str(drink.get("description", "")))
        author = html.escape(str(drink.get("author", "Участник сообщества")))
        image_path = Path(str(drink.get("image", "")))
        if not image_path.parts or image_path.is_absolute() or ".." in image_path.parts:
            raise ValueError(f"Invalid gallery image path: {image_path}")
        if not (gallery_root / image_path).is_file():
            raise ValueError(f"Missing gallery image: {gallery_root / image_path}")
        recipe_url = html.escape(str(drink.get("recipe_url", "")), quote=True)
        recipe_link = f'<p><a href="{recipe_url}">Рецепт и журнал партии</a></p>' if recipe_url else ""
        cards.append(f"""
<article class="gallery-card">
  <img src="gallery/{html.escape(image_path.as_posix(), quote=True)}" alt="{title}" loading="lazy">
  <div class="gallery-card-content">
    <h3>{title}</h3>
    <p>{description}</p>
    <p><strong>Автор:</strong> {author}</p>
    {recipe_link}
  </div>
</article>""")

    if cards:
        content = f'<div class="gallery-grid">{"".join(cards)}</div>'
    else:
        content = """
<div class="gallery-grid">
  <div class="gallery-empty">
    <div class="gallery-empty-visual" aria-hidden="true"><div class="kvass-glass"></div></div>
    <div class="gallery-empty-copy">
      <h3>Первое место ждёт твою «Жижу»</h3>
      <p>Пришли фотографию удачной партии, пропорции, время брожения и короткую заметку о вкусе. После проверки напиток появится здесь с указанием автора.</p>
      <div class="gallery-actions web-only">
        <a class="button primary" href="https://github.com/bambuchastudent/kvas-ai-agent/issues/new">Добавить свой напиток</a>
        <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/gallery/README.md">Как оформить результат</a>
      </div>
    </div>
  </div>
</div>"""

    return f"""
<section class="gallery" id="gallery">
  <h2>Галерея успешных напитков</h2>
  <p class="gallery-intro">Реальные партии сообщества: фотография, проверенный рецепт и заметки о результате. Галерея пополняется только настоящими напитками — без выдуманных примеров.</p>
  {content}
</section>"""


def selector_html(manifest: dict[str, Any], gallery: dict[str, Any], gallery_root: Path) -> str:
    cards = []
    for language in manifest["languages"]:
        code = language["code"]
        label = html.escape(language["label"])
        cards.append(f"""
<div class="language-card">
  <h2>{label}</h2>
  <p><a class="button" href="{code}/summary/">Summary</a></p>
  <p><a class="button" href="{code}/instructions/">AI agent instructions</a></p>
  <div class="downloads">
    <a href="pdfs/kvas-summary-{code}-{VERSION}.pdf">Summary PDF</a><br>
    <a href="pdfs/kvas-instructions-{code}-{VERSION}.pdf">Instructions PDF</a>
  </div>
</div>""")
    cards_html = "\n".join(cards)
    bubbles_html = beer_background_html()
    gallery_section = gallery_html(gallery, gallery_root)
    image_url = f"https://kvassistent.pages.dev/assets/kvas-zhizha-ai-agent-{VERSION}.jpg"
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Твой личный Квассистент — квас «Жижа» твоими руками</title>
<meta name="description" content="Квассистент помогает тебе приготовить домашний квас «Жижа» своими руками: ведёт по шагам, помнит состояние партии и подсказывает, что делать дальше.">
<meta property="og:type" content="website">
<meta property="og:title" content="Твой личный Квассистент">
<meta property="og:description" content="Приготовь квас «Жижа» своими руками — Квассистент проведёт тебя по всему процессу.">
<meta property="og:url" content="https://kvassistent.pages.dev/v{VERSION}/">
<meta property="og:image" content="{image_url}">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="315">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image_url}">
<style>{stylesheet()}</style>
</head>
<body class="landing-page">
<div class="beer-background web-only" aria-hidden="true">{bubbles_html}</div>
<main>
  <section class="cover">
    <div class="eyebrow">Квассистент · Версия {VERSION}</div>
    <h1>Твой личный Квассистент</h1>
    <div class="subtitle">Готовит квас «Жижа» твоими руками.</div>
    <p class="hero-copy">Он проведёт тебя по рецепту шаг за шагом, запомнит состояние текущей партии и вовремя подскажет, что делать дальше. Ты готовишь настоящий домашний квас — Квассистент помогает не сбиться.</p>
    <nav class="hero-actions web-only" aria-label="Быстрые действия">
      <a class="button primary" href="ru/instructions/">Начать готовить</a>
      <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent">Поддержать проект своим рецептом</a>
    </nav>
  </section>
  <h2>Выбери язык и формат</h2>
  <div class="language-grid">{cards_html}</div>
  {gallery_section}
</main>
</body>
</html>"""


def root_redirect() -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=v{VERSION}/"><link rel="canonical" href="v{VERSION}/"><title>Kvas {VERSION}</title></head><body><a href="v{VERSION}/">Kvas {VERSION}</a></body></html>"""


def build_share_image(root: Path, site: Path) -> None:
    parts = sorted((root / "share/assets").glob("card-1.0.4.b64.part*"))
    if not parts:
        return
    encoded = "".join(p.read_text(encoding="utf-8") for p in parts)
    encoded = re.sub(r"\s+", "", encoded)
    data = base64.b64decode(encoded, validate=True)
    if not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
        raise ValueError("Share card is not a complete JPEG")
    assets = site / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / f"kvas-zhizha-ai-agent-{VERSION}.jpg").write_bytes(data)


def validate_pdf(path: Path, title: str) -> None:
    if path.stat().st_size < 8_000:
        raise ValueError(f"PDF too small: {path}")
    reader = PdfReader(str(path))
    if not reader.pages:
        raise ValueError(f"PDF has no pages: {path}")
    metadata_title = (reader.metadata.title or "") if reader.metadata else ""
    if title not in metadata_title:
        raise ValueError(f"Unexpected PDF title metadata for {path}: {metadata_title!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    out = (args.out or root / "dist").resolve()
    site = out / "site"
    pdf_dir = out / "publication"
    shutil.rmtree(out, ignore_errors=True)
    site.mkdir(parents=True)
    pdf_dir.mkdir(parents=True)

    manifest = json.loads((root / "publication/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        raise ValueError("Manifest version mismatch")
    languages: list[dict[str, str]] = manifest["languages"]
    gallery = json.loads((root / "gallery/drinks.json").read_text(encoding="utf-8"))
    if gallery.get("version") != VERSION:
        raise ValueError("Gallery version mismatch")

    docs: list[SourceDoc] = []
    for language in languages:
        for doc_type in DOC_TYPES:
            docs.append(read_source(root, language[doc_type], language["code"], doc_type))
    validate_parity(docs, languages)

    (site / "index.html").write_text(root_redirect(), encoding="utf-8")
    version_site = site / f"v{VERSION}"
    version_site.mkdir(parents=True)
    (version_site / "index.html").write_text(
        selector_html(manifest, gallery, root / "gallery"), encoding="utf-8"
    )
    gallery_assets = root / "gallery/assets"
    if gallery_assets.exists():
        shutil.copytree(gallery_assets, version_site / "gallery/assets")
    build_share_image(root, site)

    public_manifest: dict[str, Any] = {
        "version": VERSION,
        "gallery": {"count": len(gallery.get("drinks", [])), "web": "#gallery"},
        "documents": [],
    }
    css = CSS(string=stylesheet())

    for doc in docs:
        language = next(item for item in languages if item["code"] == doc.lang)
        html_text = page_html(doc, language, manifest)
        web_dir = version_site / doc.lang / doc.doc_type
        web_dir.mkdir(parents=True, exist_ok=True)
        (web_dir / "index.html").write_text(html_text, encoding="utf-8")
        lang_dir = version_site / doc.lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        if not (lang_dir / "index.html").exists():
            (lang_dir / "index.html").write_text(
                f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=summary/"><a href="summary/">{html.escape(language["label"])}</a>',
                encoding="utf-8",
            )

        pdf_name = f"kvas-{doc.doc_type}-{doc.lang}-{VERSION}.pdf"
        pdf_path = pdf_dir / pdf_name
        HTML(string=html_text, base_url=str(root)).write_pdf(
            str(pdf_path),
            stylesheets=[css],
            presentational_hints=True,
            metadata={"title": doc.title, "author": "Kvas Zhizha", "subject": doc.subtitle},
        )
        validate_pdf(pdf_path, doc.title)
        public_manifest["documents"].append(
            {
                "language": doc.lang,
                "type": doc.doc_type,
                "title": doc.title,
                "sections": list(doc.section_ids),
                "pdf": f"pdfs/{pdf_name}",
                "web": f"{doc.lang}/{doc.doc_type}/",
            }
        )

    pdf_site = version_site / "pdfs"
    pdf_site.mkdir(parents=True)
    for pdf in pdf_dir.glob("*.pdf"):
        shutil.copy2(pdf, pdf_site / pdf.name)

    (version_site / "manifest.json").write_text(
        json.dumps(public_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (pdf_dir / "manifest.json").write_text(
        json.dumps(public_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    zip_path = out / f"kvas-{VERSION}-publication.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(pdf_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(out))
        for path in sorted((root / "publication").rglob("*.md")):
            zf.write(path, Path("sources") / path.relative_to(root / "publication"))

    tar_path = out / f"kvas-{VERSION}-publication.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(pdf_dir, arcname="publication")
        tf.add(root / "publication", arcname="sources")

    print(f"Built {len(docs)} PDFs and {len(docs)} web pages")
    print(f"Site: {site}")
    print(f"PDFs: {pdf_dir}")


if __name__ == "__main__":
    main()
