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
VERSION = "1.0.6"
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
    if expected_langs != ["ru", "en", "es", "de", "zh-CN"]:
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
    content: "Kvas Zhizha 1.0.6";
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


def selector_html(manifest: dict[str, Any]) -> str:
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
    image_url = f"https://kvassistent.pages.dev/assets/kvas-zhizha-ai-agent-{VERSION}.jpg"
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Квас Жижа для ИИ-агента - {VERSION}</title>
<meta name="description" content="Одинаковые инструкции и краткие описания в PDF и на веб-страницах на пяти языках.">
<meta property="og:type" content="website">
<meta property="og:title" content="Квас Жижа для ИИ-агента">
<meta property="og:description" content="PDF и веб-страницы на русском, английском, испанском, немецком и китайском.">
<meta property="og:url" content="https://kvassistent.pages.dev/v{VERSION}/">
<meta property="og:image" content="{image_url}">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="315">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image_url}">
<style>{stylesheet()}</style>
</head>
<body>
<main>
  <section class="cover">
    <div class="eyebrow">Version {VERSION}</div>
    <h1>Квас Жижа для ИИ-агента</h1>
    <div class="subtitle">Одинаковые инструкции и саммари как PDF и веб-страницы на пяти языках.</div>
  </section>
  <div class="language-grid">{cards_html}</div>
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

    docs: list[SourceDoc] = []
    for language in languages:
        for doc_type in DOC_TYPES:
            docs.append(read_source(root, language[doc_type], language["code"], doc_type))
    validate_parity(docs, languages)

    (site / "index.html").write_text(root_redirect(), encoding="utf-8")
    version_site = site / f"v{VERSION}"
    version_site.mkdir(parents=True)
    (version_site / "index.html").write_text(selector_html(manifest), encoding="utf-8")
    build_share_image(root, site)

    public_manifest: dict[str, Any] = {"version": VERSION, "documents": []}
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
