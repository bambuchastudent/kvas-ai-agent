#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
SITE = ROOT / "dist/site"

LANG_ROUTES = {
    "ru": {"human": "/ru/summary/", "agent": "/ru/instructions/"},
    "en": {"human": "/en/summary/", "agent": "/en/instructions/"},
    "es": {"human": "/es/summary/", "agent": "/es/instructions/"},
    "de": {"human": "/de/summary/", "agent": "/de/instructions/"},
    "zh-CN": {"human": "/zh-CN/summary/", "agent": "/zh-CN/instructions/"},
    "el": {"human": "/el/summary/", "agent": "/el/instructions/"},
}

MENU_CSS = r"""
/* kvassistent-compact-menu */
.menu-toggle{display:none;align-items:center;gap:7px;padding:9px 12px;border:1px solid rgba(180,119,24,.28);border-radius:999px;background:#fff;color:#2a2118;font:800 15px/1 system-ui;cursor:pointer}
.menu-toggle:focus-visible{outline:3px solid rgba(180,119,24,.35);outline-offset:2px}
@media(max-width:760px){
  .site-topbar{transition:padding .18s ease,border-radius .18s ease,box-shadow .18s ease}
  .menu-toggle{display:inline-flex;margin-left:auto}
  .site-topbar.is-compact{padding:8px 10px;gap:8px;border-radius:0 0 16px 16px;box-shadow:0 10px 28px rgba(0,0,0,.22)}
  .site-topbar.is-compact .topbar-brand{flex:1;min-width:0}
  .site-topbar.is-compact .topbar-brand span,
  .site-topbar.is-compact .topbar-links,
  .site-topbar.is-compact .header-language label,
  .site-topbar.is-compact .header-language a{display:none}
  .site-topbar.is-compact .topbar-brand strong{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .site-topbar.is-compact .header-language{display:flex;width:auto;margin-left:0}
  .site-topbar.is-compact .header-language select{min-width:0;max-width:132px;padding:7px 9px}
  .site-topbar.is-compact[data-expanded="true"]{padding:14px;align-items:flex-start}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand{width:calc(100% - 90px)}
  .site-topbar.is-compact[data-expanded="true"] .topbar-brand span{display:block}
  .site-topbar.is-compact[data-expanded="true"] .topbar-links,
  .site-topbar.is-compact[data-expanded="true"] .header-language{display:flex;width:100%}
  .site-topbar.is-compact[data-expanded="true"] .header-language label,
  .site-topbar.is-compact[data-expanded="true"] .header-language a{display:inline-flex}
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

  const currentLang = Object.prototype.hasOwnProperty.call(routes, document.documentElement.lang)
    ? document.documentElement.lang
    : "ru";

  const applyLinks = (lang) => {
    const route = routes[lang] || routes.ru;
    if (human) human.href = route.human;
    if (agent) agent.href = route.agent;
    return route;
  };

  if (select) {
    select.value = currentLang;
    applyLinks(select.value);
    select.addEventListener("change", () => {
      const route = applyLinks(select.value);
      window.location.assign(route.human);
    });
  }

  const setExpanded = (expanded) => {
    if (!topbar) return;
    topbar.dataset.expanded = expanded ? "true" : "false";
    if (toggle) toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
  };

  const syncCompactState = () => {
    if (!topbar) return;
    const compact = window.scrollY > 120;
    topbar.classList.toggle("is-compact", compact);
    if (!compact) setExpanded(false);
  };

  if (toggle) {
    toggle.addEventListener("click", () => {
      const expanded = topbar?.dataset.expanded === "true";
      setExpanded(!expanded);
    });
  }

  window.addEventListener("scroll", syncCompactState, { passive: true });
  syncCompactState();
})();
</script>"""

MENU_SCRIPT = MENU_SCRIPT_TEMPLATE.replace(
    "__ROUTES__",
    json.dumps(LANG_ROUTES, ensure_ascii=False, separators=(",", ":")),
)

OLD_LANGUAGE_SCRIPT = re.compile(
    r'<script>\s*\(\(\)\s*=>\s*\{.*?header-language-select.*?</script>',
    re.S,
)


def patch_landing(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<header class="site-topbar web-only" id="site-topbar">',
        '<header class="site-topbar web-only" id="site-topbar" data-expanded="false">',
        1,
    )
    if 'id="menu-toggle"' not in text:
        text = text.replace(
            '<nav class="topbar-links">',
            '<button class="menu-toggle" id="menu-toggle" type="button" '
            'aria-controls="site-topbar" aria-expanded="false">☰ <span>Меню</span></button>'
            '<nav class="topbar-links">',
            1,
        )
    if "kvassistent-compact-menu" not in text:
        text = text.replace("</style>", MENU_CSS + "\n</style>", 1)

    if 'id="kvassistent-navigation"' not in text:
        text, replaced = OLD_LANGUAGE_SCRIPT.subn(MENU_SCRIPT, text, count=1)
        if replaced == 0:
            text = text.replace("</body>", MENU_SCRIPT + "\n</body>", 1)

    path.write_text(text, encoding="utf-8")


def telegram_page() -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KVASSISTENT Telegram · Version {ONES}</title>
<meta name="description" content="Telegram feedback for KVASSISTENT: send a kvass idea to the creator and receive an encouraging reply.">
<style>
:root{{--bg:#050812;--card:#0a1b31;--line:#4da9e9;--ink:#eef8ff;--muted:#b9d8ed;--accent:#62c4ff}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;background:radial-gradient(circle at 30% 20%,#263c77,#050812 65%);color:var(--ink);font:18px/1.55 system-ui}}
main{{max-width:820px;margin:0 auto;padding:24px}}
.card{{margin:20px 0;padding:clamp(24px,5vw,42px);border:1px solid var(--line);border-radius:28px;background:rgba(4,17,34,.94);box-shadow:0 24px 70px rgba(0,0,0,.35)}}
a{{color:#7bd2ff}}code{{background:#071d30;padding:.2em .45em;border-radius:.4em}}
.answer,.status{{padding:16px 18px;border-radius:16px;background:#0c3454;color:#fff}}
.status[data-kind="error"]{{background:#5a2020}}.status[data-kind="ok"]{{background:#174a35}}
form{{display:grid;gap:14px;margin-top:22px}}label{{display:grid;gap:7px;font-weight:800}}
input,textarea,button{{font:inherit}}input,textarea{{width:100%;padding:12px 14px;border:1px solid #47769b;border-radius:12px;background:#07182a;color:#fff}}
textarea{{min-height:150px;resize:vertical}}button{{padding:13px 18px;border:0;border-radius:999px;background:var(--accent);color:#04111d;font-weight:900;cursor:pointer}}
button[disabled]{{opacity:.55;cursor:wait}}.trap{{position:absolute;left:-9999px}}.small{{color:var(--muted);font-size:.92rem}}
</style>
</head>
<body>
<main>
<section class="card">
<p>KVASSISTENT · Version {ONES}</p>
<h1>Telegram-бот и обратная связь</h1>
<p class="answer">Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤</p>
<p id="bot-status" class="status">Проверяю подключение Telegram…</p>
<p id="bot-link-wrap" hidden><a id="bot-link" rel="noopener">Открыть бота в Telegram →</a></p>
</section>
<section class="card">
<h2>Написать автору</h2>
<p class="small">Сообщение отправляется через Telegram-бота. История на сайте не хранится.</p>
<form id="feedback-form">
<label>Как тебя назвать<input name="name" maxlength="80" autocomplete="name" placeholder="Имя или ник"></label>
<label>Как ответить<input name="contact" maxlength="180" autocomplete="email" placeholder="@telegram или email"></label>
<label>Что за квас ты задумал<textarea name="message" minlength="10" maxlength="2000" required placeholder="Расскажи идею, пропорции или проблему"></textarea></label>
<label class="trap" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
<button type="submit">Отправить через Telegram</button>
<p id="form-result" class="status" hidden></p>
</form>
</section>
<p><a href="/">← Вернуться к КВАССИСТЕНТУ</a> · <a href="https://github.com/bambuchastudent/kvas-ai-agent/tree/develop/telegram-bot">Код бота</a></p>
</main>
<script>
(() => {{
  const status = document.getElementById("bot-status");
  const linkWrap = document.getElementById("bot-link-wrap");
  const link = document.getElementById("bot-link");
  const form = document.getElementById("feedback-form");
  const result = document.getElementById("form-result");

  const setMessage = (node, text, kind) => {{
    node.textContent = text;
    node.dataset.kind = kind || "";
    node.hidden = false;
  }};

  fetch("/api/telegram/status", {{ cache: "no-store" }})
    .then((response) => response.json())
    .then((data) => {{
      if (data.configured) {{
        setMessage(status, "Telegram подключён. Можно писать боту или отправить форму ниже.", "ok");
      }} else {{
        setMessage(status, "Код бота опубликован, но секреты Telegram ещё не подключены.", "error");
      }}
      if (data.bot_url) {{
        link.href = data.bot_url;
        linkWrap.hidden = false;
      }}
    }})
    .catch(() => setMessage(status, "Не удалось проверить Telegram. Попробуй позже.", "error"));

  form.addEventListener("submit", async (event) => {{
    event.preventDefault();
    const button = form.querySelector("button");
    button.disabled = true;
    result.hidden = true;
    try {{
      const payload = Object.fromEntries(new FormData(form).entries());
      const response = await fetch("/api/telegram/feedback", {{
        method: "POST",
        headers: {{ "content-type": "application/json" }},
        body: JSON.stringify(payload),
      }});
      const data = await response.json().catch(() => ({{}}));
      if (!response.ok) throw new Error(data.error || "Не получилось отправить сообщение");
      setMessage(result, data.message || "Сообщение отправлено. Ай да хорош!", "ok");
      form.reset();
    }} catch (error) {{
      setMessage(result, error.message || "Не получилось отправить сообщение", "error");
    }} finally {{
      button.disabled = false;
    }}
  }});
}})();
</script>
</body>
</html>"""


def install_telegram() -> None:
    worker_source = ROOT / "telegram-bot/worker.js"
    if not worker_source.is_file():
        raise RuntimeError("Missing telegram-bot/worker.js")
    shutil.copy2(worker_source, SITE / "_worker.js")
    (SITE / "_routes.json").write_text(
        json.dumps(
            {"version": 1, "include": ["/api/telegram/*"], "exclude": []},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for root in (SITE, SITE / f"v{VERSION}"):
        target = root / "telegram/index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(telegram_page(), encoding="utf-8")


for landing in (SITE / "index.html", SITE / f"v{VERSION}/index.html"):
    if not landing.is_file():
        raise RuntimeError(f"Missing landing page: {landing}")
    patch_landing(landing)

install_telegram()

required_agent_files = (
    ROOT / "PROJECT_GOAL.md",
    ROOT / ".github/copilot-instructions.md",
)
for path in required_agent_files:
    if not path.is_file():
        raise RuntimeError(f"Missing GitHub agent context: {path.relative_to(ROOT)}")

latest_landing = (SITE / "index.html").read_text(encoding="utf-8")
telegram_html = (SITE / "telegram/index.html").read_text(encoding="utf-8")
worker = (SITE / "_worker.js").read_text(encoding="utf-8")
for required in (
    'id="menu-toggle"',
    "kvassistent-compact-menu",
    "window.location.assign(route.human)",
    'id="kvassistent-navigation"',
):
    if required not in latest_landing:
        raise RuntimeError(f"Language/menu finalization missing: {required}")
for required in (
    'id="feedback-form"',
    "/api/telegram/status",
    "/api/telegram/feedback",
):
    if required not in telegram_html:
        raise RuntimeError(f"Telegram page finalization missing: {required}")
for required in (
    "/api/telegram/webhook",
    "/api/telegram/admin/setup",
    "TELEGRAM_OWNER_CHAT_ID",
    "setWebhook",
    "sendMessage",
):
    if required not in worker:
        raise RuntimeError(f"Telegram worker finalization missing: {required}")

print(
    f"finalized KVASSISTENT version {ONES}: simple language routing, compact menu, "
    "GitHub agent context, and Telegram feedback worker"
)
