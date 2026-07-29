#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
SITE = ROOT / "dist/site"
BOT_URL = "https://t.me/kvassistent_bot"
REPO_URL = "https://github.com/bambuchastudent/kvas-ai-agent"

LANG_ROUTES = {
    "ru": {"human": "/ru/summary/", "agent": "/ru/instructions/"},
    "en": {"human": "/en/summary/", "agent": "/en/instructions/"},
    "es": {"human": "/es/summary/", "agent": "/es/instructions/"},
    "de": {"human": "/de/summary/", "agent": "/de/instructions/"},
    "zh-CN": {"human": "/zh-CN/summary/", "agent": "/zh-CN/instructions/"},
    "el": {"human": "/el/summary/", "agent": "/el/instructions/"},
}

ACCESSIBILITY_CSS = r"""
/* kvassistent-safe-interactions-v23 */
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
@media(max-width:760px){
  .site-topbar{transition:padding .18s ease,border-radius .18s ease,box-shadow .18s ease}
  .menu-toggle{display:inline-flex;margin-left:auto}
  .site-topbar.is-compact{padding:8px 10px;gap:8px;border-radius:0 0 16px 16px;box-shadow:0 10px 28px rgba(0,0,0,.22)}
  .site-topbar.is-compact .topbar-brand{flex:1;min-width:0}
  .site-topbar.is-compact .topbar-brand span,.site-topbar.is-compact .topbar-links,.site-topbar.is-compact .header-language label,.site-topbar.is-compact .header-language a{display:none}
  .site-topbar.is-compact .topbar-brand strong{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .site-topbar.is-compact .header-language{display:flex;width:auto;margin-left:0}
  .site-topbar.is-compact .header-language select{min-width:0;max-width:132px;padding:7px 9px}
  .site-topbar.is-compact[data-expanded="true"]{padding:14px;align-items:flex-start}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand{width:calc(100% - 90px)}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand span{display:block}
  .site-topbar.is-compact[data-expanded="true"] .topbar-links,.site-topbar.is-compact[data-expanded="true"] .header-language{display:flex;width:100%}
  .site-topbar.is-compact[data-expanded="true"] .header-language label,.site-topbar.is-compact[data-expanded="true"] .header-language a{display:inline-flex}
  .site-topbar.is-compact[data-expanded="true"] .header-language select{max-width:none;flex:1}
}
"""

MENU_SCRIPT_TEMPLATE = r"""<script id="kvassistent-navigation">
(() => {
  const routes = __ROUTES__;
  const select = document.getElementById("header-language-select");
  const human = document.getElementById("header-human-link");
  const agent = document.getElementById("header-agent-link");
  const topbar = document.getElementById("site-topbar");
  const toggle = document.getElementById("menu-toggle");
  const currentLang = Object.prototype.hasOwnProperty.call(routes, document.documentElement.lang) ? document.documentElement.lang : "ru";
  const applyLinks = (lang) => { const route = routes[lang] || routes.ru; if (human) human.href = route.human; if (agent) agent.href = route.agent; return route; };
  if (select) { select.value = currentLang; applyLinks(select.value); select.addEventListener("change", () => window.location.assign(applyLinks(select.value).human)); }
  const setExpanded = (expanded) => { if (!topbar) return; topbar.dataset.expanded = expanded ? "true" : "false"; if (toggle) toggle.setAttribute("aria-expanded", expanded ? "true" : "false"); };
  const syncCompactState = () => { if (!topbar) return; const compact = window.scrollY > 120; topbar.classList.toggle("is-compact", compact); if (!compact) setExpanded(false); };
  let lastToggleAt = 0;
  if (toggle) toggle.addEventListener("click", () => { const now = performance.now(); if (now - lastToggleAt < 450) return; lastToggleAt = now; setExpanded(topbar?.dataset.expanded !== "true"); });
  window.addEventListener("scroll", syncCompactState, { passive: true }); syncCompactState();
})();
</script>"""

MENU_SCRIPT = MENU_SCRIPT_TEMPLATE.replace("__ROUTES__", json.dumps(LANG_ROUTES, ensure_ascii=False, separators=(",", ":")))
OLD_LANGUAGE_SCRIPT = re.compile(r'<script>\s*\(\(\)\s*=>\s*\{.*?header-language-select.*?</script>', re.S)


def patch_landing(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace('<header class="site-topbar web-only" id="site-topbar">', '<header class="site-topbar web-only" id="site-topbar" data-expanded="false">', 1)
    if 'id="menu-toggle"' not in text:
        text = text.replace('<nav class="topbar-links">', '<button class="menu-toggle" id="menu-toggle" type="button" aria-controls="site-topbar" aria-expanded="false">☰ <span>Меню</span></button><nav class="topbar-links">', 1)
    if BOT_URL not in text:
        text = text.replace('<nav class="topbar-links">', f'<nav class="topbar-links"><a class="telegram-direct" href="{BOT_URL}" target="_blank" rel="noopener noreferrer">Telegram-бот</a>', 1)
    if "kvassistent-compact-menu" not in text:
        text = text.replace("</style>", MENU_CSS + "\n</style>", 1)
    if 'id="kvassistent-navigation"' not in text:
        text, replaced = OLD_LANGUAGE_SCRIPT.subn(MENU_SCRIPT, text, count=1)
        if replaced == 0:
            text = text.replace("</body>", MENU_SCRIPT + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")


def install_safe_interactions() -> None:
    marker = "kvassistent-safe-interactions-v23"
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
    return f"""<!doctype html>
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
  <section class="card"><h2>Что бот умеет</h2><ul class="features">
    <li><strong>Короткий рецепт</strong><br>Процеживание через чистую марлю, сложенный бинт или пищевой фильтровальный мешок.</li>
    <li><strong>Разбор партии</strong><br>Температура, время, поверхность, запах, вкус и газированность.</li>
    <li><strong>Пожелания</strong><br>Новые содержательные идеи становятся задачами релиза 24.</li>
    <li><strong>Фотографии</strong><br>Одинаковые фото с одинаковой подписью не дублируются.</li>
  </ul></section>
  <section class="card"><h2>Все основные ссылки</h2><nav class="links">
    <a href="/">Главная</a><a href="/feedback/">Обратная связь</a><a href="/companion/">Живая партия</a><a href="/game/">Игра</a><a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">GitHub</a>
  </nav><p class="small">Версия {ONES}: v{VERSION}</p></section>
</main></body></html>"""


def install_telegram() -> None:
    for root in (SITE, SITE / f"v{VERSION}"):
        target = root / "telegram/index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(telegram_page(), encoding="utf-8")


for landing in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    if not landing.is_file():
        raise RuntimeError(f"Missing landing page: {landing}")
    patch_landing(landing)

install_telegram()
install_safe_interactions()

for required in (ROOT / "PROJECT_GOAL.md", ROOT / ".github/copilot-instructions.md"):
    if not required.is_file():
        raise RuntimeError(f"Missing GitHub agent context: {required.relative_to(ROOT)}")

latest_landing = (SITE / "index.html").read_text(encoding="utf-8")
telegram_html = (SITE / "telegram/index.html").read_text(encoding="utf-8")
for required in ('id="menu-toggle"', "kvassistent-compact-menu", BOT_URL, 'id="kvassistent-navigation"', "kvassistent-safe-interactions-v23", "touch-action:manipulation", "prefers-reduced-motion"):
    if required not in latest_landing:
        raise RuntimeError(f"Landing finalization missing: {required}")
for required in (BOT_URL, "@kvassistent_bot", f"ВЕРСИЯ {ONES}", "Ай да какой ты квас задумал", "пищевой фильтровальный мешок", "релиза 24"):
    if required not in telegram_html:
        raise RuntimeError(f"Telegram page finalization missing: {required}")

print(f"finalized KVASSISTENT version {ONES}: safe motion, touch controls, smart Telegram recipe and release feedback")
