#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
SITE = ROOT / "dist/site"
BOT_URL = "https://t.me/kvassistent_bot"
REPO_URL = "https://github.com/bambuchastudent/kvas-ai-agent"

LANGUAGES = {
    "ru": {"label": "Русский", "short": "RU", "summary": "/ru/summary/"},
    "en": {"label": "English", "short": "EN", "summary": "/en/summary/"},
    "es": {"label": "Español", "short": "ES", "summary": "/es/summary/"},
    "de": {"label": "Deutsch", "short": "DE", "summary": "/de/summary/"},
    "zh-CN": {"label": "简体中文", "short": "中文", "summary": "/zh-CN/summary/"},
    "el": {"label": "Ελληνικά", "short": "EL", "summary": "/el/summary/"},
}

ACCESSIBILITY_CSS = r"""
/* kvassistent-safe-interactions-v24 */
:where(button,a,[role="button"],input,select,textarea,summary){touch-action:manipulation}
:where(button,a,[role="button"]){-webkit-tap-highlight-color:transparent}
body::after,.kvass-flame{animation:none!important}
.kvass-orbit{animation-duration:90s!important}
@media(max-width:760px){.kvass-orbit{animation:none!important}.kvass-space-layer{opacity:.55}}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto!important}
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
  .kvass-space-layer{display:none!important}
}
"""

MENU_CSS = r"""
/* kvassistent-compact-menu */
.menu-toggle{display:none;align-items:center;gap:7px;padding:9px 12px;border:1px solid rgba(180,119,24,.28);border-radius:999px;background:#fff;color:#2a2118;font:800 15px/1 system-ui;cursor:pointer;touch-action:manipulation}
.menu-toggle:focus-visible{outline:3px solid rgba(180,119,24,.35);outline-offset:2px}
.telegram-direct{background:#229ed9!important;color:#fff!important;border-color:#229ed9!important}
.inline-language-picker{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-left:auto;padding:5px;border:1px solid rgba(180,119,24,.28);border-radius:999px;background:rgba(255,253,247,.94);box-shadow:0 8px 24px rgba(42,33,24,.09)}
.inline-language-picker>span{padding:0 6px;color:#6f6252;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.06em}
.inline-language-button{min-width:42px;border:0;border-radius:999px;padding:9px 11px;background:transparent;color:#2a2118;font:900 13px/1 system-ui;cursor:pointer;touch-action:manipulation}
.inline-language-button:hover{background:#f4ead7}
.inline-language-button[aria-pressed="true"]{background:#b47718;color:#fffdf7;box-shadow:0 5px 16px rgba(180,119,24,.28)}
.inline-language-button:focus-visible{outline:3px solid rgba(180,119,24,.36);outline-offset:2px}
#kvass-language-content[aria-busy="true"]{opacity:.62}
@media(max-width:980px){.inline-language-picker{order:4;width:100%;justify-content:center;margin-left:0;border-radius:18px}.inline-language-picker>span{width:100%;text-align:center}}
@media(max-width:760px){
  .site-topbar{transition:padding .18s ease,border-radius .18s ease,box-shadow .18s ease}
  .menu-toggle{display:inline-flex;margin-left:auto}
  .site-topbar.is-compact{padding:8px 10px;gap:8px;border-radius:0 0 16px 16px;box-shadow:0 10px 28px rgba(0,0,0,.22)}
  .site-topbar.is-compact .topbar-brand{flex:1;min-width:0}
  .site-topbar.is-compact .topbar-brand span,.site-topbar.is-compact .topbar-links{display:none}
  .site-topbar.is-compact .topbar-brand strong{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .site-topbar.is-compact .inline-language-picker{display:flex;width:100%;padding:4px;gap:3px}
  .site-topbar.is-compact .inline-language-picker>span{display:none}
  .site-topbar.is-compact .inline-language-button{flex:1;min-width:0;padding:8px 5px}
  .site-topbar.is-compact[data-expanded="true"]{padding:14px;align-items:flex-start}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand{width:calc(100% - 90px)}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand span{display:block}
  .site-topbar.is-compact[data-expanded="true"] .topbar-links{display:flex;width:100%}
}
"""


def extract_main(html: str) -> str:
    match = re.search(r"<main(?:\s[^>]*)?>(.*?)</main>", html, re.S | re.I)
    if not match:
        raise RuntimeError("Localized summary has no <main>")
    content = match.group(1)
    content = re.sub(r"<header\b[^>]*class=[\"'][^\"']*site-topbar[^\"']*[\"'][^>]*>.*?</header>", "", content, flags=re.S | re.I)
    content = re.sub(r"<script\b[^>]*>.*?</script>", "", content, flags=re.S | re.I)
    return content.strip()


def extract_title(html: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else fallback


def absolutize(content: str, base_path: str) -> str:
    pattern = re.compile(r"(?P<attr>href|src)=(?P<quote>[\"'])(?P<url>.*?)(?P=quote)", re.I)

    def replace(match: re.Match[str]) -> str:
        url = match.group("url").strip()
        if not url or url.startswith(("#", "/", "http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
            resolved = url
        else:
            resolved = urljoin(base_path, url)
        return f'{match.group("attr")}={match.group("quote")}{resolved}{match.group("quote")}'

    return pattern.sub(replace, content)


def localized_snapshots() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for language, config in LANGUAGES.items():
        path = SITE / language / "summary/index.html"
        if not path.is_file():
            raise RuntimeError(f"Missing localized summary: {path.relative_to(SITE)}")
        html = path.read_text(encoding="utf-8")
        result[language] = {
            "title": extract_title(html, f"KVASSISTENT · {config['label']}"),
            "html": absolutize(extract_main(html), str(config["summary"])),
        }
    return result


def language_markup() -> str:
    buttons = "".join(
        f'<button class="inline-language-button" type="button" data-kvass-lang="{language}" '
        f'aria-label="{config["label"]}" aria-pressed="false">{config["short"]}</button>'
        for language, config in LANGUAGES.items()
    )
    return f'<div class="inline-language-picker" role="group" aria-label="Language · Язык"><span>Язык</span>{buttons}</div>'


def language_script(snapshots: dict[str, dict[str, str]]) -> str:
    safe_json = json.dumps(snapshots, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="kvass-language-data" type="application/json">{safe_json}</script>
<script id="kvassistent-inline-languages">
(() => {{
  const content = document.getElementById("kvass-language-content");
  const dataNode = document.getElementById("kvass-language-data");
  const buttons = Array.from(document.querySelectorAll("[data-kvass-lang]"));
  if (!content || !dataNode || !buttons.length) return;
  const snapshots = JSON.parse(dataNode.textContent || "{{}}");
  snapshots.ru = {{html: content.innerHTML, title: document.title}};
  const available = new Set(Object.keys(snapshots));
  const applyLanguage = (language, remember = true) => {{
    const selected = available.has(language) ? language : "ru";
    const snapshot = snapshots[selected];
    content.setAttribute("aria-busy", "true");
    content.innerHTML = snapshot.html;
    document.documentElement.lang = selected;
    document.title = snapshot.title;
    buttons.forEach((button) => button.setAttribute("aria-pressed", button.dataset.kvassLang === selected ? "true" : "false"));
    content.removeAttribute("aria-busy");
    if (remember) {{ try {{ localStorage.setItem("kvassistent-language", selected); }} catch (_) {{}} }}
    document.dispatchEvent(new CustomEvent("kvassistent:language", {{detail: {{language: selected}}}}));
  }};
  buttons.forEach((button) => button.addEventListener("click", () => applyLanguage(button.dataset.kvassLang || "ru")));
  let stored = "ru";
  try {{ stored = localStorage.getItem("kvassistent-language") || "ru"; }} catch (_) {{}}
  applyLanguage(stored, false);
}})();
</script>'''


MENU_SCRIPT = r'''<script id="kvassistent-navigation">
(() => {
  const topbar = document.getElementById("site-topbar");
  const toggle = document.getElementById("menu-toggle");
  const setExpanded = (expanded) => { if (!topbar) return; topbar.dataset.expanded = expanded ? "true" : "false"; if (toggle) toggle.setAttribute("aria-expanded", expanded ? "true" : "false"); };
  const syncCompactState = () => { if (!topbar) return; const compact = window.scrollY > 120; topbar.classList.toggle("is-compact", compact); if (!compact) setExpanded(false); };
  let lastToggleAt = 0;
  if (toggle) toggle.addEventListener("click", () => { const now = performance.now(); if (now - lastToggleAt < 450) return; lastToggleAt = now; setExpanded(topbar?.dataset.expanded !== "true"); });
  window.addEventListener("scroll", syncCompactState, {passive:true});
  syncCompactState();
})();
</script>'''


def patch_landing(path: Path, snapshots: dict[str, dict[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<header class="site-topbar web-only" id="site-topbar">',
        '<header class="site-topbar web-only" id="site-topbar" data-expanded="false">',
        1,
    )
    if 'id="menu-toggle"' not in text:
        text = text.replace(
            '<nav class="topbar-links">',
            '<button class="menu-toggle" id="menu-toggle" type="button" aria-controls="site-topbar" aria-expanded="false">☰ <span>Меню</span></button><nav class="topbar-links">',
            1,
        )
    if BOT_URL not in text:
        text = text.replace(
            '<nav class="topbar-links">',
            f'<nav class="topbar-links"><a class="telegram-direct" href="{BOT_URL}" target="_blank" rel="noopener noreferrer">Telegram-бот</a>',
            1,
        )

    picker = language_markup()
    text, replaced = re.subn(r'<div class="header-language">.*?</div>', picker, text, count=1, flags=re.S)
    if replaced == 0 and "inline-language-picker" not in text:
        text = text.replace("</header>", picker + "</header>", 1)

    if "kvassistent-compact-menu" not in text:
        text = text.replace("</style>", MENU_CSS + "\n</style>", 1)

    if 'id="kvass-language-content"' not in text:
        header_end = text.find("</header>")
        main_end = text.rfind("</main>")
        if header_end < 0 or main_end < 0 or header_end >= main_end:
            raise RuntimeError(f"Cannot locate homepage content boundaries in {path}")
        start = header_end + len("</header>")
        original = text[start:main_end]
        text = text[:start] + '\n<div id="kvass-language-content">' + original + "</div>\n" + language_script(snapshots) + "\n" + text[main_end:]

    text = re.sub(r'<script id="kvassistent-navigation">.*?</script>', "", text, flags=re.S)
    text = text.replace("</body>", MENU_SCRIPT + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")


def install_safe_interactions() -> None:
    marker = "kvassistent-safe-interactions-v24"
    for css_path in SITE.rglob("*.css"):
        text = css_path.read_text(encoding="utf-8")
        if marker not in text:
            css_path.write_text(text.rstrip() + "\n" + ACCESSIBILITY_CSS + "\n", encoding="utf-8")
    for html_path in SITE.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        if marker in text:
            continue
        if "</head>" in text:
            text = text.replace("</head>", f"<style>{ACCESSIBILITY_CSS}</style></head>", 1)
            html_path.write_text(text, encoding="utf-8")


def telegram_page() -> str:
    return f'''<!doctype html>
<html lang="ru"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#07182a">
  <meta name="description" content="КВАССИСТЕНТ: рецепт кваса, помощь с партией и пожелания с фотографиями в PR следующего релиза.">
  <title>КВАССИСТЕНТ Telegram · Версия {ONES}</title>
  <style>
    :root{{color-scheme:dark;--ink:#eef8ff;--muted:#b9d8ed;--accent:#62c4ff}}*{{box-sizing:border-box}}
    body{{margin:0;min-height:100vh;background:radial-gradient(circle at 30% 20%,#263c77,#050812 65%);color:var(--ink);font:18px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
    main{{width:min(900px,calc(100% - 32px));margin:auto;padding:30px 0 60px}}.card{{margin:18px 0;padding:clamp(26px,6vw,48px);border:1px solid #4da9e9;border-radius:28px;background:rgba(4,17,34,.94);box-shadow:0 24px 70px rgba(0,0,0,.35)}}
    .eyebrow{{margin:0 0 12px;color:var(--accent);font-size:12px;font-weight:900;letter-spacing:.13em;text-transform:uppercase}}h1{{margin:0;font:500 clamp(46px,9vw,82px)/.95 Georgia,"Times New Roman",serif;letter-spacing:-.04em}}h2{{font:500 34px/1.1 Georgia,"Times New Roman",serif}}.lead,.small{{color:var(--muted)}}
    .answer{{padding:17px 19px;border-radius:16px;background:#0c3454;font-weight:850}}.primary{{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-top:25px;padding:17px 21px;border-radius:999px;background:var(--accent);color:#04111d;font-weight:900;text-decoration:none;touch-action:manipulation}}
    .features{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;padding:0;list-style:none}}.features li{{padding:15px;border:1px solid #315b7c;border-radius:16px;background:#07182a}}
    .links{{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}}.links a{{padding:11px 15px;border:1px solid #47769b;border-radius:999px;color:#9edcff;text-decoration:none;touch-action:manipulation}}
    {ACCESSIBILITY_CSS}
  </style>
</head><body><main>
  <section class="card"><p class="eyebrow">КВАССИСТЕНТ · ВЕРСИЯ {ONES}</p><h1>Ай да хорош!</h1>
    <p class="lead">При запуске бот сначала приветствует, затем присылает короткий рецепт на 3 литра и только после этого спрашивает, чем помочь.</p>
    <p class="answer">Ай да какой ты квас задумал, ай да хорош! 🥤</p>
    <a class="primary" href="{BOT_URL}" target="_blank" rel="noopener noreferrer"><strong>Открыть @kvassistent_bot</strong><span>→</span></a>
  </section>
  <section class="card"><h2>Что нового в версии {ONES}</h2><ul class="features">
    <li><strong>Языки на главной</strong><br>Шесть языков переключаются мгновенно без перехода на другую страницу.</li>
    <li><strong>Короткий рецепт</strong><br>Процеживание через чистую марлю, сложенный бинт или пищевой фильтровальный мешок.</li>
    <li><strong>Пожелания</strong><br>Новые содержательные идеи становятся задачами релиза 25.</li>
    <li><strong>Фотографии</strong><br>Одинаковые фото с одинаковой подписью не дублируются.</li>
  </ul></section>
  <section class="card"><h2>Все основные ссылки</h2><nav class="links">
    <a href="/">Главная и языки</a><a href="/feedback/">Добавить напиток</a><a href="/companion/">Живая партия</a><a href="/game/">Игра</a><a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub</a>
  </nav><p class="small">Версия {ONES}: v{VERSION}</p></section>
</main></body></html>'''


def install_telegram() -> None:
    for root in (SITE, SITE / f"v{VERSION}"):
        target = root / "telegram/index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(telegram_page(), encoding="utf-8")


snapshots = localized_snapshots()
for landing in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    if not landing.is_file():
        raise RuntimeError(f"Missing landing page: {landing}")
    patch_landing(landing, snapshots)

install_telegram()
install_safe_interactions()

for required in (ROOT / "PROJECT_GOAL.md", ROOT / ".github/copilot-instructions.md"):
    if not required.is_file():
        raise RuntimeError(f"Missing GitHub agent context: {required.relative_to(ROOT)}")

latest_landing = (SITE / "index.html").read_text(encoding="utf-8")
telegram_html = (SITE / "telegram/index.html").read_text(encoding="utf-8")
for required in (
    'id="menu-toggle"',
    "kvassistent-compact-menu",
    BOT_URL,
    'id="kvassistent-inline-languages"',
    'id="kvass-language-content"',
    "inline-language-button",
    "localStorage.setItem",
    "kvassistent-safe-interactions-v24",
    "touch-action:manipulation",
    "prefers-reduced-motion",
):
    if required not in latest_landing:
        raise RuntimeError(f"Landing finalization missing: {required}")
if "window.location.assign" in latest_landing:
    raise RuntimeError("Language switching must not navigate to another page")
for language in LANGUAGES:
    if f'data-kvass-lang="{language}"' not in latest_landing:
        raise RuntimeError(f"Missing inline language button: {language}")
for required in (BOT_URL, "@kvassistent_bot", f"ВЕРСИЯ {ONES}", "Ай да какой ты квас задумал", "пищевой фильтровальный мешок", "релиза 25"):
    if required not in telegram_html:
        raise RuntimeError(f"Telegram page finalization missing: {required}")

print(f"finalized KVASSISTENT version {ONES}: six inline homepage languages without navigation")
