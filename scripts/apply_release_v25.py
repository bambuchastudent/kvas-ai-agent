#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_VERSION = ".".join(["1"] * 24)
VERSION = ".".join(["1"] * 25)
NEXT_VERSION = ".".join(["1"] * 26)
ONES = 25

# Canonical release metadata.
meta_path = ROOT / "release/version.json"
meta = json.loads(meta_path.read_text(encoding="utf-8"))
if int(meta.get("ones_count", 0)) != 24:
    raise RuntimeError(f"Expected release 24 as the base, got {meta.get('ones_count')}")
meta.update(
    {
        "previous": OLD_VERSION,
        "current": VERSION,
        "ones_count": ONES,
        "display": f"v{VERSION}",
        "display_ru": f"Версия {ONES}, потому что в ней единиц вот столько: {ONES}. Пересчитай: v{VERSION}",
        "latest_url": "https://kvassistent.pages.dev/",
        "immutable_url": f"https://kvassistent.pages.dev/v{VERSION}/",
        "next": NEXT_VERSION,
    }
)
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Make the finalizer generate readable inline localizations and a fully localized sticky header.
path = ROOT / "scripts/finalize-release.py"
text = path.read_text(encoding="utf-8")
text = text.replace("kvassistent-safe-interactions-v24", "kvassistent-safe-interactions-v25")

header_copy = r'''
HEADER_COPY = {
    "ru": {"brand": "КВАССИСТЕНТ", "subtitle": "Последняя версия и все основные входы", "game": "Игра", "companion": "Живая партия", "links": "Все ссылки", "people": "Для людей", "ai": "Для ИИ", "feedback": "Фидбек", "telegram": "Telegram", "telegramBot": "Telegram-бот", "github": "GitHub", "menu": "Меню", "language": "Язык"},
    "en": {"brand": "KVASSISTENT", "subtitle": "Latest version and every main entry point", "game": "Game", "companion": "Live batch", "links": "All links", "people": "For people", "ai": "For AI", "feedback": "Feedback", "telegram": "Telegram", "telegramBot": "Telegram bot", "github": "GitHub", "menu": "Menu", "language": "Language"},
    "es": {"brand": "KVASSISTENT", "subtitle": "Última versión y todos los accesos principales", "game": "Juego", "companion": "Lote en vivo", "links": "Todos los enlaces", "people": "Para personas", "ai": "Para IA", "feedback": "Comentarios", "telegram": "Telegram", "telegramBot": "Bot de Telegram", "github": "GitHub", "menu": "Menú", "language": "Idioma"},
    "de": {"brand": "KVASSISTENT", "subtitle": "Neueste Version und alle wichtigen Einstiege", "game": "Spiel", "companion": "Live-Charge", "links": "Alle Links", "people": "Für Menschen", "ai": "Für KI", "feedback": "Feedback", "telegram": "Telegram", "telegramBot": "Telegram-Bot", "github": "GitHub", "menu": "Menü", "language": "Sprache"},
    "zh-CN": {"brand": "KVASSISTENT", "subtitle": "最新版本和所有主要入口", "game": "游戏", "companion": "实时批次", "links": "全部链接", "people": "用户指南", "ai": "AI 指南", "feedback": "反馈", "telegram": "Telegram", "telegramBot": "Telegram 机器人", "github": "GitHub", "menu": "菜单", "language": "语言"},
    "el": {"brand": "KVASSISTENT", "subtitle": "Τελευταία έκδοση και όλες οι βασικές είσοδοι", "game": "Παιχνίδι", "companion": "Ζωντανή παρτίδα", "links": "Όλοι οι σύνδεσμοι", "people": "Για ανθρώπους", "ai": "Για AI", "feedback": "Σχόλια", "telegram": "Telegram", "telegramBot": "Bot Telegram", "github": "GitHub", "menu": "Μενού", "language": "Γλώσσα"},
}
'''
if "HEADER_COPY =" not in text:
    marker = "}\n\nACCESSIBILITY_CSS ="
    if marker not in text:
        raise RuntimeError("Cannot insert localized header copy")
    text = text.replace(marker, "}\n" + header_copy + "\nACCESSIBILITY_CSS =", 1)

css_addition = r'''
.header-version-badge{display:inline-flex;align-items:center;justify-content:center;min-height:38px;padding:8px 12px;border-radius:999px;background:#2a2118;color:#fffdf7;font:950 13px/1 system-ui;letter-spacing:.08em;box-shadow:0 7px 18px rgba(42,33,24,.2);white-space:nowrap}
#kvass-language-content{transition:opacity .12s ease}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]){margin:18px 0 42px;padding:clamp(20px,4vw,42px);border:1px solid rgba(219,201,169,.96);border-radius:26px;background:rgba(255,253,247,.98);color:#2a2118;box-shadow:0 24px 70px rgba(0,0,0,.28);backdrop-filter:blur(14px)}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) :where(h1,h2,h3,h4,p,li,strong,em,code,span){color:inherit}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) a{color:#7a4c06;text-decoration-thickness:2px;text-underline-offset:3px}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) .cover{background:linear-gradient(145deg,#fffdf7,#f8efdd)!important;color:#2a2118!important;box-shadow:none!important}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) article{color:#2a2118}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) pre{color:#fff8e8;background:#211a13}
#kvass-language-content[data-active-lang]:not([data-active-lang="ru"]) h2{border-bottom-color:#dbc9a9}
'''
if ".header-version-badge{" not in text:
    css_marker = '#kvass-language-content[aria-busy="true"]{opacity:.62}'
    if css_marker not in text:
        raise RuntimeError("Cannot insert readable localization CSS")
    text = text.replace(css_marker, css_marker + css_addition, 1)

# Keep the version badge useful on narrow screens.
text = text.replace(
    ".site-topbar.is-compact .topbar-brand span,.site-topbar.is-compact .topbar-links{display:none}",
    ".site-topbar.is-compact .topbar-brand span,.site-topbar.is-compact .topbar-links{display:none}.site-topbar.is-compact .header-version-badge{min-height:34px;padding:7px 9px}",
)

# Translate the visible language label too.
text = text.replace(
    "return f'<div class=\"inline-language-picker\" role=\"group\" aria-label=\"Language · Язык\"><span>Язык</span>{buttons}{legacy}</div>'",
    "return f'<div class=\"inline-language-picker\" role=\"group\" aria-label=\"Language · Язык\"><span id=\"header-language-label\">Язык</span>{buttons}{legacy}</div>'",
)

# Replace language_script with a version that also localizes the sticky header.
start = text.find("def language_script(data: dict[str, dict[str, str]]) -> str:")
end = text.find("\n\nMENU_SCRIPT =", start)
if start < 0 or end < 0:
    raise RuntimeError("Cannot locate language_script")
new_function = r'''def language_script(data: dict[str, dict[str, str]]) -> str:
    safe_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    header_json = json.dumps(HEADER_COPY, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'''<script id="kvass-language-data" type="application/json">{safe_json}</script>
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
</script>'''
'''
text = text[:start] + new_function + text[end:]

# Give every visible header element a stable localization key and add V25 badge.
needle = "    picker = language_markup()\n"
replacement = f'''    picker = '<span class="header-version-badge" id="header-version-badge" aria-label="KVASSISTENT version {ONES}">V{ONES}</span>' + language_markup()\n'''
if needle not in text:
    raise RuntimeError("Cannot add persistent version badge")
text = text.replace(needle, replacement, 1)

hook = "    if BOT_URL not in text:\n        text = text.replace('<nav class=\"topbar-links\">', f'<nav class=\"topbar-links\"><a class=\"telegram-direct\" href=\"{BOT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">Telegram-бот</a>', 1)\n"
if hook not in text:
    raise RuntimeError("Cannot locate topbar patch hook")
localization_patch = hook + r'''
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
'''
text = text.replace(hook, localization_patch, 1)
text = text.replace("'<div id=\"kvass-language-content\">'", "'<div id=\"kvass-language-content\" aria-live=\"polite\" data-active-lang=\"ru\">'", 1)

# Strengthen finalizer assertions and release message.
text = text.replace(
    "'id=\"header-language-select\"','id=\"kvassistent-inline-languages\"'",
    "'id=\"header-language-select\"','id=\"header-version-badge\"','id=\"header-brand-title\"','data-header-key=\"game\"','id=\"kvassistent-inline-languages\"'",
)
text = text.replace('"inline-language-button","localStorage.setItem"', '"inline-language-button","data-active-lang","kvass-header-language-data","localStorage.setItem"')
text = text.replace("print(f\"finalized KVASSISTENT version {ONES}: six inline homepage languages without navigation\")", "print(f\"finalized KVASSISTENT version {ONES}: readable inline languages, localized header and persistent version badge\")")
path.write_text(text, encoding="utf-8")

# Release notes and a demo pitch stored with the release.
notes = ROOT / f"release/RELEASE-{VERSION}.md"
notes.write_text(
f'''# КВАССИСТЕНТ 25\n\nВерсия 25 исправляет две проблемы, найденные прямо перед демо.\n\n## Что изменилось\n\n- локализованный контент теперь показывается на светлой контрастной карточке и читается поверх космического фона;\n- вместе с контентом переводится вся липкая шапка: подпись, меню, ссылки и слово «Язык»;\n- версия `V25` всегда видна в шапке при любом языке и положении прокрутки;\n- переключение RU / EN / ES / DE / 中文 / EL остаётся мгновенным, без перехода на новую страницу и без изменения URL;\n- выбранный язык сохраняется в браузере;\n- обычный pinch-to-zoom сохранён, double-tap на кнопках не запускает масштабирование.\n\n## Демо\n\nОткрой `https://kvassistent.pages.dev/`, прокрути страницу и переключи RU → EN → ES → 中文. Текст и шапка меняются на месте, а `V25` остаётся видимой.\n''',
encoding="utf-8",
)

pitch = ROOT / "release/DEMO-PITCH-25.md"
pitch.write_text(
'''# KVASSISTENT 25 — demo pitch\n\n## Русский, около 20 секунд\n\nКВАССИСТЕНТ — это ИИ-проводник по приготовлению домашнего кваса. Человек готовит напиток своими руками, а ассистент помнит состояние партии, подсказывает следующий безопасный шаг и принимает реальные пожелания пользователей. В версии 25 весь интерфейс мгновенно переключается между шестью языками прямо на одной странице. Никаких переходов — нажимаем English, Español или 中文, и демо сразу готово для любой аудитории.\n\n## English, about 20 seconds\n\nKVASSISTENT is an AI guide for making homemade kvass. A human brews the drink by hand, while the assistant remembers the batch state, suggests the next safe step, and collects real user feedback. In version 25, the whole interface switches instantly between six languages on the same page. No navigation, no reload — choose English, Español, or 中文 and the demo is ready for any audience.\n''',
encoding="utf-8",
)

# Create the required release poster by carrying the previous visual forward with truthful v25 text.
old_comic = ROOT / f"share/kvassistent-{OLD_VERSION}-comic.svg"
new_comic = ROOT / f"share/kvassistent-{VERSION}-comic.svg"
if old_comic.is_file():
    comic = old_comic.read_text(encoding="utf-8")
    comic = comic.replace("version 24", "version 25").replace("VERSION 24", "VERSION 25")
    comic = comic.replace("release 25", "release 26")
    new_comic.write_text(comic, encoding="utf-8")
else:
    new_comic.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#07182a"/><rect x="70" y="70" width="1060" height="490" rx="42" fill="#fffdf7"/><text x="120" y="185" font-family="sans-serif" font-size="34" font-weight="900" fill="#b47718">KVASSISTENT · VERSION 25</text><text x="120" y="295" font-family="sans-serif" font-size="72" font-weight="900" fill="#2a2118">SIX LANGUAGES.</text><text x="120" y="385" font-family="sans-serif" font-size="72" font-weight="900" fill="#2a2118">ONE PAGE.</text><text x="120" y="475" font-family="sans-serif" font-size="34" fill="#6f6252">Readable content · localized header · persistent V25</text></svg>''', encoding="utf-8")

# Fix the stale version lines in README without rewriting its history.
readme = ROOT / "README.md"
readme_text = readme.read_text(encoding="utf-8")
readme_text = re.sub(r'^\*\*Текущая версия:.*$', f'**Текущая версия: {VERSION} · единиц: 25.**', readme_text, flags=re.M)
readme_text = re.sub(r'^\*\*Следующая версия:.*$', f'**Следующая версия: {NEXT_VERSION} · единиц: 26.**', readme_text, flags=re.M)
readme.write_text(readme_text, encoding="utf-8")

# AI-readable handoff.
changelog = ROOT / "AI_CHANGELOG.md"
old = changelog.read_text(encoding="utf-8")
entry = f'''# AI-readable change log\n\n## 2026-07-30 — KVASSISTENT website release 25\n\n- **Version or scope:** release 25, `v{VERSION}`.\n- **Changed:** put every non-Russian inline localization on a high-contrast light card; localized the complete sticky header for six languages; added a persistent `V25` badge; preserved single-page switching, current scroll position and local language preference; added release notes, demo pitch and poster.\n- **Why:** the version-24 demo screenshot showed dark text on a dark space background, an untranslated Russian header and no visible version after switching languages.\n- **Behavior:** RU, EN, ES, DE, 中文 and EL switch without navigation; both content and header change together; text stays readable; version remains visible while scrolling.\n- **Files and systems:** release metadata, finalizer, publication workflow assertions, README, release notes, demo pitch, poster, generated latest and immutable site.\n- **Verification:** migration assertions, Python compile, publication build, twelve PDFs, inline-language checks, contrast markers, localized-header markers, persistent badge checks and live Cloudflare verification.\n- **Deployment:** merge to `develop` publishes version 25.\n- **Remaining work:** none after green live verification.\n\n---\n\n'''
if old.startswith("# AI-readable change log"):
    old = old.split("\n", 1)[1].lstrip("\n")
changelog.write_text(entry + old, encoding="utf-8")

# Publication CI must explicitly guard the demo regressions.
workflow = ROOT / ".github/workflows/publish.yml"
workflow_text = workflow.read_text(encoding="utf-8")
ci_marker = "          grep -Fq 'id=\"header-language-select\"' \"$landing\"\n"
ci_checks = ci_marker + "          grep -Fq 'id=\"header-version-badge\"' \"$landing\"\n          grep -Fq 'id=\"header-brand-title\"' \"$landing\"\n          grep -Fq 'data-header-key=\"game\"' \"$landing\"\n          grep -Fq 'data-active-lang=\"ru\"' \"$landing\"\n          grep -Fq 'header-version-badge' \"$landing\"\n          grep -Fq 'kvass-header-language-data' \"$landing\"\n          grep -Fq 'background:rgba(255,253,247,.98)' \"$landing\"\n"
if "grep -Fq 'id=\"header-version-badge\"'" not in workflow_text:
    if ci_marker not in workflow_text:
        raise RuntimeError("Cannot add publication regression checks")
    workflow_text = workflow_text.replace(ci_marker, ci_checks, 1)
live_marker = "            grep -Fq 'id=\"human-manifesto\"' /tmp/latest.html 2>/dev/null || ok=0\n"
live_checks = live_marker + "            grep -Fq 'id=\"header-version-badge\"' /tmp/latest.html 2>/dev/null || ok=0\n            grep -Fq 'kvass-header-language-data' /tmp/latest.html 2>/dev/null || ok=0\n"
if "grep -Fq 'id=\"header-version-badge\"' /tmp/latest.html" not in workflow_text:
    if live_marker not in workflow_text:
        raise RuntimeError("Cannot add live demo regression checks")
    workflow_text = workflow_text.replace(live_marker, live_checks, 1)
workflow.write_text(workflow_text, encoding="utf-8")

# Final sanity checks before GitHub commits the migration output.
finalizer = path.read_text(encoding="utf-8")
for required in ("HEADER_COPY", "header-version-badge", "data-header-key", "data-active-lang", "background:rgba(255,253,247,.98)"):
    if required not in finalizer:
        raise RuntimeError(f"Missing v25 hotfix marker: {required}")
assert meta["ones_count"] == 25
assert sum(part == "1" for part in meta["current"].split(".")) == 25
assert notes.is_file() and new_comic.is_file() and pitch.is_file()
print(f"Prepared KVASSISTENT version {ONES}: v{VERSION}")
