#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
VERSION = str(META["current"])
ONES = int(META["ones_count"])
SITE = ROOT / "dist/site"


def creator_text() -> str:
    source = (ROOT / "HUMAN_MANIFESTO.md").read_text(encoding="utf-8")
    start = source.index("ЭТО ТВОЙ КВАС")
    end = source.index("\n## Meaning for collaborators")
    return source[start:end].rstrip()


SPACE_CSS = r"""
body{position:relative;background:#03050d!important;color:#f8f3df;overflow-x:hidden}
body::before{content:"";position:fixed;inset:-10%;z-index:0;pointer-events:none;background:
radial-gradient(1200px 800px at 15% 20%,rgba(128,82,255,.32),transparent 55%),
radial-gradient(900px 700px at 85% 15%,rgba(39,170,255,.22),transparent 55%),
radial-gradient(1000px 900px at 60% 92%,rgba(255,168,45,.15),transparent 55%),
radial-gradient(circle at center,#0a0f22 0%,#03050d 65%)}
body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:
radial-gradient(circle,#fff 0 1px,transparent 1.5px) 0 0/54px 54px,
radial-gradient(circle,rgba(255,255,255,.55) 0 1px,transparent 1.5px) 27px 27px/94px 94px,
radial-gradient(circle,rgba(255,255,255,.35) 0 .8px,transparent 1.4px) 13px 41px/140px 140px;
animation:kvass-twinkle 6s ease-in-out infinite}
main,footer{position:relative;z-index:2}
.kvass-space-layer{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.kvass-orbit{position:absolute;top:50%;left:50%;width:0;height:0;animation:kvass-spin linear infinite}
.kvass-orbit:nth-child(1){animation-duration:38s}
.kvass-orbit:nth-child(2){animation-duration:52s;animation-direction:reverse}
.kvass-orbit:nth-child(3){animation-duration:44s;animation-delay:-12s}
.kvass-orbit:nth-child(4){animation-duration:66s;animation-direction:reverse;animation-delay:-22s}
.kvass-orbit:nth-child(5){animation-duration:30s;animation-delay:-4s}
.kvass-orbit:nth-child(6){animation-duration:74s;animation-direction:reverse;animation-delay:-30s}
.kvass-satellite{position:absolute;left:0;top:0;width:26px;height:70px;transform-origin:center center;
border:2px solid rgba(255,231,166,.85);border-radius:9px 9px 13px 13px;
background:linear-gradient(90deg,rgba(255,255,255,.28),rgba(110,58,12,.9) 38%,rgba(30,15,5,.98));
box-shadow:0 0 22px rgba(255,186,72,.42),0 0 46px rgba(255,120,32,.22)}
.kvass-orbit:nth-child(1) .kvass-satellite{translate:340px -35px;rotate:90deg}
.kvass-orbit:nth-child(2) .kvass-satellite{translate:470px -35px;rotate:90deg;scale:.9}
.kvass-orbit:nth-child(3) .kvass-satellite{translate:230px -35px;rotate:90deg;scale:.75}
.kvass-orbit:nth-child(4) .kvass-satellite{translate:560px -35px;rotate:90deg;scale:.85}
.kvass-orbit:nth-child(5) .kvass-satellite{translate:150px -35px;rotate:90deg;scale:.6}
.kvass-orbit:nth-child(6) .kvass-satellite{translate:640px -35px;rotate:90deg;scale:.7}
.kvass-satellite::before{content:"";position:absolute;left:6px;top:-18px;width:12px;height:20px;
border:2px solid rgba(255,231,166,.85);border-bottom:0;border-radius:5px 5px 0 0;background:#6b2f0b}
.kvass-satellite::after{content:"КВАС";position:absolute;left:3px;right:3px;top:29px;padding:3px 0;
border-radius:4px;background:#f2c05c;color:#201005;font:900 8px/1 sans-serif;text-align:center;letter-spacing:.5px}
.kvass-flame{position:absolute;left:50%;bottom:-30px;width:10px;height:34px;translate:-50% 0;
background:radial-gradient(ellipse at top,rgba(255,240,120,.95),rgba(255,120,32,.75) 40%,transparent 78%);
filter:blur(2px);border-radius:50%;animation:kvass-flicker .18s steps(2) infinite}
@keyframes kvass-spin{to{rotate:360deg}}
@keyframes kvass-flicker{0%{opacity:.7;scale:1 .9}100%{opacity:1;scale:1.15 1.15}}
@keyframes kvass-twinkle{0%,100%{opacity:.85}50%{opacity:1}}
.human-manifesto-release,.telegram-release{margin:30px 0;padding:clamp(22px,5vw,44px);border-radius:28px;position:relative;overflow:hidden}
.human-manifesto-release{border:2px solid rgba(255,207,98,.72);background:linear-gradient(145deg,rgba(22,13,44,.96),rgba(7,19,48,.96));color:#fff8df;box-shadow:0 24px 70px rgba(0,0,0,.35)}
.human-manifesto-release::before{content:"ORIGINAL HUMAN SIGNAL";position:absolute;right:18px;top:15px;color:rgba(255,222,143,.5);font:900 11px/1 sans-serif;letter-spacing:2px}
.manifesto-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(250px,.8fr);gap:20px;margin-top:22px}.manifesto-original,.manifesto-explained{padding:20px;border-radius:20px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14)}
.manifesto-original pre{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;color:#fff8df;font:700 clamp(14px,2vw,18px)/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}.manifesto-explained p{color:#d8e4ff}.manifesto-explained strong{color:#ffd778}.manifesto-kicker{color:#ffd778;font-weight:900;letter-spacing:.08em;text-transform:uppercase}
.telegram-release{border:2px solid #4da9e9;background:linear-gradient(135deg,#07182d,#0b3150);color:#eef8ff}.telegram-release h2{color:#fff}.telegram-release p{color:#c8e6f7}.telegram-release a{display:inline-flex;padding:13px 18px;border-radius:999px;background:#55acee;color:#06111d;text-decoration:none;font-weight:950}
@media(max-width:760px){.manifesto-grid{grid-template-columns:1fr}.kvass-orbit:nth-child(n+4){display:none}}
@media(prefers-reduced-motion:reduce){.kvass-orbit,.kvass-satellite,.kvass-flame,body::after{animation:none}}
"""


def manifesto_section() -> str:
    original = html.escape(creator_text())
    return f"""
<section class="human-manifesto-release" id="human-manifesto">
  <div class="manifesto-kicker">Человек написал первым · Human-authored comes first</div>
  <h2>ЭТО ТВОЙ КВАС</h2>
  <p>Оригинальный текст сохранён дословно. Профессиональное объяснение стоит рядом, а не вместо него.</p>
  <div class="manifesto-grid">
    <div class="manifesto-original"><pre>{original}</pre></div>
    <div class="manifesto-explained">
      <h3>What this means</h3>
      <p><strong>KVASSISTENT is human-first AI for manual craft.</strong></p>
      <p>You dry the bread, mix the wort, observe the jar, smell it, taste it, and decide. AI remembers the state, explains risk, and asks for the next observation without pretending it can see or smell the batch.</p>
      <p><strong>Humans brew. AI guides.</strong></p>
    </div>
  </div>
</section>
<section class="telegram-release" id="telegram">
  <div class="manifesto-kicker">Version {ONES} · feedback channel</div>
  <h2>КВАССИСТЕНТ идёт в Telegram</h2>
  <p>Каркас бота уже входит в релиз. Токен не хранится в репозитории. После безопасного подключения бот будет отвечать: «Какой хороший квас ты задумал! Вот это молодец — ай да хорош!»</p>
  <a href="/telegram/">Открыть страницу Telegram →</a>
</section>
"""


def space_layer() -> str:
    orbit = '<div class="kvass-orbit"><span class="kvass-satellite"><i class="kvass-flame"></i></span></div>'
    orbits = "".join(orbit for _ in range(6))
    return f'<div class="kvass-space-layer" aria-hidden="true">{orbits}</div>'


def patch_landing(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "human-manifesto-release" in text:
        return
    text = text.replace("</style>", SPACE_CSS + "\n</style>", 1) if "</style>" in text else text.replace("</head>", f"<style>{SPACE_CSS}</style></head>", 1)
    text = text.replace("<body>", "<body>\n" + space_layer(), 1)
    marker = '<section class="globe-game-release"'
    if marker in text:
        text = text.replace(marker, manifesto_section() + "\n" + marker, 1)
    else:
        text = text.replace("<main>", "<main>\n" + manifesto_section(), 1)
    text = text.replace('<a href="/feedback/">Фидбек</a>', '<a href="/feedback/">Фидбек</a><a href="/telegram/">Telegram</a>')
    path.write_text(text, encoding="utf-8")


def telegram_page() -> str:
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KVASSISTENT Telegram · Version {ONES}</title>
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:radial-gradient(circle at 30% 20%,#263c77,#050812 65%);color:#f4f8ff;font:18px/1.55 system-ui}}main{{max-width:760px;margin:24px;padding:34px;border:1px solid #4da9e9;border-radius:28px;background:rgba(4,17,34,.9)}}a{{color:#7bd2ff}}code{{background:#071d30;padding:.2em .45em;border-radius:.4em}}.answer{{padding:18px;border-radius:16px;background:#0c3454;color:#fff}}</style></head>
<body><main><p>KVASSISTENT · Version {ONES}</p><h1>Telegram-бот подготовлен</h1><p>Код webhook-бота находится в <code>telegram-bot/</code>. Секретный токен в репозиторий не записывается.</p><p class="answer">Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤</p><p>После добавления токена и установки webhook здесь появится прямая ссылка на бота.</p><p><a href="/">← Вернуться к КВАССИСТЕНТУ</a> · <a href="https://github.com/bambuchastudent/kvas-ai-agent/tree/develop/telegram-bot">Код бота</a></p></main></body></html>"""


def write_telegram(root: Path) -> None:
    target = root / "telegram/index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(telegram_page(), encoding="utf-8")


version_root = SITE / f"v{VERSION}"
for landing in (version_root / "index.html", SITE / "index.html"):
    if not landing.is_file():
        raise RuntimeError(f"Missing landing page: {landing}")
    patch_landing(landing)

write_telegram(version_root)
write_telegram(SITE)
latest = SITE / "latest-version.json"
if latest.is_file():
    data = json.loads(latest.read_text(encoding="utf-8"))
    data["telegram"] = "/telegram/"
    latest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for required in ("human-manifesto-release", "kvass-space-layer", 'href="/telegram/"'):
    if required not in (SITE / "index.html").read_text(encoding="utf-8"):
        raise RuntimeError(f"Release enhancement missing: {required}")
print(f"enhanced KVASSISTENT version {ONES}: v{VERSION}")
