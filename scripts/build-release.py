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
.rocket-launch-release { margin: 30px 0; padding: 26px; border-radius: 18px; }
.heat-release { border: 2px solid #d48a18; background: #fff5dc; }
.comic-release { border: 2px solid #493a8a; background: #f6f3ff; }
.rocket-launch-release { border: 2px solid #20315f; background: linear-gradient(180deg,#eef5ff,#f7fbff); }
.heat-release h2,
.comic-release h2,
.rocket-launch-release h2 { margin-top: 0; }
.heat-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 12px; }
.heat-grid article { padding: 14px; border-radius: 12px; background: #fffdf7; border: 1px solid #e7c98d; }
.heat-danger { margin-top: 15px; padding: 14px; border-left: 5px solid #a52b20; background: #fff0ea; }
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
.launch-hangar { position: relative; min-height: 450px; margin-top: 22px; border: 1px solid rgba(32,49,95,.18); border-radius: 24px; overflow: hidden; background: radial-gradient(circle at 20% 18%,rgba(255,255,255,.95),transparent 1.5%),radial-gradient(circle at 83% 24%,rgba(255,255,255,.9),transparent 1.8%),radial-gradient(circle at 59% 14%,rgba(255,255,255,.85),transparent 1.4%),linear-gradient(180deg,#122047,#08111f 68%,#34445f 68%,#1c2738 100%); }
.launch-counter { position: absolute; top: 14px; right: 14px; z-index: 20; padding: 10px 14px; border-radius: 16px; background: rgba(7,12,23,.82); color: #fff8e8; border: 1px solid rgba(240,187,69,.65); font-weight: 800; font-size: .95rem; }
.launch-counter strong { color: #f0bb45; font-size: 1.08rem; }
.launch-status { position: absolute; top: 16px; left: 16px; z-index: 20; padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,.12); color: #e8f0ff; border: 1px solid rgba(255,255,255,.24); font-weight: 750; }
.rocket-bottle { position: absolute; bottom: 58px; width: 96px; height: 255px; border: 0; padding: 0; background: none; cursor: pointer; transform-origin: 50% 100%; transition: transform .15s ease, filter .15s ease; }
.rocket-bottle:hover { transform: translateY(-4px) scale(1.03); filter: drop-shadow(0 18px 25px rgba(0,0,0,.25)); }
.rocket-bottle:focus-visible { outline: 3px solid #f0bb45; outline-offset: 6px; border-radius: 20px; }
.rocket-bottle[data-direction="left"] { left: 12%; --dx: -200px; --dy: -360px; --rot: -28deg; }
.rocket-bottle[data-direction="center"] { left: calc(50% - 48px); --dx: 0px; --dy: -430px; --rot: -6deg; }
.rocket-bottle[data-direction="right"] { right: 12%; --dx: 200px; --dy: -360px; --rot: 28deg; }
.rocket-core { position: absolute; inset: 0; }
.rocket-body { position: absolute; left: 8px; right: 8px; bottom: 0; top: 42px; border: 4px solid #d8ecff; border-radius: 18px 18px 28px 28px; background: linear-gradient(90deg,rgba(255,255,255,.35),rgba(167,222,255,.16) 38%,rgba(255,255,255,.08)); box-shadow: inset 0 -96px 0 rgba(112,61,24,.92), inset 0 -106px 0 #dca84b; }
.rocket-body::after { content: "ЖИЖА"; position: absolute; left: 10px; right: 10px; bottom: 38px; padding: 6px 0; border-radius: 8px; background: #f0bb45; color: #18110b; font-weight: 950; font-size: 12px; letter-spacing: .06em; }
.rocket-neck { position: absolute; left: 33px; top: 11px; width: 30px; height: 45px; border: 4px solid #d8ecff; border-bottom: 0; border-radius: 9px 9px 0 0; background: rgba(255,255,255,.18); }
.rocket-cap { position: absolute; left: 28px; top: 0; width: 40px; height: 14px; border-radius: 5px 5px 3px 3px; background: #e65444; border: 3px solid #7a231c; }
.rocket-fin { position: absolute; bottom: 10px; width: 30px; height: 58px; background: #e65444; border: 3px solid #6b211b; }
.rocket-fin.left { left: -16px; clip-path: polygon(100% 0,100% 100%,0 100%); }
.rocket-fin.right { right: -16px; clip-path: polygon(0 0,100% 100%,0 100%); }
.rocket-arm { position: absolute; top: 110px; width: 22px; height: 70px; border-radius: 12px; background: #dfe8f3; border: 3px solid #6d829f; }
.rocket-arm.left { left: -26px; transform: rotate(-18deg); }
.rocket-arm.right { right: -26px; transform: rotate(18deg); }
.rocket-flame { position: absolute; left: 36px; bottom: -72px; width: 24px; height: 74px; opacity: 0; border-radius: 50% 50% 45% 45%; background: linear-gradient(#fff6b2,#ffa139 48%,#ea4729 75%,transparent); filter: drop-shadow(0 0 16px #ff9d2e); transform-origin: 50% 0; }
.rocket-bottle .launch-bubbles span { position: absolute; display: block; bottom: 32px; width: 10px; height: 10px; border: 2px solid rgba(255,255,255,.74); border-radius: 50%; opacity: 0; }
.rocket-bottle .launch-bubbles span:nth-child(1) { left: 18px; }
.rocket-bottle .launch-bubbles span:nth-child(2) { left: 44px; width: 14px; height: 14px; }
.rocket-bottle .launch-bubbles span:nth-child(3) { left: 66px; width: 8px; height: 8px; }
.rocket-bottle.launched { pointer-events: none; animation: rocket-fly 1.8s cubic-bezier(.22,.61,.18,1) forwards; }
.rocket-bottle.launched .rocket-flame { opacity: 1; animation: rocket-flame .14s ease-in-out infinite alternate; }
.rocket-bottle.launched .launch-bubbles span { animation: launch-bubble .7s ease-out infinite; }
.rocket-bottle.is-done { opacity: .1; }
.launch-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; }
.launch-reset { border: 0; border-radius: 999px; background: #20315f; color: #fff8e8; padding: 12px 18px; font-weight: 800; cursor: pointer; }
.launch-reset:hover { filter: brightness(1.08); }
.launch-note { color: var(--muted); font-size: .98rem; align-self: center; }
@keyframes rocket-fly { 0% { transform: translate(0,0) rotate(0deg) scale(1); opacity: 1; } 14% { transform: translate(0,-18px) rotate(1deg) scale(1.03); opacity: 1; } 100% { transform: translate(var(--dx), var(--dy)) rotate(var(--rot)) scale(.88); opacity: 0; } }
@keyframes rocket-flame { from { transform: scaleY(.78); } to { transform: scaleY(1.22); } }
@keyframes launch-bubble { 0% { transform: translateY(10px) scale(.4); opacity: 0; } 25% { opacity: 1; } 100% { transform: translateY(-90px) scale(1.1); opacity: 0; } }
@media (max-width: 760px) {
  .launch-hangar { min-height: 520px; }
  .rocket-bottle[data-direction="left"] { left: 6%; }
  .rocket-bottle[data-direction="right"] { right: 6%; }
  .launch-counter { top: auto; bottom: 14px; }
}
@media (max-width: 520px) {
  .launch-hangar { min-height: 620px; }
  .rocket-bottle[data-direction="left"] { left: calc(50% - 145px); bottom: 88px; }
  .rocket-bottle[data-direction="center"] { bottom: 188px; }
  .rocket-bottle[data-direction="right"] { right: calc(50% - 145px); bottom: 88px; }
}
@media (prefers-reduced-motion: reduce) {
  .rocket-bottle,
  .rocket-bottle.launched,
  .rocket-bottle.launched .rocket-flame,
  .rocket-bottle.launched .launch-bubbles span { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition: none !important; }
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

<section class="rocket-launch-release" id="rocket-launch">
  <div class="eyebrow">Версия {version} · кликабельные ракеты-бутылки</div>
  <h2>Нажми на бутылку-ракету — и она улетит в свою сторону</h2>
  <p>Теперь каждая бутылка запускается отдельно. Левая уходит влево, центральная летит почти строго вверх, правая — вправо. Маленький счётчик в углу считает, сколько бутылок уже запущено.</p>
  <div class="launch-hangar" id="launch-hangar" aria-label="Интерактивная площадка запуска бутылок-ракет">
    <div class="launch-status" id="launch-status">Выбирай бутылку для запуска</div>
    <div class="launch-counter" id="launch-counter">Запущено бутылок: <strong>0</strong></div>

    <button class="rocket-bottle" type="button" data-direction="left" aria-label="Запустить левую бутылку-ракету">
      <span class="rocket-core">
        <span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span>
        <span class="rocket-fin left"></span><span class="rocket-fin right"></span>
        <span class="rocket-arm left"></span><span class="rocket-arm right"></span>
        <span class="rocket-flame"></span>
        <span class="launch-bubbles"><span></span><span></span><span></span></span>
      </span>
    </button>

    <button class="rocket-bottle" type="button" data-direction="center" aria-label="Запустить центральную бутылку-ракету">
      <span class="rocket-core">
        <span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span>
        <span class="rocket-fin left"></span><span class="rocket-fin right"></span>
        <span class="rocket-arm left"></span><span class="rocket-arm right"></span>
        <span class="rocket-flame"></span>
        <span class="launch-bubbles"><span></span><span></span><span></span></span>
      </span>
    </button>

    <button class="rocket-bottle" type="button" data-direction="right" aria-label="Запустить правую бутылку-ракету">
      <span class="rocket-core">
        <span class="rocket-cap"></span><span class="rocket-neck"></span><span class="rocket-body"></span>
        <span class="rocket-fin left"></span><span class="rocket-fin right"></span>
        <span class="rocket-arm left"></span><span class="rocket-arm right"></span>
        <span class="rocket-flame"></span>
        <span class="launch-bubbles"><span></span><span></span><span></span></span>
      </span>
    </button>
  </div>
  <div class="launch-actions">
    <button class="launch-reset" id="launch-reset" type="button">Сбросить пуски</button>
    <div class="launch-note">Каждая бутылка считается только один раз, пока ты не нажмёшь сброс.</div>
  </div>
</section>

<section class="comic-release" id="comic-guide">
  <div class="eyebrow">Версия {version} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>Схема собрана по фотогалерее этой партии: подготовка сухарей, замачивание, перелив в бутыль, открытое брожение под тканью и проверка примерно через сутки при 28°C.</p>
  <p><strong>Главная мысль:</strong> не закупоривать первичное брожение, не держать бутыль на прямом солнце и перед розливом проверить запах, поверхность и вкус.</p>
  <figure>
    <a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="Схематический комикс КВАССИСТЕНТА: ракеты-бутылки и счётчик запусков" loading="lazy"></a>
    <figcaption>В новой версии комикс поддерживает тему отдельных запусков: бутылки расходятся по разным траекториям, а счётчик в углу показывает прогресс.</figcaption>
  </figure>
</section>
"""
    text = text.replace(marker, section + marker, 1)

    script = """
<script>
(() => {
  const hangar = document.getElementById('launch-hangar');
  const counter = document.getElementById('launch-counter');
  const counterValue = counter ? counter.querySelector('strong') : null;
  const status = document.getElementById('launch-status');
  const reset = document.getElementById('launch-reset');
  const rockets = Array.from(document.querySelectorAll('.rocket-bottle[data-direction]'));
  if (!hangar || !counterValue || !status || !reset || !rockets.length) return;

  const labels = { left: 'Левая ракета ушла влево', center: 'Центральная ракета ушла вверх', right: 'Правая ракета ушла вправо' };
  let launched = 0;

  function updateCounter() {
    counterValue.textContent = String(launched);
    if (launched === rockets.length) {
      status.textContent = 'Все бутылки запущены';
    }
  }

  function launchRocket(rocket) {
    if (rocket.dataset.launched === 'true') return;
    rocket.dataset.launched = 'true';
    rocket.classList.add('launched');
    launched += 1;
    status.textContent = labels[rocket.dataset.direction] || 'Бутылка запущена';
    updateCounter();
    window.setTimeout(() => rocket.classList.add('is-done'), 1750);
  }

  rockets.forEach((rocket) => {
    rocket.addEventListener('click', () => launchRocket(rocket));
  });

  reset.addEventListener('click', () => {
    launched = 0;
    counterValue.textContent = '0';
    status.textContent = 'Выбирай бутылку для запуска';
    rockets.forEach((rocket) => {
      rocket.dataset.launched = 'false';
      rocket.classList.remove('launched', 'is-done');
      rocket.style.animation = 'none';
      void rocket.offsetWidth;
      rocket.style.animation = '';
    });
  });
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
        'id="rocket-launch"',
        'id="launch-counter"',
        "Запущено бутылок:",
        'data-direction="left"',
        'data-direction="center"',
        'data-direction="right"',
        'id="launch-reset"',
        "Все бутылки запущены",
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
    print(f"Built КВАССИСТЕНТ {meta['display']} with clickable bottle rockets, launch counter, and comic guide")


if __name__ == "__main__":
    main()
