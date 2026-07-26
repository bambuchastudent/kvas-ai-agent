#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
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
    required = ("index.html", "styles.css", "engine.js", "preferences.js", "app.js", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js")
    missing = [name for name in required if not (COMPANION / name).is_file()]
    if missing:
        raise RuntimeError(f"Missing live-batch companion assets: {missing}")
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


def patch_landing(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    marker = '<section class="audience-section people" id="for-people">'
    if marker not in text:
        raise RuntimeError("Cannot find human section marker in landing page")

    css = """
.heat-release,
.comic-release,
.rocket-launch-release,
.zero-alcohol-release { margin: 30px 0; padding: 26px; border-radius: 18px; }
.heat-release { border: 2px solid #d48a18; background: #fff5dc; }
.comic-release { border: 2px solid #493a8a; background: #f6f3ff; }
.rocket-launch-release { border: 2px solid #20315f; background: linear-gradient(180deg,#edf5ff,#f8fbff); }
.zero-alcohol-release { border: 2px solid #20705b; background: linear-gradient(135deg,#eefcf7,#fffdf8); }
.heat-release h2,
.comic-release h2,
.rocket-launch-release h2,
.zero-alcohol-release h2 { margin-top: 0; }
.heat-grid,
.zero-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 12px; }
.heat-grid article,
.zero-grid article { padding: 14px; border-radius: 12px; background: #fffdf7; border: 1px solid #e7c98d; }
.zero-grid article { border-color: #9fd4be; background: rgba(255,255,255,.76); }
.heat-danger { margin-top: 15px; padding: 14px; border-left: 5px solid #a52b20; background: #fff0ea; }
.zero-note { margin-top: 16px; padding: 14px; border-left: 5px solid #20705b; background: #e8fbf3; }
.comic-release figure { margin: 22px 0 0; }
.comic-release img { display: block; width: min(100%, 860px); height: auto; margin: 0 auto; border: 3px solid #2b244d; border-radius: 18px; background: #f8efd7; box-shadow: 0 20px 55px rgba(43,36,77,.18); }
.comic-release figcaption { max-width: 860px; margin: 12px auto 0; color: var(--muted); }
.companion-release { margin: 30px 0; padding: clamp(26px,5vw,46px); border-radius: 24px; color: #f6f0df; background: radial-gradient(circle at 90% 5%,rgba(240,187,69,.2),transparent 36%),#17130d; border: 1px solid #67522a; overflow: hidden; }
.companion-release .eyebrow { color: #f0bb45; }
.companion-release h2 { max-width: 780px; margin: 14px 0; color: #fff8e8; font-size: clamp(34px,6vw,64px); line-height: .98; }
.companion-release p { max-width: 720px; color: #c8bea8; }
.companion-benefits { display: grid; grid-template-columns: repeat(auto-fit,minmax(170px,1fr)); gap: 10px; margin: 26px 0; }
.companion-benefits article { padding: 16px; border: 1px solid #433a2c; border-radius: 14px; background: rgba(255,255,255,.035); color: #c8bea8; }
.companion-benefits strong { display: block; margin-bottom: 5px; color: #fff8e8; }
.companion-cta { display: inline-flex; align-items: center; gap: 18px; margin-top: 4px; padding: 15px 20px; border-radius: 999px; color: #17130d; background: #f0bb45; text-decoration: none; font-weight: 850; }
.companion-cta:hover { filter: brightness(1.06); transform: translateY(-1px); }
.companion-actions { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.companion-secondary { color: #f0bb45; font-weight: 750; }
.community-release { margin: 30px 0; padding: clamp(26px,5vw,44px); border-radius: 24px; border: 2px solid #317054; background: linear-gradient(135deg,#effcf4,#fffdf7); }
.community-release h2 { max-width: 760px; margin: 10px 0; font-size: clamp(34px,6vw,60px); line-height: 1; }
.community-release p { max-width: 720px; }
.community-actions { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-top: 22px; }
.community-social { color: #22573f; font-weight: 800; text-decoration: none; }
.launch-world { position: relative; min-height: 720px; margin-top: 20px; border-radius: 24px; overflow: hidden; border: 1px solid rgba(32,49,95,.18); background: radial-gradient(circle at 15% 16%,rgba(255,255,255,.95),transparent 1.2%),radial-gradient(circle at 88% 22%,rgba(255,255,255,.8),transparent 1.6%),linear-gradient(180deg,#122047 0,#0a1328 66%,#233148 66%,#1a2432 100%); }
.launch-counter { position: absolute; top: 16px; right: 16px; z-index: 30; padding: 10px 14px; border-radius: 16px; background: rgba(7,12,23,.84); color: #fff8e8; border: 1px solid rgba(240,187,69,.65); font-weight: 800; font-size: .95rem; }
.launch-counter strong { color: #f0bb45; font-size: 1.1rem; }
.launch-status { position: absolute; top: 16px; left: 16px; z-index: 30; padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,.12); color: #e8f0ff; border: 1px solid rgba(255,255,255,.24); font-weight: 750; }
.global-note { position: absolute; top: 72px; right: 16px; z-index: 30; padding: 8px 12px; border-radius: 12px; background: rgba(255,255,255,.08); color: #d8e4ff; font-size: .92rem; }
.continent-launch { position: absolute; width: 158px; height: 168px; border: 1px solid rgba(255,255,255,.12); border-radius: 18px; background: rgba(255,255,255,.05); padding: 8px; }
.continent-launch h3 { margin: 0 0 6px; color: #fff8e8; font-size: 1rem; }
.continent-launch small { display: block; color: #b8c9f0; margin-bottom: 8px; }
.continent-launch[data-continent="north-america"] { left: 4%; top: 20%; }
.continent-launch[data-continent="south-america"] { left: 12%; top: 49%; }
.continent-launch[data-continent="europe"] { left: 41%; top: 19%; }
.continent-launch[data-continent="africa"] { left: 43%; top: 48%; }
.continent-launch[data-continent="asia"] { right: 16%; top: 22%; }
.continent-launch[data-continent="oceania"] { right: 8%; top: 53%; }
.continent-launch.local-accumulated { box-shadow: 0 0 0 2px rgba(240,187,69,.35), 0 16px 28px rgba(0,0,0,.25); }
.continent-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; border-radius: 999px; background: rgba(255,255,255,.08); color: #fff8e8; font-size: .78rem; }
.rocket-bottle { position: absolute; left: calc(50% - 38px); bottom: 10px; width: 76px; height: 120px; border: 0; padding: 0; background: none; cursor: pointer; transform-origin: 50% 100%; }
.rocket-bottle:focus-visible { outline: 3px solid #f0bb45; outline-offset: 4px; border-radius: 18px; }
.rocket-core { position: absolute; inset: 0; }
.rocket-body { position: absolute; left: 8px; right: 8px; bottom: 0; top: 28px; border: 4px solid #d8ecff; border-radius: 16px 16px 24px 24px; background: linear-gradient(90deg,rgba(255,255,255,.34),rgba(167,222,255,.15) 38%,rgba(255,255,255,.06)); box-shadow: inset 0 -54px 0 rgba(113,61,23,.93), inset 0 -62px 0 #dca84b; }
.rocket-body::after { content: "ЖИЖА"; position: absolute; left: 7px; right: 7px; bottom: 20px; padding: 4px 0; border-radius: 8px; background: #f0bb45; color: #17120c; font-weight: 950; font-size: 10px; }
.rocket-neck { position: absolute; left: 24px; top: 8px; width: 28px; height: 28px; border: 4px solid #d8ecff; border-bottom: 0; border-radius: 8px 8px 0 0; background: rgba(255,255,255,.16); }
.rocket-cap { position: absolute; left: 20px; top: 0; width: 36px; height: 12px; border-radius: 5px 5px 3px 3px; background: #e65444; border: 3px solid #7a231c; }
.rocket-fin { position: absolute; bottom: 8px; width: 24px; height: 40px; background: #e65444; border: 3px solid #6b211b; }
.rocket-fin.left { left: -12px; clip-path: polygon(100% 0,100% 100%,0 100%); }
.rocket-fin.right { right: -12px; clip-path: polygon(0 0,100% 100%,0 100%); }
.rocket-flame { position: absolute; left: 28px; bottom: -42px; width: 18px; height: 48px; opacity: 0; border-radius: 50% 50% 44% 44%; background: linear-gradient(#fff7b7,#ffa33e 45%,#e94429 78%,transparent); filter: drop-shadow(0 0 14px #ff9d2e); }
.rocket-bottle .launch-bubbles span { position: absolute; display: block; bottom: 18px; width: 9px; height: 9px; border: 2px solid rgba(255,255,255,.72); border-radius: 50%; opacity: 0; }
.rocket-bottle .launch-bubbles span:nth-child(1) { left: 12px; }
.rocket-bottle .launch-bubbles span:nth-child(2) { left: 34px; width: 12px; height: 12px; }
.rocket-bottle .launch-bubbles span:nth-child(3) { left: 52px; width: 8px; height: 8px; }
.rocket-bottle.launching { pointer-events: none; animation: continent-launch 1.9s cubic-bezier(.25,.62,.18,1) forwards; transform: translate(var(--dx), var(--dy)) rotate(var(--rot)); }
.rocket-bottle.launching .rocket-flame { opacity: 1; animation: rocket-flame .16s ease-in-out infinite alternate; }
.rocket-bottle.launching .launch-bubbles span { animation: launch-bubble .8s ease-out infinite; }
.rocket-bottle.is-done { opacity: 0; }
.rocket-returning { animation: rocket-return .5s ease-out; }
.launch-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; align-items: center; }
.global-reset { border: 0; border-radius: 999px; background: #20315f; color: #fff8e8; padding: 12px 18px; font-weight: 800; cursor: pointer; }
.global-reset:hover { filter: brightness(1.08); }
.local-copy { color: var(--muted); font-size: .98rem; }
@keyframes continent-launch { 0% { transform: translate(0,0) rotate(0deg) scale(1); opacity: 1; } 20% { transform: translate(0,-14px) scale(1.03); opacity: 1; } 100% { transform: translate(var(--dx), var(--dy)) rotate(var(--rot)) scale(.84); opacity: 0; } }
@keyframes rocket-flame { from { transform: scaleY(.78); } to { transform: scaleY(1.2); } }
@keyframes launch-bubble { 0% { transform: translateY(8px) scale(.45); opacity: 0; } 25% { opacity: 1; } 100% { transform: translateY(-72px) scale(1.1); opacity: 0; } }
@keyframes rocket-return { from { transform: scale(.85); opacity: .4; } to { transform: scale(1); opacity: 1; } }
@media (max-width: 920px) {
  .launch-world { min-height: 880px; }
  .continent-launch[data-continent="north-america"] { left: 5%; top: 16%; }
  .continent-launch[data-continent="south-america"] { left: 6%; top: 44%; }
  .continent-launch[data-continent="europe"] { left: 36%; top: 18%; }
  .continent-launch[data-continent="africa"] { left: 36%; top: 46%; }
  .continent-launch[data-continent="asia"] { right: 8%; top: 20%; }
  .continent-launch[data-continent="oceania"] { right: 10%; top: 52%; }
}
@media (max-width: 640px) {
  .launch-world { min-height: 1220px; }
  .continent-launch { width: 88%; left: 6% !important; right: auto !important; }
  .continent-launch[data-continent="north-america"] { top: 12%; }
  .continent-launch[data-continent="south-america"] { top: 25%; }
  .continent-launch[data-continent="europe"] { top: 38%; }
  .continent-launch[data-continent="africa"] { top: 51%; }
  .continent-launch[data-continent="asia"] { top: 64%; }
  .continent-launch[data-continent="oceania"] { top: 77%; }
  .launch-counter { top: auto; bottom: 16px; }
  .global-note { top: auto; right: auto; left: 16px; bottom: 16px; max-width: calc(100% - 170px); }
}
@media (prefers-reduced-motion: reduce) {
  .rocket-bottle.launching,
  .rocket-bottle.launching .rocket-flame,
  .rocket-bottle.launching .launch-bubbles span,
  .rocket-returning { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; }
}
"""
    text = text.replace("</style>", css + "</style>", 1)

    comic_name = f"kvassistent-{version}-comic.svg"
    section = f"""
<section class="companion-release" id="live-batch">
  <div class="eyebrow">Apps for Your Life · ИИ-агент на кухне</div>
  <h2>Один ИИ-агент — одна понятная партия кваса</h2>
  <p>КВАССИСТЕНТ даёт агенту простой рецепт, явное состояние партии и честные правила безопасности. Человек делает квас руками, агент держит контекст и предлагает только следующий шаг.</p>
  <div class="companion-benefits">
    <article><strong>Простой рецепт</strong>Сухари, вода, сахар, температура и семь коротких шагов для первой партии на 3 л.</article>
    <article><strong>Живая партия</strong>Один check-in превращает температуру, запах и поверхность в следующее действие.</article>
    <article><strong>Передача ИИ</strong>Структурированный handoff сохраняет подтверждённые факты и неизвестные, а не выдуманный контекст.</article>
  </div>
  <div class="companion-actions"><a class="companion-cta" href="companion/">Открыть живую партию <span aria-hidden="true">→</span></a><a class="companion-secondary" href="ru/instructions/">Инструкция для ИИ-агента →</a></div>
</section>

<section class="community-release" id="community-feedback">
  <div class="eyebrow">Сообщество КВАССИСТЕНТА</div>
  <h2>Твой напиток может стать следующей историей</h2>
  <p>Пришли рецепт, фото удачной партии, идею или сообщение об ошибке. Форма отправит обращение на <strong>kvassitent@gmail.com</strong>; публикацию материалов мы всегда согласуем отдельно.</p>
  <div class="community-actions"><a class="button primary" href="feedback/">Рассказать о своём напитке →</a><a class="community-social" href="https://www.instagram.com/kvassistent/">Instagram</a><a class="community-social" href="https://www.tiktok.com/@kvassistent">TikTok</a></div>
</section>

<section class="heat-release" id="hot-fermentation">
  <div class="eyebrow">Версия {version} · жара и солнце</div>
  <h2>При 28°C банку убрать с прямого солнца</h2>
  <p>28°C в тени — быстрый рабочий режим. Солнце может нагреть жидкость выше температуры воздуха. Измеряй именно жидкость и проверяй квас через 4–6 часов.</p>
  <div class="heat-grid">
    <article><strong>18–24°C</strong><br>спокойный режим</article>
    <article><strong>25–27°C</strong><br>проверка с 6 часов</article>
    <article><strong>28–30°C</strong><br>только тень, проверка с 4 часов</article>
    <article><strong>31°C+</strong><br>переставить в прохладу</article>
  </div>
  <div class="heat-danger"><strong>Сейчас:</strong> убрать банку с солнца, прикрыть чистой тканью или неплотной крышкой и измерить температуру жидкости.</div>
</section>

<section class="zero-alcohol-release" id="zero-alcohol-max-carbonation">
  <div class="eyebrow">Версия {version} · максимум газиков без алкоголя</div>
  <h2>Максимальная газированность без алкоголя</h2>
  <p>Новый акцент версии — режим «максимум пузырьков, минимум спирта». Мы не разгоняем длительное тёплое дображивание: используем быстрый короткий набор газа в ПЭТ, затем сразу холод, чтобы удержать карбонизацию и не наращивать алкоголь.</p>
  <div class="zero-grid">
    <article><strong>Короткое окно</strong><br>Вторичная карбонизация короткая: старт проверки через 60 минут при жаре и остановка сразу после набора давления.</article>
    <article><strong>Только ПЭТ</strong><br>Пищевой ПЭТ и контроль упругости бутылки позволяют ловить максимум безопасных газиков.</article>
    <article><strong>Быстрый холод</strong><br>Как только бутылка стала упругой, её сразу охлаждают минимум на 8–12 часов.</article>
    <article><strong>Без усиления алкоголя</strong><br>Не оставлять герметично тёплой надолго и не добавлять лишний сахар сверх дозы для газа.</article>
  </div>
  <div class="zero-note"><strong>Практический режим:</strong> целевая идея этой версии — «максимальная газированность без алкоголя», то есть короткий controlled bottle-conditioning cycle и немедленное охлаждение вместо долгого тёплого дображивания.</div>
</section>

<section class="rocket-launch-release" id="global-rocket-launch">
  <div class="eyebrow">Версия {version} · шесть континентов и локальное накопление</div>
  <h2>Бутылки-ракеты вылетают с 6 континентов каждые 10 секунд</h2>
  <p>Теперь запуск идёт с шести континентов: Северная Америка, Южная Америка, Европа, Африка, Азия и Океания. Каждые 10 секунд система локально выбирает следующую бутылку для пуска, увеличивает общий счётчик и сохраняет накопленный результат у пользователя в браузере.</p>
  <div class="launch-world" id="launch-world" aria-label="Глобальная карта запусков бутылок-ракет с шести континентов">
    <div class="launch-status" id="launch-status">Автозапуск каждые 10 секунд · локальное накопление включено</div>
    <div class="launch-counter" id="launch-counter">Запущено бутылок: <strong>0</strong></div>
    <div class="global-note">Хранение локально: твой браузер помнит накопленный счётчик.</div>

    <article class="continent-launch" data-continent="north-america">
      <h3>Северная Америка</h3>
      <small>launch source #1</small>
      <div class="continent-badge">🌎 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Северной Америки" style="--dx:-180px; --dy:-250px; --rot:-26deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
    <article class="continent-launch" data-continent="south-america">
      <h3>Южная Америка</h3>
      <small>launch source #2</small>
      <div class="continent-badge">🌎 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Южной Америки" style="--dx:-130px; --dy:-270px; --rot:-18deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
    <article class="continent-launch" data-continent="europe">
      <h3>Европа</h3>
      <small>launch source #3</small>
      <div class="continent-badge">🌍 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Европы" style="--dx:0px; --dy:-300px; --rot:-6deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
    <article class="continent-launch" data-continent="africa">
      <h3>Африка</h3>
      <small>launch source #4</small>
      <div class="continent-badge">🌍 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Африки" style="--dx:30px; --dy:-260px; --rot:10deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
    <article class="continent-launch" data-continent="asia">
      <h3>Азия</h3>
      <small>launch source #5</small>
      <div class="continent-badge">🌏 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Азии" style="--dx:170px; --dy:-250px; --rot:24deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
    <article class="continent-launch" data-continent="oceania">
      <h3>Океания</h3>
      <small>launch source #6</small>
      <div class="continent-badge">🌏 Локально копится</div>
      <button class="rocket-bottle" type="button" aria-label="Запустить бутылку из Океании" style="--dx:120px; --dy:-220px; --rot:17deg;">
        <span class="rocket-core"><span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span><span class="rocket-fin left"></span><span class="rocket-fin right"></span><span class="rocket-flame"></span><span class="launch-bubbles"><span></span><span></span><span></span></span></span>
      </button>
    </article>
  </div>
  <div class="launch-actions">
    <button class="global-reset" id="global-reset" type="button">Сбросить локальный счётчик</button>
    <div class="local-copy">Автозапуск: каждые 10 секунд. Счётчик хранится локально через localStorage.</div>
  </div>
</section>

<section class="comic-release" id="comic-guide">
  <div class="eyebrow">Версия {version} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>Комикс версии собран вокруг новой идеи: шесть континентов, автоматические пуски каждые 10 секунд, локальное накопление и режим максимальной газированности без алкоголя.</p>
  <p><strong>Главная мысль:</strong> визуальный эффект глобальных пусков живёт на странице, а для напитка мы всё равно держим безопасный сценарий — короткая карбонизация и быстрый холод.</p>
  <figure>
    <a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="Схематический комикс КВАССИСТЕНТА: шесть континентов, локальный счётчик и максимальная газированность без алкоголя" loading="lazy"></a>
    <figcaption>Комикс поддерживает глобальную тему версии: шесть точек запуска, автопуски, локальное накопление счётчика и отдельный блок про максимально газированный безалкогольный режим.</figcaption>
  </figure>
</section>
"""
    text = text.replace(marker, section + marker, 1)

    script = """
<script>
(() => {
  const world = document.getElementById('launch-world');
  const counter = document.getElementById('launch-counter');
  const counterValue = counter ? counter.querySelector('strong') : null;
  const status = document.getElementById('launch-status');
  const reset = document.getElementById('global-reset');
  const storageKey = 'kvassistent-global-launch-count-v13';
  const continents = Array.from(document.querySelectorAll('.continent-launch'));
  if (!world || !counterValue || !status || !reset || !continents.length) return;

  const labels = {
    'north-america': 'Северная Америка',
    'south-america': 'Южная Америка',
    europe: 'Европа',
    africa: 'Африка',
    asia: 'Азия',
    oceania: 'Океания'
  };

  let total = Number.parseInt(localStorage.getItem(storageKey) || '0', 10);
  if (!Number.isFinite(total) || total < 0) total = 0;
  let index = 0;
  let intervalId = null;
  counterValue.textContent = String(total);

  function persist() {
    localStorage.setItem(storageKey, String(total));
    counterValue.textContent = String(total);
  }

  function relaunchBottle(continent) {
    const rocket = continent.querySelector('.rocket-bottle');
    if (!rocket) return;
    rocket.classList.remove('launching', 'is-done', 'rocket-returning');
    void rocket.offsetWidth;
    rocket.classList.add('rocket-returning');
  }

  function fireFrom(continent) {
    if (!continent) return;
    const rocket = continent.querySelector('.rocket-bottle');
    const key = continent.dataset.continent;
    if (!rocket || !key) return;
    continent.classList.add('local-accumulated');
    rocket.classList.remove('rocket-returning', 'launching', 'is-done');
    void rocket.offsetWidth;
    rocket.classList.add('launching');
    total += 1;
    persist();
    status.textContent = `Запуск: ${labels[key]} · всего локально накоплено ${total}`;
    window.setTimeout(() => {
      rocket.classList.add('is-done');
      relaunchBottle(continent);
    }, 1900);
  }

  continents.forEach((continent) => {
    continent.addEventListener('click', () => fireFrom(continent));
  });

  function tick() {
    fireFrom(continents[index % continents.length]);
    index += 1;
  }

  function start() {
    if (intervalId) return;
    intervalId = window.setInterval(tick, 10000);
  }

  reset.addEventListener('click', () => {
    total = 0;
    localStorage.removeItem(storageKey);
    counterValue.textContent = '0';
    status.textContent = 'Локальный счётчик сброшен · автозапуск продолжается каждые 10 секунд';
    continents.forEach((continent) => continent.classList.remove('local-accumulated'));
  });

  start();
  status.textContent = 'Автозапуск каждые 10 секунд · локальный накопленный счётчик загружен';
})();
</script>
"""
    text = text.replace("</body>", script + "</body>", 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    comic = ROOT / f"dist/site/v{version}/assets/kvassistent-{version}-comic.svg"
    companion = ROOT / f"dist/site/v{version}/companion"
    feedback = ROOT / f"dist/site/v{version}/feedback"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="live-batch"',
        'href="companion/"',
        "Один ИИ-агент — одна понятная партия кваса",
        'href="ru/instructions/"',
        "Простой рецепт",
        'id="hot-fermentation"',
        'id="zero-alcohol-max-carbonation"',
        "Максимальная газированность без алкоголя",
        'id="global-rocket-launch"',
        'id="launch-counter"',
        "Запущено бутылок:",
        'data-continent="north-america"',
        'data-continent="south-america"',
        'data-continent="europe"',
        'data-continent="africa"',
        'data-continent="asia"',
        'data-continent="oceania"',
        "каждые 10 секунд",
        "localStorage",
        'id="global-reset"',
        'id="comic-guide"',
        "При 28°C банку убрать с прямого солнца",
        f"kvassistent-{version}-comic.svg",
        "Реальная партия — в простом комиксе",
        'id="community-feedback"',
        'href="feedback/"',
        "kvassitent@gmail.com",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")
    companion_required = ("index.html", "styles.css", "engine.js", "preferences.js", "app.js", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js")
    missing_companion = [name for name in companion_required if not (companion / name).is_file()]
    if missing_companion:
        raise RuntimeError(f"Companion assets were not copied: {missing_companion}")
    feedback_required = ("index.html", "styles.css", "thanks.html")
    missing_feedback = [name for name in feedback_required if not (feedback / name).is_file()]
    if missing_feedback:
        raise RuntimeError(f"Feedback assets were not copied: {missing_feedback}")
    feedback_text = (feedback / "index.html").read_text(encoding="utf-8")
    if "formsubmit.co/kvassitent@gmail.com" not in feedback_text or "www.instagram.com/kvassistent" not in feedback_text or "www.tiktok.com/@kvassistent" not in feedback_text:
        raise RuntimeError("Feedback page misses email delivery or social channels")
    companion_text = (companion / "index.html").read_text(encoding="utf-8")
    if "Живая партия" not in companion_text or "Простой квас без догадок" not in companion_text:
        raise RuntimeError("Companion entry point misses the feature title")
    if "consent-card" not in companion_text or 'data-consent="essential"' not in companion_text:
        raise RuntimeError("Companion entry point misses privacy consent controls")
    if 'option value="el"' not in companion_text or 'id="nearby-kvass"' not in companion_text:
        raise RuntimeError("Companion entry point misses Greek or nearby-kvass discovery")
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
    core = load_core()
    core.main()
    install_comic(version)
    install_companion(version)
    install_feedback(version)
    patch_landing(version)
    verify(version)
    print(f"Built КВАССИСТЕНТ {meta['display']} with six-continent bottle launches, local counter persistence, 10-second auto-launch cadence, and max carbonation without alcohol")


if __name__ == "__main__":
    main()
