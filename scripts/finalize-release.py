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
HUMAN = f"Версия {ONES}"
TECHNICAL = f"v{VERSION}"
NEXT_RELEASE = int(META.get("next_release_number", ONES + 1))

LANGUAGES = {
    "ru": ("Русский", "RU", "/ru/summary/"),
    "en": ("English", "EN", "/en/summary/"),
    "es": ("Español", "ES", "/es/summary/"),
    "de": ("Deutsch", "DE", "/de/summary/"),
    "zh-CN": ("简体中文", "中文", "/zh-CN/summary/"),
    "el": ("Ελληνικά", "EL", "/el/summary/"),
}

HEADER_COPY = {
    "ru": {"brand": "КВАССИСТЕНТ", "subtitle": "Последняя версия и все основные входы", "game": "Игра", "companion": "Живая партия", "links": "Все ссылки", "people": "Для людей", "ai": "Для ИИ", "feedback": "Фидбек", "telegram": "Telegram", "telegramBot": "Telegram-бот", "github": "GitHub", "menu": "Меню", "language": "Язык"},
    "en": {"brand": "KVASSISTENT", "subtitle": "Latest version and every main entry point", "game": "Game", "companion": "Live batch", "links": "All links", "people": "For people", "ai": "For AI", "feedback": "Feedback", "telegram": "Telegram", "telegramBot": "Telegram bot", "github": "GitHub", "menu": "Menu", "language": "Language"},
    "es": {"brand": "KVASSISTENT", "subtitle": "Última versión y todos los accesos principales", "game": "Juego", "companion": "Lote en vivo", "links": "Todos los enlaces", "people": "Para personas", "ai": "Para IA", "feedback": "Comentarios", "telegram": "Telegram", "telegramBot": "Bot de Telegram", "github": "GitHub", "menu": "Menú", "language": "Idioma"},
    "de": {"brand": "KVASSISTENT", "subtitle": "Neueste Version und alle wichtigen Einstiege", "game": "Spiel", "companion": "Live-Charge", "links": "Alle Links", "people": "Für Menschen", "ai": "Für KI", "feedback": "Feedback", "telegram": "Telegram", "telegramBot": "Telegram-Bot", "github": "GitHub", "menu": "Menü", "language": "Sprache"},
    "zh-CN": {"brand": "KVASSISTENT", "subtitle": "最新版本和所有主要入口", "game": "游戏", "companion": "实时批次", "links": "全部链接", "people": "用户指南", "ai": "AI 指南", "feedback": "反馈", "telegram": "Telegram", "telegramBot": "Telegram 机器人", "github": "GitHub", "menu": "菜单", "language": "语言"},
    "el": {"brand": "KVASSISTENT", "subtitle": "Τελευταία έκδοση και όλες οι βασικές είσοδοι", "game": "Παιχνίδι", "companion": "Ζωντανή παρτίδα", "links": "Όλοι οι σύνδεσμοι", "people": "Για ανθρώπους", "ai": "Για AI", "feedback": "Σχόλια", "telegram": "Telegram", "telegramBot": "Bot Telegram", "github": "GitHub", "menu": "Μενού", "language": "Γλώσσα"},
}

ACCESSIBILITY_CSS = r"""
/* kvassistent-safe-interactions */
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
.inline-language-picker{display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-left:auto;padding:5px;border:1px solid rgba(180,119,24,.28);border-radius:999px;background:rgba(255,253,247,.96);box-shadow:0 8px 24px rgba(42,33,24,.09)}
.inline-language-picker>span{padding:0 6px;color:#6f6252;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.06em}
.inline-language-button{min-width:42px;border:0;border-radius:999px;padding:9px 11px;background:transparent;color:#2a2118;font:900 13px/1 system-ui;cursor:pointer;touch-action:manipulation}
.inline-language-button:hover{background:#f4ead7}
.inline-language-button[aria-pressed="true"]{background:#b47718;color:#fffdf7;box-shadow:0 5px 16px rgba(180,119,24,.28)}
.inline-language-button:focus-visible{outline:3px solid rgba(180,119,24,.36);outline-offset:2px}
#header-language-select[hidden]{display:none!important}
#kvass-language-content[aria-busy="true"]{opacity:.62}
.header-version-badge{display:inline-flex;align-items:center;justify-content:center;min-height:38px;padding:8px 12px;border-radius:999px;background:#2a2118;color:#fffdf7;font:950 13px/1 system-ui;letter-spacing:.08em;box-shadow:0 7px 18px rgba(42,33,24,.2);white-space:nowrap}
#kvass-language-content{transition:opacity .12s ease}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]){margin:18px 0 42px;padding:clamp(20px,4vw,42px);border:1px solid rgba(219,201,169,.96);border-radius:26px;background:rgba(255,253,247,.98);color:#2a2118;box-shadow:0 24px 70px rgba(0,0,0,.28);backdrop-filter:blur(14px)}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) :where(h1,h2,h3,h4,p,li,strong,em,code,span){color:inherit}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) a{color:#7a4c06;text-decoration-thickness:2px;text-underline-offset:3px}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) .cover{background:linear-gradient(145deg,#fffdf7,#f8efdd)!important;color:#2a2118!important;box-shadow:none!important}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) article{color:#2a2118}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) pre{color:#fff8e8;background:#211a13}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) h2{border-bottom-color:#dbc9a9}

@media(max-width:980px){.inline-language-picker{order:4;width:100%;justify-content:center;margin-left:0;border-radius:18px}.inline-language-picker>span{width:100%;text-align:center}}
@media(max-width:760px){
  .site-topbar{transition:padding .18s ease,border-radius .18s ease,box-shadow .18s ease}
  .menu-toggle{display:inline-flex;margin-left:auto}
  .site-topbar.is-compact{padding:8px 10px;gap:8px;border-radius:0 0 16px 16px;box-shadow:0 10px 28px rgba(0,0,0,.22)}
  .site-topbar.is-compact .topbar-brand{flex:1;min-width:0}
  .site-topbar.is-compact .topbar-brand span,.site-topbar.is-compact .topbar-links{display:none}.site-topbar.is-compact .header-version-badge{min-height:34px;padding:7px 9px}
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


def snapshots() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for language, (label, _short, route) in LANGUAGES.items():
        path = SITE / language / "summary/index.html"
        if not path.is_file():
            raise RuntimeError(f"Missing localized summary: {path.relative_to(SITE)}")
        html = path.read_text(encoding="utf-8")
        result[language] = {
            "title": extract_title(html, f"KVASSISTENT · {label}"),
            "html": absolutize(extract_main(html), route),
        }
    return result


def language_markup() -> str:
    buttons = "".join(
        f'<button class="inline-language-button" type="button" data-kvass-lang="{language}" aria-label="{label}" aria-pressed="false">{short}</button>'
        for language, (label, short, _route) in LANGUAGES.items()
    )
    options = "".join(f'<option value="{language}">{label}</option>' for language, (label, _short, _route) in LANGUAGES.items())
    legacy = f'<select id="header-language-select" hidden aria-hidden="true" tabindex="-1">{options}</select>'
    return f'<div class="inline-language-picker" role="group" aria-label="Language · Язык"><span id="header-language-label">Язык</span>{buttons}{legacy}</div>'


def language_script(data: dict[str, dict[str, str]]) -> str:
    safe_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    header_json = json.dumps(HEADER_COPY, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<script id="kvass-language-data" type="application/json">{safe_json}</script>
<script id="kvass-header-language-data" type="application/json">{header_json}</script>
<script id="kvassistent-inline-languages">
(() => {{
  const content = document.getElementById("kvass-language-content");
  const dataNode = document.getElementById("kvass-language-data");
  const headerNode = document.getElementById("kvass-header-language-data");
  const buttons = Array.from(document.querySelectorAll("[data-kvass-lang]"));
  if (!content || !dataNode || !headerNode || !buttons.length) return;
  const items = JSON.parse(dataNode.textContent || "{{}}");
  const headerItems = JSON.parse(headerNode.textContent || "{{}}");
  items.ru = {{html:content.innerHTML,title:document.title}};
  const setText = (id, value) => {{ const node = document.getElementById(id); if (node && value) node.textContent = value; }};
  const apply = (requested, remember=true) => {{
    const language = Object.prototype.hasOwnProperty.call(items, requested) ? requested : "ru";
    const header = headerItems[language] || headerItems.ru || {{}};
    content.setAttribute("aria-busy", "true");
    content.innerHTML = items[language].html;
    content.dataset.activeLang = language;
    document.documentElement.lang = language;
    document.title = items[language].title;
    setText("header-brand-title", header.brand);
    setText("header-brand-subtitle", header.subtitle);
    setText("menu-label", header.menu);
    setText("header-language-label", header.language);
    document.querySelectorAll("[data-header-key]").forEach((node) => {{ const value = header[node.dataset.headerKey]; if (value) node.textContent = value; }});
    buttons.forEach((button) => button.setAttribute("aria-pressed", button.dataset.kvassLang === language ? "true" : "false"));
    content.removeAttribute("aria-busy");
    if (remember) {{ try {{ localStorage.setItem("kvassistent-language", language); }} catch (_) {{}} }}
  }};
  buttons.forEach((button) => button.addEventListener("click", () => apply(button.dataset.kvassLang || "ru")));
  let stored = "ru";
  try {{ stored = localStorage.getItem("kvassistent-language") || "ru"; }} catch (_) {{}}
  apply(stored, false);
}})();
</script>"""


MENU_SCRIPT = r'''<script id="kvassistent-navigation">
(() => {
  const topbar = document.getElementById("site-topbar");
  const toggle = document.getElementById("menu-toggle");
  const setExpanded = (expanded) => { if (!topbar) return; topbar.dataset.expanded = expanded ? "true" : "false"; if (toggle) toggle.setAttribute("aria-expanded", expanded ? "true" : "false"); };
  const sync = () => { if (!topbar) return; const compact = window.scrollY > 120; topbar.classList.toggle("is-compact", compact); if (!compact) setExpanded(false); };
  let last = 0;
  if (toggle) toggle.addEventListener("click", () => { const now = performance.now(); if (now-last < 450) return; last=now; setExpanded(topbar?.dataset.expanded !== "true"); });
  window.addEventListener("scroll", sync, {passive:true}); sync();
})();
</script>'''


def patch_landing(path: Path, data: dict[str, dict[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace('<header class="site-topbar web-only" id="site-topbar">', '<header class="site-topbar web-only" id="site-topbar" data-expanded="false">', 1)
    if 'id="menu-toggle"' not in text:
        text = text.replace('<nav class="topbar-links">', '<button class="menu-toggle" id="menu-toggle" type="button" aria-controls="site-topbar" aria-expanded="false">☰ <span>Меню</span></button><nav class="topbar-links">', 1)
    if BOT_URL not in text:
        text = text.replace('<nav class="topbar-links">', f'<nav class="topbar-links"><a class="telegram-direct" href="{BOT_URL}" target="_blank" rel="noopener noreferrer">Telegram-бот</a>', 1)

    text = text.replace('<div class="topbar-brand"><strong>КВАССИСТЕНТ</strong><span>Последняя версия и все основные входы</span></div>', '<div class="topbar-brand"><strong id="header-brand-title">КВАССИСТЕНТ</strong><span id="header-brand-subtitle">Последняя версия и все основные входы</span></div>', 1)
    text = text.replace('☰ <span>Меню</span>', '☰ <span id="menu-label">Меню</span>', 1)
    header_links = {
        '<a href="/game/">Игра</a>': '<a href="/game/" data-header-key="game">Игра</a>',
        '<a href="/companion/">Живая партия</a>': '<a href="/companion/" data-header-key="companion">Живая партия</a>',
        '<a href="#all-links">Все ссылки</a>': '<a href="#all-links" data-header-key="links">Все ссылки</a>',
        '<a href="#for-people">Для людей</a>': '<a href="#for-people" data-header-key="people">Для людей</a>',
        '<a href="#for-ai-agents">Для ИИ</a>': '<a href="#for-ai-agents" data-header-key="ai">Для ИИ</a>',
        '<a href="/feedback/">Фидбек</a>': '<a href="/feedback/" data-header-key="feedback">Фидбек</a>',
        '<a href="/telegram/">Telegram</a>': '<a href="/telegram/" data-header-key="telegram">Telegram</a>',
        '<a href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a>': '<a href="https://github.com/bambuchastudent/kvas-ai-agent" data-header-key="github">GitHub</a>',
        f'<a class="telegram-direct" href="{BOT_URL}" target="_blank" rel="noopener noreferrer">Telegram-бот</a>': f'<a class="telegram-direct" href="{BOT_URL}" target="_blank" rel="noopener noreferrer" data-header-key="telegramBot">Telegram-бот</a>',
    }
    for old, new in header_links.items():
        text = text.replace(old, new, 1)

    picker = f'<span class="header-version-badge" id="header-version-badge" aria-label="KVASSISTENT {HUMAN}">{HUMAN}</span>' + language_markup()
    text, replaced = re.subn(r'<div class="header-language">.*?</div>', picker, text, count=1, flags=re.S)
    if replaced == 0 and "inline-language-picker" not in text:
        text = text.replace("</header>", picker + "</header>", 1)
    if "kvassistent-compact-menu" not in text:
        text = text.replace("</style>", MENU_CSS + "\n</style>", 1)

    if 'id="kvass-language-content"' not in text:
        header_end = text.find("</header>")
        main_end = text.rfind("</main>")
        if header_end < 0 or main_end < 0 or header_end >= main_end:
            raise RuntimeError(f"Cannot locate homepage boundaries in {path}")
        start = header_end + len("</header>")
        original = text[start:main_end]
        text = text[:start] + '\n<div id="kvass-language-content">' + original + "</div>\n" + language_script(data) + "\n" + text[main_end:]

    text = re.sub(r'<script id="kvassistent-navigation">.*?</script>', "", text, flags=re.S)
    text = text.replace("</body>", MENU_SCRIPT + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")


def install_safe_interactions() -> None:
    marker = "kvassistent-safe-interactions"
    for css_path in SITE.rglob("*.css"):
        text = css_path.read_text(encoding="utf-8")
        if marker not in text:
            css_path.write_text(text.rstrip()+"\n"+ACCESSIBILITY_CSS+"\n", encoding="utf-8")
    for html_path in SITE.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        if marker not in text and "</head>" in text:
            html_path.write_text(text.replace("</head>", f"<style>{ACCESSIBILITY_CSS}</style></head>", 1), encoding="utf-8")


def telegram_page() -> str:
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>КВАССИСТЕНТ Telegram · Версия {ONES}</title><style>
:root{{color-scheme:dark;--ink:#eef8ff;--accent:#62c4ff}}*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;background:radial-gradient(circle at 30% 20%,#263c77,#050812 65%);color:var(--ink);font:18px/1.55 system-ui}}main{{width:min(900px,calc(100% - 32px));margin:auto;padding:30px 0 60px}}.card{{margin:18px 0;padding:clamp(26px,6vw,48px);border:1px solid #4da9e9;border-radius:28px;background:rgba(4,17,34,.94)}}h1{{font:500 clamp(46px,9vw,82px)/.95 Georgia,serif}}a{{color:#9edcff}}.primary{{display:flex;padding:17px 21px;border-radius:999px;background:var(--accent);color:#04111d;font-weight:900;text-decoration:none}}{ACCESSIBILITY_CSS}</style></head><body><main>
<section class="card"><p>КВАССИСТЕНТ · ВЕРСИЯ {ONES}</p><h1>Ай да хорош!</h1><p>Ай да какой ты квас задумал, ай да хорош! 🥤</p><a class="primary" href="{BOT_URL}">Открыть @kvassistent_bot →</a></section>
<section class="card"><h2>Что нового</h2><p>Шесть языков переключаются прямо на главной без перехода на другую страницу.</p><p>Короткий рецепт сохраняет процеживание через чистую марлю, сложенный бинт или пищевой фильтровальный мешок.</p><p>Новые идеи и фотографии становятся задачами релиза {NEXT_RELEASE}.</p></section>
<section class="card"><a href="/">Главная и языки</a> · <a href="/feedback/">Добавить напиток</a> · <a href="/companion/">Живая партия</a> · <a href="/game/">Игра</a> · <a href="{REPO_URL}">GitHub</a><p>v{VERSION}</p></section>
</main></body></html>'''


def install_telegram() -> None:
    for root in (SITE, SITE/f"v{VERSION}"):
        target = root/"telegram/index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(telegram_page(), encoding="utf-8")


data = snapshots()
for landing in (SITE/"index.html", SITE/f"v{VERSION}/index.html"):
    if not landing.is_file():
        raise RuntimeError(f"Missing landing page: {landing}")
    patch_landing(landing, data)
install_telegram()
install_safe_interactions()

for required in (ROOT/"PROJECT_GOAL.md", ROOT/".github/copilot-instructions.md"):
    if not required.is_file():
        raise RuntimeError(f"Missing GitHub agent context: {required.relative_to(ROOT)}")

latest = (SITE/"index.html").read_text(encoding="utf-8")
telegram = (SITE/"telegram/index.html").read_text(encoding="utf-8")
for required in ('id="header-language-select"','id="header-version-badge"','id="header-brand-title"','data-header-key="game"','id="kvassistent-inline-languages"','id="kvass-language-content"',"inline-language-button","data-active-lang","kvass-header-language-data","localStorage.setItem","kvassistent-safe-interactions","touch-action:manipulation","prefers-reduced-motion",BOT_URL):
    if required not in latest:
        raise RuntimeError(f"Landing finalization missing: {required}")
if "window.location.assign" in latest:
    raise RuntimeError("Language switching must not navigate")
for language in LANGUAGES:
    if f'data-kvass-lang="{language}"' not in latest:
        raise RuntimeError(f"Missing inline language button: {language}")
for required in (BOT_URL,"@kvassistent_bot",f"ВЕРСИЯ {ONES}","Ай да какой ты квас задумал","пищевой фильтровальный мешок",f"релиза {NEXT_RELEASE}"):
    if required not in telegram:
        raise RuntimeError(f"Telegram page finalization missing: {required}")
print(f"finalized KVASSISTENT version {ONES}: readable inline languages, localized header and persistent version badge")

# KVASSISTENT_PUBLIC_DISCOVERY_V26
import html as _public_html
import shutil as _public_shutil

_PUBLIC_BASE = "https://kvassistent.pages.dev"
_PUBLIC_IMAGE = f"{_PUBLIC_BASE}/assets/kvassistent-social.png"
_PUBLIC_DESCRIPTION = (
    "KVASSISTENT is a free human-first AI companion for making homemade kvass. "
    "It guides a real person through one batch, explains risks, works in six languages, "
    "and keeps the latest public entry points on one stable URL."
)
_PUBLIC_LANGS = ("ru", "en", "es", "de", "zh-CN", "el")


def _public_route(path: Path) -> tuple[str, bool]:
    relative = path.relative_to(SITE).as_posix()
    immutable_prefix = f"v{VERSION}/"
    immutable = relative.startswith(immutable_prefix)
    if immutable:
        relative = relative[len(immutable_prefix):]
    if relative in ("index.html", ""):
        route = "/"
    elif relative in ("game/index.html", "companion/game/index.html"):
        route = "/game/"
    elif relative.endswith("/index.html"):
        route = "/" + relative[:-len("index.html")]
    else:
        route = "/" + relative
    route = re.sub(r"/+", "/", route)
    return route, immutable


def _public_title(text: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
    if not match:
        return fallback
    return re.sub(r"\s+", " ", match.group(1)).strip()


def _public_description(text: str) -> str:
    match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        text,
        flags=re.I | re.S,
    )
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else _PUBLIC_DESCRIPTION


def _public_alternates(route: str) -> str:
    if route == "/":
        doc_type = "summary"
    else:
        match = re.fullmatch(r"/(?:ru|en|es|de|zh-CN|el)/(summary|instructions)/", route)
        if not match:
            return ""
        doc_type = match.group(1)
    links = [
        f'<link rel="alternate" hreflang="{language}" href="{_PUBLIC_BASE}/{language}/{doc_type}/">'
        for language in _PUBLIC_LANGS
    ]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{_PUBLIC_BASE}/">')
    return "".join(links)


def _public_patch_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    route, immutable = _public_route(path)
    canonical = _PUBLIC_BASE + route
    title = _public_title(text, "KVASSISTENT — human-first AI for homemade kvass")
    description = _public_description(text)
    robots = "noindex,follow" if immutable else "index,follow,max-image-preview:large"

    removal_patterns = (
        r'<link\s+rel=["\']canonical["\'][^>]*>',
        r'<link\s+rel=["\']alternate["\'][^>]*>',
        r'<meta\s+name=["\']robots["\'][^>]*>',
        r'<meta\s+name=["\']googlebot["\'][^>]*>',
        r'<meta\s+property=["\']og:(?:site_name|type|title|description|url|image|image:width|image:height)["\'][^>]*>',
        r'<meta\s+name=["\']twitter:(?:card|title|description|image)["\'][^>]*>',
    )
    for pattern in removal_patterns:
        text = re.sub(pattern, "", text, flags=re.I)

    esc_title = _public_html.escape(title, quote=True)
    esc_description = _public_html.escape(description, quote=True)
    metadata = (
        f'<meta name="robots" content="{robots}">'
        f'<meta name="googlebot" content="{robots}">'
        f'<link rel="canonical" href="{canonical}">'
        f'{_public_alternates(route)}'
        '<meta property="og:site_name" content="KVASSISTENT">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:title" content="{esc_title}">'
        f'<meta property="og:description" content="{esc_description}">'
        f'<meta property="og:url" content="{canonical}">'
        f'<meta property="og:image" content="{_PUBLIC_IMAGE}">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="800">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{esc_title}">'
        f'<meta name="twitter:description" content="{esc_description}">'
        f'<meta name="twitter:image" content="{_PUBLIC_IMAGE}">'
    )
    if "</head>" not in text:
        raise RuntimeError(f"HTML page has no closing head: {path}")
    text = text.replace("</head>", metadata + "</head>", 1)
    path.write_text(text, encoding="utf-8")


def _public_page(title: str, lead: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_public_html.escape(title)}</title><meta name="description" content="{_public_html.escape(lead, quote=True)}">
<style>
:root{{color-scheme:dark;--ink:#fff8e8;--muted:#c9d8ed;--gold:#f0bb45}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 20% 10%,#283d86,#050812 64%);color:var(--ink);font:18px/1.6 system-ui,-apple-system,sans-serif}}
main{{width:min(920px,calc(100% - 32px));margin:auto;padding:32px 0 70px}}nav{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:42px}}
nav a,.cta{{padding:10px 14px;border:1px solid #5276a3;border-radius:999px;color:#aee1ff;text-decoration:none}}
article{{padding:clamp(25px,6vw,55px);border:1px solid #576b99;border-radius:28px;background:rgba(4,15,36,.91);box-shadow:0 24px 70px rgba(0,0,0,.35)}}
h1{{margin:.1em 0 .35em;font:700 clamp(42px,8vw,76px)/.96 Georgia,serif}}h2{{margin-top:1.5em;color:#ffd778}}p,li{{color:var(--muted)}}strong{{color:var(--ink)}}code{{overflow-wrap:anywhere;color:#ffd778}}
</style></head><body><main>
<nav><a href="/">KVASSISTENT</a><a href="/how-it-works/">How it works</a><a href="/faq/">FAQ</a><a href="/press/">Press</a><a href="/changelog/">Changelog</a><a href="/telegram/">Telegram</a><a href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a></nav>
<article><p><strong>KVASSISTENT · Version {ONES}</strong></p><h1>{_public_html.escape(title)}</h1><p>{_public_html.escape(lead)}</p>{body}</article>
</main></body></html>"""


def _public_write_pages() -> None:
    pages = {
        "about": (
            "About KVASSISTENT",
            "A human-first AI companion for making real homemade kvass from bread.",
            """<h2>What it is</h2><p>KVASSISTENT guides one real batch at a time. The person prepares the ingredients, observes the jar, smells and tastes the drink; the assistant remembers state, explains risk and asks for the next observation.</p>
<h2>What makes it different</h2><ul><li>Six-language interface on one stable homepage.</li><li>Offline live-batch companion with structured JSON handoff.</li><li>Explicit safety stops instead of pretending AI can inspect food.</li><li>Open source, free to use and built in public.</li></ul>
<p><a class="cta" href="/companion/">Open the live batch companion →</a></p>""",
        ),
        "how-it-works": (
            "How KVASSISTENT works",
            "From dry bread to a chilled bottle, with one clear next step at a time.",
            """<h2>1. Start a batch</h2><p>Enter volume, ingredients, start time and temperature.</p>
<h2>2. Report what you observe</h2><p>Surface, smell, taste, sunlight, temperature and bottle pressure stay explicit; unknown data stays unknown.</p>
<h2>3. Receive the next safe step</h2><p>The companion suggests one action and a check-in time. Mold, slime, dangerous smell or overheating stop the household protocol.</p>
<h2>4. Share feedback</h2><p>Ideas, recipes and photos can be sent through the website or Telegram and become structured work for a later release.</p>""",
        ),
        "faq": (
            "KVASSISTENT FAQ",
            "Straight answers about the product, kvass, safety, languages and privacy.",
            """<h2>Does AI make the kvass?</h2><p>No. A person makes and judges the drink. AI guides, records and explains.</p>
<h2>Is homemade yeast kvass always alcohol-free?</h2><p>No honest household process can guarantee 0.0%. Fermentation can create some alcohol.</p>
<h2>Which languages are supported?</h2><p>Russian, English, Spanish, German, Simplified Chinese and Greek.</p>
<h2>Does the live companion upload my batch?</h2><p>The companion is designed to keep its working state locally in the browser. External links are opened only after an explicit action.</p>
<h2>Can AI certify food safety?</h2><p>No. KVASSISTENT provides conservative household guidance, not laboratory testing or a medical diagnosis.</p>""",
        ),
        "press": (
            "KVASSISTENT press kit",
            "Facts, positioning and official links for reviewers, communities and hackathon judges.",
            """<h2>One-line description</h2><p><strong>KVASSISTENT is a human-first AI companion that guides people through making homemade kvass while keeping observation, safety and final judgment in human hands.</strong></p>
<h2>Project facts</h2><ul><li>Free and open source.</li><li>Progressive web app with six languages.</li><li>Live batch state, safety flags and JSON handoff.</li><li>Public immutable releases plus a stable latest URL.</li><li>Telegram feedback and community recipe intake.</li></ul>
<h2>Official links</h2><p><a href="/">Live product</a> · <a href="https://devpost.com/software/kvassistent">Devpost</a> · <a href="https://github.com/bambuchastudent/kvas-ai-agent">Source code</a> · <a href="https://t.me/kvassistent_bot">Telegram bot</a></p>
<h2>Media asset</h2><p><a href="/assets/kvassistent-social.png">1200×800 social image</a></p>""",
        ),
        "changelog": (
            "KVASSISTENT changelog",
            f"Current public release: Version {ONES}. The stable homepage always points to the latest release.",
            f"""<h2>Version {ONES}</h2><p>Unified version display and public discovery: canonical latest URLs, noindex immutable archives, complete social cards, sitemap, robots, public product pages and an AI-readable project summary.</p>
<h2>Release history</h2><p>The detailed human and AI-readable history is maintained in the public repository.</p>
<p><a class="cta" href="https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/AI_CHANGELOG.md">Open AI_CHANGELOG.md →</a></p>""",
        ),
    }
    for slug, (title, lead, body) in pages.items():
        target = SITE / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_public_page(title, lead, body), encoding="utf-8")


def _public_inject_home() -> None:
    path = SITE / "index.html"
    text = path.read_text(encoding="utf-8")
    if 'id="public-discovery"' in text:
        return
    section = """
<section class="all-links-release" id="public-discovery">
  <div class="eyebrow">Public discovery · понятно людям, поиску и ИИ</div>
  <h2>Один официальный адрес и нормальное описание проекта</h2>
  <p>Главная страница всегда ведёт на последний релиз. Архивные версии остаются доступными, но не конкурируют с главной в поиске.</p>
  <div class="all-links-grid">
    <a href="/about/"><strong>About</strong><span>Что такое KVASSISTENT</span></a>
    <a href="/how-it-works/"><strong>How it works</strong><span>Как устроен продукт</span></a>
    <a href="/faq/"><strong>FAQ</strong><span>Безопасность, приватность, языки</span></a>
    <a href="/press/"><strong>Press kit</strong><span>Факты и официальные ссылки</span></a>
    <a href="/changelog/"><strong>Changelog</strong><span>Что меняется по версиям</span></a>
    <a href="/llms.txt"><strong>llms.txt</strong><span>Краткие факты для ИИ-систем</span></a>
  </div>
</section>
"""
    marker = '<section class="all-links-release" id="all-links">'
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    else:
        text = text.replace("</main>", section + "</main>", 1)
    path.write_text(text, encoding="utf-8")


def _public_write_discovery_files() -> None:
    routes = [
        ("/", "weekly", "1.0"),
        ("/about/", "monthly", "0.8"),
        ("/how-it-works/", "monthly", "0.9"),
        ("/faq/", "monthly", "0.8"),
        ("/press/", "monthly", "0.7"),
        ("/changelog/", "weekly", "0.7"),
        ("/companion/", "weekly", "0.9"),
        ("/game/", "monthly", "0.6"),
        ("/feedback/", "monthly", "0.6"),
        ("/telegram/", "monthly", "0.6"),
    ]
    for language in _PUBLIC_LANGS:
        routes.append((f"/{language}/summary/", "monthly", "0.8"))
        routes.append((f"/{language}/instructions/", "monthly", "0.7"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for route, frequency, priority in routes:
        lines.extend((
            "<url>",
            f"<loc>{_PUBLIC_BASE}{route}</loc>",
            f"<changefreq>{frequency}</changefreq>",
            f"<priority>{priority}</priority>",
            "</url>",
        ))
    lines.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {_PUBLIC_BASE}/sitemap.xml\n",
        encoding="utf-8",
    )
    (SITE / "llms.txt").write_text(
        f"""# KVASSISTENT

> KVASSISTENT is a free human-first AI companion for making homemade kvass.

Official URL: {_PUBLIC_BASE}/
Current release: Version {ONES} ({TECHNICAL})
Source: https://github.com/bambuchastudent/kvas-ai-agent
Devpost: https://devpost.com/software/kvassistent
Telegram: https://t.me/kvassistent_bot

## Product facts
- A real person brews, observes, smells, tastes and decides.
- AI remembers batch state, explains risk and suggests the next observation.
- Supported languages: Russian, English, Spanish, German, Simplified Chinese and Greek.
- Live batch state can be handed to another AI as structured JSON.
- Household guidance is not laboratory certification or medical advice.
- Yeast fermentation cannot honestly guarantee 0.0% alcohol.

## Canonical public pages
- About: {_PUBLIC_BASE}/about/
- How it works: {_PUBLIC_BASE}/how-it-works/
- FAQ: {_PUBLIC_BASE}/faq/
- Press: {_PUBLIC_BASE}/press/
- Changelog: {_PUBLIC_BASE}/changelog/
- Live batch: {_PUBLIC_BASE}/companion/
- Feedback: {_PUBLIC_BASE}/feedback/

Immutable /v.../ URLs are release archives. Cite the canonical latest pages unless a historical release is specifically required.
""",
        encoding="utf-8",
    )
    (SITE / "_headers").write_text(
        f"""/v{VERSION}/*
  X-Robots-Tag: noindex, follow
  Cache-Control: public, max-age=31536000, immutable

/assets/kvassistent-social.png
  Cache-Control: public, max-age=604800

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
""",
        encoding="utf-8",
    )


def _public_install_social_image() -> None:
    source = ROOT / "share/devpost-cover.png"
    if not source.is_file():
        raise RuntimeError(f"Missing social image source: {source}")
    for target in (
        SITE / "assets/kvassistent-social.png",
        SITE / f"v{VERSION}/assets/kvassistent-social.png",
    ):
        target.parent.mkdir(parents=True, exist_ok=True)
        _public_shutil.copy2(source, target)


_public_install_social_image()
_public_write_pages()
_public_inject_home()
_public_write_discovery_files()
for _public_html_path in SITE.rglob("*.html"):
    _public_patch_html(_public_html_path)

_public_latest = (SITE / "index.html").read_text(encoding="utf-8")
_public_immutable = (SITE / f"v{VERSION}/index.html").read_text(encoding="utf-8")
for _public_required in (
    'id="public-discovery"',
    'rel="canonical" href="https://kvassistent.pages.dev/"',
    'property="og:image" content="https://kvassistent.pages.dev/assets/kvassistent-social.png"',
    'name="twitter:card" content="summary_large_image"',
):
    if _public_required not in _public_latest:
        raise RuntimeError(f"Public discovery marker missing: {_public_required}")
if 'content="noindex,follow"' not in _public_immutable:
    raise RuntimeError("Immutable release must be noindex,follow")
for _public_required_file in (
    "robots.txt", "sitemap.xml", "llms.txt", "_headers",
    "about/index.html", "how-it-works/index.html", "faq/index.html",
    "press/index.html", "changelog/index.html", "assets/kvassistent-social.png",
):
    if not (SITE / _public_required_file).is_file():
        raise RuntimeError(f"Missing public discovery artifact: {_public_required_file}")
print(f"public discovery ready for KVASSISTENT Version {ONES}")
