#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

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
        "game/index.html", "game/styles.css", "game/game.js",
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
        raise RuntimeError("Cannot find landing page markers for release sections")

    version_phrase = f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}"
    comic_name = f"kvassistent-{version}-comic.svg"

    css = """
.site-topbar{position:sticky;top:0;z-index:40;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin:0 0 22px;padding:14px 18px;border:1px solid rgba(180,119,24,.18);border-radius:20px;background:rgba(255,251,241,.92);backdrop-filter:blur(14px);box-shadow:0 10px 30px rgba(52,31,8,.08)}
.topbar-brand{display:flex;flex-direction:column;gap:4px}.topbar-brand strong{font-size:1.08rem;color:#503107}.topbar-brand span{color:var(--muted);font-size:.95rem}
.topbar-links,.header-quick-links{display:flex;flex-wrap:wrap;gap:10px;align-items:center}.topbar-links a,.header-quick-links a{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;background:#fff;color:#2c251b;text-decoration:none;font-weight:780;border:1px solid rgba(180,119,24,.18)}
.topbar-links a:hover,.header-quick-links a:hover,.hero-actions .button:hover,.all-links-grid a:hover,.game-cta:hover{transform:translateY(-1px);filter:brightness(1.03)}
.header-language{display:flex;flex-wrap:wrap;align-items:center;gap:10px}.header-language label{font-weight:800;color:#7a4c06}.header-language select{padding:11px 14px;border-radius:999px;border:1px solid rgba(180,119,24,.24);background:#fff;font:inherit;color:#2c251b;min-width:170px}.header-language .lang-link{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;text-decoration:none;font-weight:800;background:#b47718;color:#fff8eb}.header-language .lang-link.secondary{background:#fff;color:#7a4c06;border:1px solid rgba(180,119,24,.22)}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px}.hero-actions .button{display:inline-flex;align-items:center;justify-content:center}
.top-links-release,.companion-release,.community-release,.heat-release,.globe-game-release,.comic-release{margin:30px 0;padding:clamp(24px,5vw,44px);border-radius:24px}
.top-links-release{border:2px solid #d7c39a;background:linear-gradient(135deg,#fffaf0,#fff)}.top-links-release h2{margin:10px 0 8px;font-size:clamp(30px,5vw,48px)}.top-links-release p{max-width:760px}.all-links-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:22px}.all-links-grid a{display:flex;min-height:78px;flex-direction:column;justify-content:center;gap:4px;padding:14px 16px;border-radius:18px;background:#fff;text-decoration:none;color:#1f1811;border:1px solid rgba(180,119,24,.18);box-shadow:0 10px 24px rgba(64,37,6,.06)}.all-links-grid strong{font-size:1rem}.all-links-grid span{color:var(--muted);font-size:.94rem}
.globe-game-release{position:relative;overflow:hidden;color:#eef5ff;border:2px solid #244b88;background:radial-gradient(circle at 50% 72%,rgba(38,117,213,.22),transparent 38%),linear-gradient(180deg,#0b1734,#040914)}.globe-game-release::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle,#fff 0 1px,transparent 1.4px);background-size:91px 91px;opacity:.26}.globe-game-release>*{position:relative}.globe-game-release .eyebrow{color:#ffdc7a}.globe-game-release h2{max-width:880px;margin:10px 0;color:#fff8e8;font-size:clamp(38px,7vw,72px);line-height:.94}.globe-game-release p{max-width:780px;color:#becce6}.globe-preview{display:grid;grid-template-columns:minmax(240px,1fr) minmax(260px,1fr);gap:24px;align-items:center;margin-top:24px}.mini-globe{position:relative;width:min(100%,430px);aspect-ratio:1;margin:auto;border-radius:50%;background:radial-gradient(circle at 30% 24%,#81d5ff 0 4%,#1e82d0 28%,#09569f 58%,#031c43 100%);box-shadow:inset -42px -20px 70px rgba(0,0,0,.58),0 0 48px rgba(62,154,255,.52);border:2px solid rgba(186,230,255,.65);overflow:hidden}.mini-globe::before{content:"";position:absolute;inset:12% 12% 18% 7%;background:#74ad4c;clip-path:polygon(4% 20%,18% 2%,34% 9%,42% 26%,34% 42%,27% 61%,18% 58%,10% 43%,0 39%,46% 25%,56% 9%,70% 12%,79% 27%,71% 38%,60% 39%,49% 30%,57% 45%,68% 43%,78% 55%,75% 77%,64% 92%,56% 70%,50% 52%,82% 18%,95% 10%,100% 28%,92% 47%,82% 52%,90% 67%,100% 74%,94% 88%,80% 91%,75% 75%,61% 66%)}.mini-globe::after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 27% 18%,rgba(255,255,255,.34),transparent 26%),radial-gradient(circle at 70% 75%,transparent 46%,rgba(0,0,0,.45) 82%)}.globe-dot{position:absolute;z-index:2;width:18px;height:18px;border-radius:50%;background:#f0bb45;box-shadow:0 0 0 5px rgba(240,187,69,.18),0 0 18px #f0bb45}.globe-dot:nth-child(1){left:24%;top:32%}.globe-dot:nth-child(2){left:35%;top:66%}.globe-dot:nth-child(3){left:51%;top:28%}.globe-dot:nth-child(4){left:54%;top:56%}.globe-dot:nth-child(5){left:73%;top:35%}.globe-dot:nth-child(6){left:79%;top:70%}.game-copy{display:grid;gap:12px}.game-copy article{padding:15px;border:1px solid rgba(255,255,255,.13);border-radius:16px;background:rgba(255,255,255,.045);color:#c6d3e9}.game-copy strong{display:block;margin-bottom:4px;color:#fff8e8}.game-cta{display:inline-flex;justify-content:center;align-items:center;margin-top:8px;padding:15px 22px;border-radius:999px;background:#f0bb45;color:#17110a;text-decoration:none;font-weight:950;letter-spacing:.03em}
.companion-release{color:#f6f0df;background:radial-gradient(circle at 90% 5%,rgba(240,187,69,.2),transparent 36%),#17130d;border:1px solid #67522a}.companion-release .eyebrow{color:#f0bb45}.companion-release h2{max-width:780px;margin:14px 0;color:#fff8e8;font-size:clamp(34px,6vw,64px);line-height:.98}.companion-release p{max-width:720px;color:#c8bea8}.companion-benefits{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:26px 0}.companion-benefits article{padding:16px;border:1px solid #433a2c;border-radius:14px;background:rgba(255,255,255,.035);color:#c8bea8}.companion-benefits strong{display:block;margin-bottom:5px;color:#fff8e8}.companion-actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center}.companion-cta{display:inline-flex;align-items:center;gap:18px;padding:15px 20px;border-radius:999px;color:#17130d;background:#f0bb45;text-decoration:none;font-weight:850}.companion-secondary{color:#f0bb45;font-weight:750}
.community-release{border:2px solid #317054;background:linear-gradient(135deg,#effcf4,#fffdf7)}.community-release h2{max-width:760px;margin:10px 0;font-size:clamp(34px,6vw,60px);line-height:1}.community-release p{max-width:720px}.community-actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:22px}.community-social{color:#22573f;font-weight:800;text-decoration:none}
.heat-release{border:2px solid #d48a18;background:#fff5dc}.heat-release h2,.comic-release h2{margin-top:0}.heat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.heat-grid article{padding:14px;border-radius:12px;background:#fffdf7;border:1px solid #e7c98d}.heat-danger{margin-top:15px;padding:14px;border-left:5px solid #a52b20;background:#fff0ea}
.comic-release{border:2px solid #493a8a;background:#f6f3ff}.comic-release figure{margin:22px 0 0}.comic-release img{display:block;width:min(100%,860px);height:auto;margin:0 auto;border:3px solid #2b244d;border-radius:18px;background:#f8efd7;box-shadow:0 20px 55px rgba(43,36,77,.18)}.comic-release figcaption{max-width:860px;margin:12px auto 0;color:var(--muted)}
@media(max-width:900px){.site-topbar{padding:14px}.site-topbar,.header-language{justify-content:flex-start}}
@media(max-width:720px){.globe-preview{grid-template-columns:1fr}.mini-globe{width:min(88vw,400px)}.topbar-links,.header-quick-links{width:100%}.header-language{width:100%}.header-language select{width:100%}}
"""
    if "</style>" not in text:
        raise RuntimeError("Cannot inject landing CSS")
    text = text.replace("</style>", css + "\n</style>", 1)

    topbar = """
<header class="site-topbar web-only" id="site-topbar" aria-label="Главная навигация">
  <div class="topbar-brand">
    <strong>КВАССИСТЕНТ</strong>
    <span>Всё нужное по квасу и игре — сразу сверху</span>
  </div>
  <nav class="topbar-links" aria-label="Быстрые ссылки">
    <a href="#globe-game">Игра</a>
    <a href="#all-links">Все ссылки</a>
    <a href="#for-people">Для людей</a>
    <a href="#for-ai-agents">Для ИИ</a>
    <a href="companion/">Живая партия</a>
    <a href="feedback/">Фидбек</a>
    <a href="#gallery">Галерея</a>
    <a href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a>
  </nav>
  <div class="header-language" aria-label="Выбор языка">
    <label for="header-language-select">Язык</label>
    <select id="header-language-select">
      <option value="ru">Русский</option>
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="de">Deutsch</option>
      <option value="zh-CN">简体中文</option>
      <option value="el">Ελληνικά</option>
    </select>
    <a class="lang-link" id="header-human-link" href="ru/summary/">Для людей</a>
    <a class="lang-link secondary" id="header-agent-link" href="ru/instructions/">Для ИИ</a>
  </div>
</header>
"""
    text = text.replace("<main>", f"<main>\n{topbar}", 1)

    text = re.sub(r'<div class="eyebrow">.*?</div>', f'<div class="eyebrow">{version_phrase}</div>', text, count=1, flags=re.S)

    hero_nav = """
<nav class="hero-actions web-only" aria-label="Быстрые действия">
  <a class="button primary" href="#globe-game">Игру наверх</a>
  <a class="button" href="#all-links">Все ссылки</a>
  <a class="button" href="#for-people">Для людей</a>
  <a class="button" href="#for-ai-agents">Инструкция ИИ-агенту</a>
  <a class="button" href="https://github.com/bambuchastudent/kvas-ai-agent">GitHub</a>
</nav>
<div class="header-quick-links web-only" aria-label="Прямые ссылки">
  <a href="companion/game/">Играть на глобусе</a>
  <a href="companion/">Живая партия</a>
  <a href="feedback/">Фидбек</a>
  <a href="#gallery">Галерея напитков</a>
</div>
"""
    text = re.sub(r'<nav class="hero-actions web-only" aria-label="Быстрые действия">.*?</nav>', hero_nav.strip(), text, count=1, flags=re.S)

    globe_section = f"""
<section class="globe-game-release" id="globe-game">
  <div class="eyebrow">Игра теперь сразу наверху</div>
  <h2>Глобус вместо плоской карты</h2>
  <p>Главная страница сразу показывает игру: сфера, шесть точек запуска, локальное накопление и автопуск каждые 10 секунд. Больше не нужно искать игру ниже по странице.</p>
  <div class="globe-preview">
    <div class="mini-globe" aria-hidden="true">
      <span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span>
      <span class="globe-dot"></span><span class="globe-dot"></span><span class="globe-dot"></span>
    </div>
    <div class="game-copy">
      <article><strong>{version_phrase}</strong>Новое описание версии теперь видно сразу в главном блоке.</article>
      <article><strong>Автопуск: 10 секунд</strong>Глобус сам запускает бутылки-ракеты по кругу, а ручной запуск тоже остаётся.</article>
      <article><strong>Локальное накопление</strong>Счётчики сохраняются на устройстве и продолжаются после перезагрузки страницы.</article>
      <article><strong>6 точек на сфере</strong>Северная Америка, Южная Америка, Европа, Африка, Азия и Океания.</article>
      <a class="game-cta" href="companion/game/">ИГРАТЬ НА ГЛОБУСЕ →</a>
    </div>
  </div>
</section>
"""

    all_links_section = f"""
<section class="top-links-release" id="all-links">
  <div class="eyebrow">Все ссылки сразу</div>
  <h2>Всё нужное — в одном месте</h2>
  <p>На главной странице теперь отдельный блок со ссылками на все основные точки входа: игру, живую партию, инструкции для людей, инструкции для ИИ, обратную связь, галерею и репозиторий.</p>
  <div class="all-links-grid">
    <a href="companion/game/"><strong>Игра на глобусе</strong><span>Сфера, запуски и счётчики</span></a>
    <a href="companion/"><strong>Живая партия</strong><span>Пошаговый PWA-компаньон</span></a>
    <a href="#for-people"><strong>Для людей</strong><span>Краткие рецепты по языкам</span></a>
    <a href="#for-ai-agents"><strong>Для ИИ</strong><span>Состояние партии и schema</span></a>
    <a href="feedback/"><strong>Фидбек</strong><span>Фото, баги, идеи и рецепты</span></a>
    <a href="#gallery"><strong>Галерея</strong><span>Проверенные реальные напитки</span></a>
    <a href="https://github.com/bambuchastudent/kvas-ai-agent"><strong>GitHub</strong><span>Код и релизы проекта</span></a>
    <a href="assets/{comic_name}"><strong>Постер версии</strong><span>SVG-комикс текущего релиза</span></a>
  </div>
</section>
"""

    text = text.replace(people_marker, globe_section + "\n" + all_links_section + "\n" + people_marker, 1)

    lower_sections = f"""
<section class="companion-release" id="live-batch">
  <div class="eyebrow">PWA-компаньон</div>
  <h2>Один ИИ-агент — одна понятная партия кваса</h2>
  <p>Если нужна не игра, а реальное ведение домашней партии, открывай «Живую партию»: там шаги, проверки, таймеры, предупреждения и локальное сохранение состояния.</p>
  <div class="companion-benefits">
    <article><strong>Простой рецепт</strong>Чёткие действия без гадания.</article>
    <article><strong>Проверки безопасности</strong>Температура, солнце, запах, герметичность и срок.</article>
    <article><strong>Локальная память</strong>История партии остаётся у пользователя.</article>
  </div>
  <div class="companion-actions"><a class="companion-cta" href="companion/">Открыть «Живую партию»</a><a class="companion-secondary" href="#for-people">Сразу к языковым карточкам ↓</a></div>
</section>
<section class="community-release" id="community-feedback">
  <div class="eyebrow">Сообщество</div>
  <h2>Отправь рецепт, баг или историю своей «Жижи»</h2>
  <p>На сайте есть отдельная страница обратной связи. Можно прислать фото напитка, заметки о вкусе, идеи по функциональности или сообщение об ошибке.</p>
  <div class="community-actions"><a class="button primary" href="feedback/">Открыть форму</a><a class="community-social" href="mailto:kvassitent@gmail.com">kvassitent@gmail.com</a><a class="community-social" href="https://instagram.com/kvassistent">Instagram</a><a class="community-social" href="https://tiktok.com/@kvassistent">TikTok</a></div>
</section>
<section class="heat-release" id="hot-fermentation">
  <div class="eyebrow">Безопасность в жару</div>
  <h2>Квас и жара: быстрый ориентир</h2>
  <div class="heat-grid">
    <article><strong>6–12 часов</strong><br>Нормальное окно старта активного брожения в тепле.</article>
    <article><strong>Проверка раньше</strong><br>При 28°C и выше смотреть уже через 6 часов.</article>
    <article><strong>Газ набрался — в холод</strong><br>Как только ПЭТ стал упругим, сразу охлаждать.</article>
  </div>
  <div class="heat-danger">Не держи реальный напиток долго в тёплой герметичной таре ради «максимума». Для версии с газиками смысл в коротком наборе давления и быстром охлаждении.</div>
</section>
<section class="comic-release" id="comic-guide">
  <div class="eyebrow">{version_phrase} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>Текущий релиз объединяет игру на глобусе, верхнюю навигацию, выбор языка в шапке и блок со всеми ссылками на одном экране.</p>
  <figure><a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="КВАССИСТЕНТ {ones_count}: глобус, ссылки и выбор языка" loading="lazy"></a><figcaption>Векторный постер текущей версии и отдельная интерактивная игра доступны прямо на сайте.</figcaption></figure>
</section>
"""
    text = text.replace(audience_marker, lower_sections + "\n" + audience_marker, 1)

    landing_script = """
<script>
(() => {
  const routes = {
    ru: { human: 'ru/summary/', agent: 'ru/instructions/' },
    en: { human: 'en/summary/', agent: 'en/instructions/' },
    es: { human: 'es/summary/', agent: 'es/instructions/' },
    de: { human: 'de/summary/', agent: 'de/instructions/' },
    'zh-CN': { human: 'zh-CN/summary/', agent: 'zh-CN/instructions/' },
    el: { human: 'el/summary/', agent: 'el/instructions/' },
  };
  const select = document.getElementById('header-language-select');
  const human = document.getElementById('header-human-link');
  const agent = document.getElementById('header-agent-link');
  if (!select || !human || !agent) return;
  const preferred = localStorage.getItem('kvassistent-landing-lang');
  if (preferred && routes[preferred]) select.value = preferred;
  const apply = () => {
    const current = routes[select.value] || routes.ru;
    human.href = current.human;
    agent.href = current.agent;
    localStorage.setItem('kvassistent-landing-lang', select.value);
  };
  select.addEventListener('change', apply);
  apply();
})();
</script>
"""
    text = text.replace("</body>", landing_script + "\n</body>", 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str, ones_count: int) -> None:
    root = ROOT / f"dist/site/v{version}"
    landing = root / "index.html"
    comic = root / f"assets/kvassistent-{version}-comic.svg"
    companion = root / "companion"
    game = companion / "game/index.html"
    feedback = root / "feedback"
    text = landing.read_text(encoding="utf-8")
    version_phrase = f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}"
    required = [
        'id="site-topbar"', 'id="header-language-select"', 'id="header-human-link"', 'id="header-agent-link"',
        'id="globe-game"', 'href="companion/game/"', 'id="all-links"', 'href="companion/"',
        'id="live-batch"', 'id="community-feedback"', 'href="feedback/"', 'id="hot-fermentation"',
        'id="comic-guide"', f"kvassistent-{version}-comic.svg", version_phrase,
        'href="#for-people"', 'href="#for-ai-agents"', 'href="#gallery"', 'kvassistent-landing-lang',
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")
    if not game.is_file() or game.stat().st_size < 4000:
        raise RuntimeError(f"Globe game is missing or too small: {game}")
    game_text = game.read_text(encoding="utf-8")
    game_required = [f"КВАССИСТЕНТ {ones_count}", f"ВЕРСИЯ {ones_count}", "10 сек", "Сфера, а не плоская карта"]
    missing_game = [item for item in game_required if item not in game_text]
    if missing_game:
        raise RuntimeError(f"Globe game misses required mechanics: {missing_game}")
    if game_text.count('class="site"') != 6:
        raise RuntimeError("Globe game must expose exactly six launch sites")
    game_js = (companion / "game/game.js").read_text(encoding="utf-8")
    if "localStorage" not in game_js or "setInterval" not in game_js:
        raise RuntimeError("Globe game misses local accumulation or timed launches")

    required_companion = ("index.html", "styles.css", "engine.js", "preferences.js", "app.js", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js")
    missing_companion = [name for name in required_companion if not (companion / name).is_file()]
    if missing_companion:
        raise RuntimeError(f"Companion assets were not copied: {missing_companion}")
    required_feedback = ("index.html", "styles.css", "thanks.html")
    missing_feedback = [name for name in required_feedback if not (feedback / name).is_file()]
    if missing_feedback:
        raise RuntimeError(f"Feedback assets were not copied: {missing_feedback}")

    feedback_text = (feedback / "index.html").read_text(encoding="utf-8")
    if "formsubmit.co/kvassitent@gmail.com" not in feedback_text:
        raise RuntimeError("Feedback page misses email delivery")
    companion_text = (companion / "index.html").read_text(encoding="utf-8")
    if "Живая партия" not in companion_text or "Простой квас без догадок" not in companion_text:
        raise RuntimeError("Companion entry point misses required titles")
    if "consent-card" not in companion_text or 'data-consent="essential"' not in companion_text:
        raise RuntimeError("Companion entry point misses privacy controls")
    if 'option value="el"' not in companion_text or 'id="nearby-kvass"' not in companion_text:
        raise RuntimeError("Companion entry point misses Greek or nearby discovery")
    service_worker = (companion / "sw.js").read_text(encoding="utf-8")
    if "kvassistent-live-v10" not in service_worker or "self.skipWaiting()" not in service_worker:
        raise RuntimeError("Companion service worker is not release-safe")

    manifest = json.loads((ROOT / "publication/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("visual_guide") != f"share/kvassistent-{version}-comic.svg":
        raise RuntimeError("Manifest visual_guide does not match current release")
    for language in manifest["languages"]:
        for key in ("summary", "instructions"):
            source = (ROOT / language[key]).read_text(encoding="utf-8")
            if "<!-- section:heat -->" not in source or "<!-- section:alcohol -->" not in source:
                raise RuntimeError(f"Missing heat/alcohol sections: {language[key]}")


def main() -> None:
    meta = json.loads((ROOT / "release/version.json").read_text(encoding="utf-8"))
    version = str(meta["current"])
    ones_count = int(meta["ones_count"])
    core = load_core()
    core.main()
    install_comic(version)
    install_companion(version)
    install_feedback(version)
    patch_landing(version, ones_count)
    verify(version, ones_count)
    print(f"Built КВАССИСТЕНТ {version} with landing-first globe game, top header language switcher, and full-link navigation")


if __name__ == "__main__":
    main()
