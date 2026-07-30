#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "scripts/build-publication-safe.py"
COMPANION = ROOT / "companion"
FEEDBACK = ROOT / "feedback"


def load_core():
    spec = importlib.util.spec_from_file_location("kvassistent_publication_core", CORE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {CORE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def configure_localized_document_metadata(core, version: str, ones_count: int) -> None:
    core.VERSION = version
    labels = {
        "ru": f"Версия {ones_count}. В ней {ones_count} единиц: v{version}",
        "en": f"Version {ones_count}. It contains {ones_count} ones: v{version}",
        "es": f"Versión {ones_count}. Contiene {ones_count} unos: v{version}",
        "de": f"Version {ones_count}. Sie enthält {ones_count} Einsen: v{version}",
        "zh-CN": f"第 {ones_count} 版，共有 {ones_count} 个 1：v{version}",
        "el": f"Έκδοση {ones_count}. Περιέχει {ones_count} μονάδες: v{version}",
    }

    def patch_document_pages(builder) -> None:
        original_page_html = builder.page_html

        def page_html(doc, language: dict[str, Any], manifest):
            result = original_page_html(doc, language, manifest)
            code = str(language["code"])
            result = result.replace("Kvas - Zhizha -", "KVASSISTENT ·")
            result = result.replace(
                f"Version {version} · Source of truth:",
                f"{labels.get(code, labels['en'])} · Source of truth:",
            )
            return result

        builder.page_html = page_html

    core.patch_document_pages = patch_document_pages


def install_comic(version: str) -> Path:
    source = ROOT / f"share/kvassistent-{version}-comic.svg"
    if not source.is_file():
        raise RuntimeError(f"Missing comic source: {source}")
    target = ROOT / f"dist/site/v{version}/assets/kvassistent-{version}-comic.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def install_companion(version: str) -> Path:
    required = (
        "index.html", "styles.css", "engine.js", "preferences.js", "app.js",
        "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js",
        "game/index.html", "game/styles.css", "game/i18n.css", "game/i18n.js", "game/game.js",
    )
    missing = [name for name in required if not (COMPANION / name).is_file()]
    if missing:
        raise RuntimeError(f"Missing companion/game assets: {missing}")
    target = ROOT / f"dist/site/v{version}/companion"
    shutil.copytree(COMPANION, target, dirs_exist_ok=True)
    return target


def install_feedback(version: str) -> Path:
    required = ("index.html", "styles.css", "thanks.html")
    missing = [name for name in required if not (FEEDBACK / name).is_file()]
    if missing:
        raise RuntimeError(f"Missing feedback assets: {missing}")
    target = ROOT / f"dist/site/v{version}/feedback"
    shutil.copytree(FEEDBACK, target, dirs_exist_ok=True)
    return target


def patch_landing(version: str, ones_count: int) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    people_marker = '<section class="people-quickstart" id="best-human-instructions">'
    audience_marker = '<section class="audience-section people" id="for-people">'
    if people_marker not in text or audience_marker not in text:
        raise RuntimeError("Cannot find landing page markers")

    immutable_path = f"/v{version}/"
    version_text = f"Версия {ones_count}"
    version_html = f'{version_text} · технический номер: <a class="version-link" href="{immutable_path}">v{version}</a>'
    comic_name = f"kvassistent-{version}-comic.svg"

    css = """
.site-topbar{position:sticky;top:0;z-index:40;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin:0 0 22px;padding:14px 18px;border:1px solid rgba(180,119,24,.2);border-radius:20px;background:rgba(255,251,241,.94);backdrop-filter:blur(14px);box-shadow:0 10px 30px rgba(52,31,8,.08)}
.topbar-brand{display:flex;flex-direction:column;gap:4px}.topbar-brand strong{color:#503107}.topbar-brand span{color:var(--muted);font-size:.92rem}.topbar-links,.header-links{display:flex;flex-wrap:wrap;gap:9px}.topbar-links a,.header-links a{padding:9px 13px;border:1px solid rgba(180,119,24,.2);border-radius:999px;background:#fff;color:#2c251b;text-decoration:none;font-weight:800}
.header-language{display:flex;flex-wrap:wrap;align-items:center;gap:9px}.header-language label{font-weight:900;color:#7a4c06}.header-language select{padding:10px 13px;border:1px solid rgba(180,119,24,.25);border-radius:999px;background:#fff;font:inherit}.header-language a{padding:10px 13px;border-radius:999px;background:#b47718;color:#fff;text-decoration:none;font-weight:850}.header-language a.secondary{background:#fff;color:#7a4c06;border:1px solid rgba(180,119,24,.25)}
.version-link{color:inherit;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}.version-banner{margin:16px 0;padding:15px 18px;border:1px solid rgba(255,255,255,.18);border-radius:16px;background:rgba(255,255,255,.07);color:#fff4ce;font-weight:850;overflow-wrap:anywhere}
.globe-game-release,.all-links-release,.companion-release,.localization-release,.comic-release{margin:30px 0;padding:clamp(24px,5vw,44px);border-radius:26px}.globe-game-release{position:relative;overflow:hidden;color:#eef5ff;border:2px solid #244b88;background:radial-gradient(circle at 30% 68%,rgba(38,117,213,.26),transparent 38%),linear-gradient(180deg,#0b1734,#040914)}.globe-game-release::before{content:"";position:absolute;inset:0;background-image:radial-gradient(circle,#fff 0 1px,transparent 1.4px);background-size:91px 91px;opacity:.22;pointer-events:none}.globe-game-release>*{position:relative}.globe-game-release .eyebrow{color:#ffdc7a}.globe-game-release h2{margin:10px 0;color:#fff8e8;font-size:clamp(38px,7vw,72px);line-height:.95}.globe-game-release p{max-width:780px;color:#becce6}.globe-preview{display:grid;grid-template-columns:minmax(250px,1fr) minmax(270px,1fr);gap:25px;align-items:center}.mini-globe{position:relative;width:min(100%,430px);aspect-ratio:1;margin:auto;border:2px solid rgba(186,230,255,.65);border-radius:50%;background:radial-gradient(circle at 30% 24%,#81d5ff 0 4%,#1e82d0 28%,#09569f 58%,#031c43 100%);box-shadow:inset -42px -20px 70px rgba(0,0,0,.58),0 0 48px rgba(62,154,255,.52);overflow:hidden}.mini-globe::before{content:"";position:absolute;inset:12%;background:#79b850;clip-path:polygon(4% 20%,18% 2%,34% 9%,42% 26%,34% 42%,27% 61%,18% 58%,10% 43%,0 39%,46% 25%,56% 9%,70% 12%,79% 27%,71% 38%,60% 39%,49% 30%,57% 45%,68% 43%,78% 55%,75% 77%,64% 92%,56% 70%,50% 52%,82% 18%,95% 10%,100% 28%,92% 47%,82% 52%,90% 67%,100% 74%,94% 88%,80% 91%,75% 75%,61% 66%)}.mini-globe::after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 27% 18%,rgba(255,255,255,.34),transparent 26%),radial-gradient(circle at 70% 75%,transparent 46%,rgba(0,0,0,.45) 82%)}.globe-dot{position:absolute;z-index:2;width:18px;height:18px;border-radius:50%;background:#f0bb45;box-shadow:0 0 0 5px rgba(240,187,69,.18),0 0 18px #f0bb45}.globe-dot:nth-child(1){left:24%;top:32%}.globe-dot:nth-child(2){left:35%;top:66%}.globe-dot:nth-child(3){left:51%;top:28%}.globe-dot:nth-child(4){left:54%;top:56%}.globe-dot:nth-child(5){left:73%;top:35%}.globe-dot:nth-child(6){left:79%;top:70%}.game-copy{display:grid;gap:12px}.game-copy article{padding:15px;border:1px solid rgba(255,255,255,.13);border-radius:16px;background:rgba(255,255,255,.045);color:#c6d3e9}.game-copy strong{display:block;color:#fff8e8}.game-cta{display:inline-flex;justify-content:center;padding:15px 22px;border-radius:999px;background:#f0bb45;color:#17110a;text-decoration:none;font-weight:950}
.all-links-release{border:2px solid #d7c39a;background:linear-gradient(135deg,#fffaf0,#fff)}.all-links-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-top:22px}.all-links-grid a{display:flex;min-height:82px;flex-direction:column;justify-content:center;padding:14px 16px;border:1px solid rgba(180,119,24,.18);border-radius:18px;background:#fff;color:#1f1811;text-decoration:none;box-shadow:0 10px 24px rgba(64,37,6,.06)}.all-links-grid span{color:var(--muted);font-size:.93rem}.stable-url{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}
.companion-release{color:#f6f0df;background:#17130d;border:1px solid #67522a}.companion-release h2{color:#fff8e8}.companion-release p{color:#c8bea8}.companion-release a{display:inline-flex;padding:13px 18px;border-radius:999px;background:#f0bb45;color:#17130d;text-decoration:none;font-weight:900}
.localization-release{border:2px solid #317054;background:linear-gradient(135deg,#effcf4,#fffdf7)}.localization-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:11px}.localization-grid article{padding:15px;border:1px solid #b8dcc7;border-radius:16px;background:#fff}.localization-grid strong{display:block;margin-bottom:5px}.localization-note{margin-top:16px;padding:14px;border-left:5px solid #317054;background:#fff}
.comic-release{border:2px solid #493a8a;background:#f6f3ff}.comic-release img{display:block;width:min(100%,900px);margin:20px auto 0;border:3px solid #2b244d;border-radius:18px}.comic-release figcaption{max-width:900px;margin:10px auto;color:var(--muted)}
@media(max-width:760px){.globe-preview{grid-template-columns:1fr}.site-topbar{justify-content:flex-start}.header-language,.topbar-links{width:100%}.header-language select{flex:1;min-width:160px}}
"""
    text = text.replace("</style>", css + "\n</style>", 1)

    topbar = """
<header class="site-topbar web-only" id="site-topbar">
  <div class="topbar-brand"><strong>КВАССИСТЕНТ</strong><span>Последняя версия и все основные входы</span></div>
  <nav class="topbar-links"><a href="/game/">Игра</a><a href="/companion/">Живая партия</a><a href="#all-links">Все ссылки</a><a href="#for-people">Для людей</a><a href="#for-ai-agents">Для ИИ</a><a href="/feedback/">Фидбек</a><a href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a></nav>
  <div class="header-language"><label for="header-language-select">Язык</label><select id="header-language-select"><option value="ru">Русский</option><option value="en">English</option><option value="es">Español</option><option value="de">Deutsch</option><option value="zh-CN">简体中文</option><option value="el">Ελληνικά</option></select><a id="header-human-link" href="/ru/summary/">Для людей</a><a class="secondary" id="header-agent-link" href="/ru/instructions/">Для ИИ</a></div>
</header>
"""
    text = text.replace("<main>", f"<main>\n{topbar}", 1)
    text = re.sub(r'<div class="eyebrow">.*?</div>', f'<div class="eyebrow">{version_html}</div>', text, count=1, flags=re.S)

    hero_nav = """
<nav class="hero-actions web-only" aria-label="Быстрые действия"><a class="button primary" href="/game/">Играть</a><a class="button" href="/companion/">Живая партия</a><a class="button" href="#all-links">Все ссылки</a><a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a></nav>
<div class="header-links web-only"><a href="/">Последняя версия</a><a href="/game/">/game/</a><a href="/companion/">/companion/</a><a href="/feedback/">/feedback/</a></div>
"""
    text = re.sub(r'<nav class="hero-actions web-only" aria-label="Быстрые действия">.*?</nav>', hero_nav, text, count=1, flags=re.S)

    game_section = f"""
<section class="globe-game-release" id="globe-game"><div class="eyebrow">Игра сразу наверху</div><h2>Глобальная игра на сфере</h2><p>Она выглядит плоской только потому, что экран пока не согласился стать шаром. Внутри — шесть континентов, ручные пуски, автозапуск каждые 10 секунд и локальный счётчик.</p><div class="globe-preview"><div class="mini-globe" aria-hidden="true"><span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span></div><div class="game-copy"><div class="version-banner">{version_html}</div><article><strong>Короткая актуальная ссылка</strong><span class="stable-url">kvassistent.pages.dev/game/</span></article><article><strong>Локализация</strong>Русский и английский — источники знаний; другие языки совпадают по правилам и используют английский fallback, а не русский.</article><article><strong>Газ и реальность</strong>Игра обещает максимум пузырьков. Реальный дрожжевой квас не может честно гарантировать 0,0% алкоголя.</article><a class="game-cta" href="/game/">ИГРАТЬ НА ГЛОБУСЕ →</a></div></div></section>
"""

    links_section = f"""
<section class="all-links-release" id="all-links"><div class="eyebrow">Короткие адреса всегда ведут на последнее</div><h2>Больше никаких обязательных километров из единиц</h2><p>Длинная ссылка остаётся неизменяемым адресом конкретного релиза. Для обычного использования теперь есть короткие постоянные адреса.</p><div class="all-links-grid"><a href="/"><strong>Главная</strong><span class="stable-url">kvassistent.pages.dev/</span></a><a href="/game/"><strong>Игра</strong><span class="stable-url">kvassistent.pages.dev/game/</span></a><a href="/companion/"><strong>Живая партия</strong><span class="stable-url">kvassistent.pages.dev/companion/</span></a><a href="/feedback/"><strong>Фидбек</strong><span class="stable-url">kvassistent.pages.dev/feedback/</span></a><a href="/ru/summary/"><strong>Русская инструкция</strong><span>Последняя локализация</span></a><a href="/en/summary/"><strong>English guide</strong><span>Latest localization</span></a><a href="{immutable_path}"><strong>Версия {ones_count}</strong><span class="stable-url">v{version}</span></a><a href="https://github.com/bambuchastudent/kvas-ai-agent"><strong>GitHub</strong><span>Код и история релизов</span></a></div></section>
"""
    text = text.replace(people_marker, game_section + "\n" + links_section + "\n" + people_marker, 1)

    lower = f"""
<section class="companion-release" id="live-batch"><div class="eyebrow">Реальный процесс отдельно от игры</div><h2>Живая партия</h2><p>Пошаговый локальный помощник хранит состояние партии на устройстве, проверяет температуру, солнце, запах, поверхность и давление.</p><a href="/companion/">Открыть короткий адрес /companion/ →</a></section>
<section class="localization-release" id="localization"><div class="eyebrow">Локализации сопоставлены</div><h2>Одинаковые знания, числа, риски и ссылки</h2><div class="localization-grid"><article><strong>Русский</strong>Канонический источник знаний.</article><article><strong>English</strong>Canonical knowledge source and universal fallback.</article><article><strong>Español</strong>Misma estructura y seguridad.</article><article><strong>Deutsch</strong>Gleiche Struktur und Sicherheitsregeln.</article><article><strong>简体中文</strong>相同的步骤、数量和安全规则。</article><article><strong>Ελληνικά</strong>Ίδια βήματα, ποσότητες και ασφάλεια.</article></div><div class="localization-note"><strong>Правило fallback:</strong> в нерусских интерфейсах недостающая строка может временно остаться английской или быть записана местным письмом, но не должна заменяться русским текстом.</div></section>
<section class="comic-release" id="comic-guide"><div class="eyebrow">Версия {ones_count} · визуальное резюме</div><h2>Последняя версия, короткие ссылки и переводы</h2><figure><a href="/assets/{comic_name}"><img src="/assets/{comic_name}" alt="КВАССИСТЕНТ {ones_count}: короткие ссылки и согласованная локализация" loading="lazy"></a><figcaption>Неизменяемый релиз: <a href="{immutable_path}">v{version}</a>. Обычная актуальная ссылка: <a href="/">kvassistent.pages.dev/</a>.</figcaption></figure></section>
"""
    text = text.replace(audience_marker, lower + "\n" + audience_marker, 1)

    script = """
<script>
(() => {
  const routes={ru:{human:'/ru/summary/',agent:'/ru/instructions/'},en:{human:'/en/summary/',agent:'/en/instructions/'},es:{human:'/es/summary/',agent:'/es/instructions/'},de:{human:'/de/summary/',agent:'/de/instructions/'},'zh-CN':{human:'/zh-CN/summary/',agent:'/zh-CN/instructions/'},el:{human:'/el/summary/',agent:'/el/instructions/'}};
  const select=document.getElementById('header-language-select');const human=document.getElementById('header-human-link');const agent=document.getElementById('header-agent-link');if(!select||!human||!agent)return;
  const stored=localStorage.getItem('kvassistent-landing-lang');if(stored&&routes[stored])select.value=stored;
  const apply=()=>{const current=routes[select.value]||routes.en;human.href=current.human;agent.href=current.agent;localStorage.setItem('kvassistent-landing-lang',select.value)};select.addEventListener('change',apply);apply();
})();
</script>
"""
    text = text.replace("</body>", script + "\n</body>", 1)
    text = text.replace("https://github.com/bambuchastudent/kvas-ai-agent/issues/new", "https://t.me/kvassistent_bot")
    landing.write_text(text, encoding="utf-8")


def section_markers(path: Path) -> list[str]:
    return re.findall(r"<!-- section:([a-z0-9_-]+) -->", path.read_text(encoding="utf-8"))


def verify_localizations(manifest: dict[str, Any]) -> None:
    by_code = {item["code"]: item for item in manifest["languages"]}
    for doc_type in ("summary", "instructions"):
        canonical = section_markers(ROOT / by_code["ru"][doc_type])
        english = section_markers(ROOT / by_code["en"][doc_type])
        if canonical != english:
            raise RuntimeError(f"RU/EN section mismatch for {doc_type}: {canonical} != {english}")
        for code, language in by_code.items():
            path = ROOT / language[doc_type]
            if section_markers(path) != canonical:
                raise RuntimeError(f"Localization section mismatch: {path}")
            content = path.read_text(encoding="utf-8")
            if code != "ru" and re.search(r"[А-Яа-яЁё]", content):
                raise RuntimeError(f"Russian text leaked into {code}: {path}")
            for token in ("180–220", "100–120", "25–35", "28°C", "2,2–2,6" if code != "en" else "2.2–2.6"):
                if token not in content:
                    raise RuntimeError(f"Localization lost canonical quantity {token}: {path}")


def publish_latest_aliases(version: str) -> None:
    site = ROOT / "dist/site"
    source = site / f"v{version}"
    for item in source.iterdir():
        target = site / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    shutil.copytree(site / "companion/game", site / "game", dirs_exist_ok=True)
    root_index = site / "index.html"
    text = root_index.read_text(encoding="utf-8")
    text = text.replace(f"https://kvassistent.pages.dev/v{version}/", "https://kvassistent.pages.dev/")
    root_index.write_text(text, encoding="utf-8")
    (site / "latest-version.json").write_text(
        json.dumps({"version": version, "home": "/", "game": "/game/", "companion": "/companion/", "immutable": f"/v{version}/"}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def verify(version: str, ones_count: int) -> None:
    site = ROOT / "dist/site"
    version_root = site / f"v{version}"
    landing = version_root / "index.html"
    text = landing.read_text(encoding="utf-8")
    required = [
        f"Версия {ones_count}",
        f'href="/v{version}/"',
        f">v{version}</a>", 'href="/game/"', 'href="/companion/"', 'href="/feedback/"',
        'id="header-language-select"', 'id="globe-game"', 'id="all-links"', 'id="localization"',
    ]
    missing = [value for value in required if value not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release {ones_count} content: {missing}")

    game_dir = version_root / "companion/game"
    game_html = (game_dir / "index.html").read_text(encoding="utf-8")
    game_js = (game_dir / "game.js").read_text(encoding="utf-8")
    game_i18n = (game_dir / "i18n.js").read_text(encoding="utf-8")
    if game_html.count('class="site"') != 6 or f"VERSION {ones_count}" not in game_html:
        raise RuntimeError("Globe game release or launch sites are incorrect")
    for code in ("ru", "en", "es", "de", "zh-CN", "el"):
        if code not in game_i18n:
            raise RuntimeError(f"Game localization missing: {code}")
    if "localStorage" not in game_js or "setInterval" not in game_js or "resolveGameLanguage" not in game_js:
        raise RuntimeError("Game misses persistence, automatic launches, or localization")

    companion_html = (version_root / "companion/index.html").read_text(encoding="utf-8")
    if re.search(r"[А-Яа-яЁё]", companion_html):
        raise RuntimeError("Russian static fallback leaked into the universal companion shell")
    if "consent-card" not in companion_html or 'option value="el"' not in companion_html:
        raise RuntimeError("Companion privacy or language controls are missing")

    manifest = json.loads((ROOT / "publication/manifest.json").read_text(encoding="utf-8"))
    verify_localizations(manifest)

    for path in (
        site / "index.html", site / "game/index.html", site / "companion/index.html", site / "feedback/index.html",
        site / "ru/summary/index.html", site / "en/summary/index.html", site / f"v{version}/index.html",
    ):
        if not path.is_file() or path.stat().st_size < 500:
            raise RuntimeError(f"Latest alias is missing or empty: {path}")


def main() -> None:
    meta = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
    version = str(meta["current"])
    ones_count = int(meta["ones_count"])
    core = load_core()
    configure_localized_document_metadata(core, version, ones_count)
    core.main()
    install_comic(version)
    install_companion(version)
    install_feedback(version)
    patch_landing(version, ones_count)
    publish_latest_aliases(version)
    verify(version, ones_count)
    print(f"Built KVASSISTENT release {ones_count}: v{version}; latest URLs: /, /game/, /companion/, /feedback/")


if __name__ == "__main__":
    main()
