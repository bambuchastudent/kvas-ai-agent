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


def install_tree(source: Path, version: str, name: str, required: tuple[str, ...]) -> Path:
    missing = [filename for filename in required if not (source / filename).is_file()]
    if missing:
        raise RuntimeError(f"Missing {name} assets: {missing}")
    target = ROOT / f"dist/site/v{version}/{name}"
    shutil.copytree(source, target, dirs_exist_ok=True)
    return target


def install_companion(version: str) -> Path:
    required = (
        "index.html", "styles.css", "engine.js", "preferences.js", "app.js",
        "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js",
    )
    return install_tree(COMPANION, version, "companion", required)


def install_feedback(version: str) -> Path:
    return install_tree(FEEDBACK, version, "feedback", ("index.html", "styles.css", "thanks.html"))


def patch_landing(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    marker = '<section class="audience-section people" id="for-people">'
    if marker not in text:
        raise RuntimeError("Cannot find human section marker in landing page")

    # Make the human quick-start produce an actually carbonated drink rather than stopping after primary fermentation.
    text = text.replace(
        "При нормальном запахе и пузырьках разлей в пластиковые бутылки. Догазируй 2–6 часов. Как бутылка стала твёрдой — сразу в холодильник минимум на 8 часов.",
        "После первичного брожения процеди и разлей только в ПЭТ-бутылки. Добавь 4 г сахара на 1 л, оставь 10–15% воздуха и закрой. Как бутылка стала упругой — сразу в холодильник минимум на 8–12 часов.",
    )

    css = r"""
.heat-release,
.comic-release { margin: 30px 0; padding: 26px; border-radius: 18px; }
.heat-release { border: 2px solid #d48a18; background: #fff5dc; }
.comic-release { border: 2px solid #493a8a; background: #f6f3ff; }
.heat-release h2,
.comic-release h2 { margin-top: 0; }
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
.carbonation-release { margin: 32px 0; padding: clamp(24px,5vw,46px); border-radius: 26px; color: #f8f2df; background: radial-gradient(circle at 50% 105%,rgba(240,187,69,.25),transparent 32%),linear-gradient(180deg,#111b37,#080b17 72%); border: 2px solid #eeb53f; overflow: hidden; }
.carbonation-release h2 { max-width: 850px; margin: 12px 0; color: #fff8e8; font-size: clamp(36px,7vw,72px); line-height: .95; }
.carbonation-release > p { max-width: 800px; color: #cbd4eb; }
.carbonation-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(190px,1fr)); gap: 12px; margin: 24px 0; }
.carbonation-grid article { padding: 16px; border: 1px solid rgba(238,181,63,.35); border-radius: 15px; background: rgba(255,255,255,.055); color: #cbd4eb; }
.carbonation-grid strong { display: block; margin-bottom: 7px; color: #fff4c8; }
.carbonation-warning { margin: 18px 0 24px; padding: 15px 17px; border-left: 5px solid #ff796f; border-radius: 9px; background: rgba(117,24,24,.32); color: #ffe6e2; }
.launch-pad { position: relative; min-height: 430px; margin-top: 25px; border: 1px solid rgba(142,179,255,.36); border-radius: 22px; overflow: hidden; background: radial-gradient(circle at 50% 110%,#385797 0 8%,transparent 34%),radial-gradient(circle at 16% 18%,#fff 0 1px,transparent 2px),radial-gradient(circle at 76% 24%,#fff 0 1px,transparent 2px),radial-gradient(circle at 42% 9%,#fff 0 1.5px,transparent 2.5px),linear-gradient(#101c42,#050814); }
.launch-pad::after { content:""; position:absolute; inset:auto 0 0; height:82px; background:linear-gradient(#34445f,#172033); border-top:5px solid #eeb53f; }
.launch-status { position:absolute; z-index:8; top:18px; left:50%; transform:translateX(-50%); min-width:210px; padding:9px 15px; border:1px solid rgba(238,181,63,.55); border-radius:999px; background:rgba(3,7,18,.78); color:#fff4c8; text-align:center; font-weight:850; letter-spacing:.08em; }
.bottle-rocket { position:absolute; z-index:4; bottom:72px; width:78px; height:205px; transform-origin:50% 100%; }
.bottle-rocket.left { left:calc(50% - 145px); }
.bottle-rocket.right { right:calc(50% - 145px); }
.bottle-body { position:absolute; inset:38px 7px 0; border:4px solid #d8ecff; border-radius:18px 18px 25px 25px; background:linear-gradient(90deg,rgba(255,255,255,.3),rgba(110,195,255,.15) 35%,rgba(255,255,255,.08)); box-shadow:inset 0 -70px 0 rgba(115,65,20,.88),inset 0 -78px 0 #dca84b; }
.bottle-body::before { content:"ЖИЖА"; position:absolute; left:7px; right:7px; bottom:42px; padding:7px 2px; border-radius:7px; background:#f0bb45; color:#17130d; text-align:center; font-size:11px; font-weight:950; }
.bottle-neck { position:absolute; left:26px; top:8px; width:27px; height:42px; border:4px solid #d8ecff; border-bottom:0; border-radius:8px 8px 0 0; background:rgba(255,255,255,.15); }
.bottle-cap { position:absolute; left:22px; top:0; width:35px; height:13px; border-radius:5px 5px 2px 2px; background:#e65444; border:3px solid #7b211b; }
.fin { position:absolute; bottom:13px; width:28px; height:54px; background:#e65444; border:3px solid #6c211b; }
.fin.left { left:-14px; clip-path:polygon(100% 0,100% 100%,0 100%); }
.fin.right { right:-14px; clip-path:polygon(0 0,100% 100%,0 100%); }
.flame { position:absolute; left:27px; bottom:-54px; width:25px; height:66px; opacity:0; border-radius:50% 50% 48% 48%; background:linear-gradient(#fff5ac,#ff9d2e 48%,#f0442b 75%,transparent); filter:drop-shadow(0 0 15px #ff9d2e); transform-origin:50% 0; }
.launch-arm { position:absolute; z-index:5; bottom:102px; width:126px; height:22px; border:4px solid #6a7f9e; border-radius:10px; background:#a9bdd5; transform-origin:12px 50%; }
.launch-arm::after { content:""; position:absolute; right:-13px; top:-12px; width:30px; height:42px; border:4px solid #6a7f9e; border-radius:9px; background:#d8e4ef; }
.launch-arm.left { left:calc(50% - 250px); transform:rotate(-8deg); }
.launch-arm.right { right:calc(50% - 250px); transform:scaleX(-1) rotate(-8deg); }
.launch-button { display:block; margin:22px auto 0; padding:15px 24px; border:0; border-radius:999px; background:#f0bb45; color:#11172a; font:900 14px inherit; letter-spacing:.08em; cursor:pointer; box-shadow:0 10px 30px rgba(240,187,69,.25); }
.launch-button:hover { filter:brightness(1.08); transform:translateY(-1px); }
.launch-pad.launching .launch-arm.left { animation:arm-left .72s ease-in forwards; }
.launch-pad.launching .launch-arm.right { animation:arm-right .72s ease-in forwards; }
.launch-pad.launching .bottle-rocket { animation:bottle-launch 2.7s .28s cubic-bezier(.32,.04,.28,1) forwards; }
.launch-pad.launching .bottle-rocket.right { animation-name:bottle-launch-right; }
.launch-pad.launching .flame { animation:flame-on 2.1s .2s ease-in forwards; }
@keyframes arm-left { to { transform:translateX(-90px) rotate(-68deg); opacity:.35; } }
@keyframes arm-right { to { transform:scaleX(-1) translateX(-90px) rotate(-68deg); opacity:.35; } }
@keyframes bottle-launch { 0%{transform:translate(0,0) rotate(-2deg)} 16%{transform:translate(-4px,-18px) rotate(2deg)} 100%{transform:translate(-110px,-650px) rotate(-13deg)} }
@keyframes bottle-launch-right { 0%{transform:translate(0,0) rotate(2deg)} 16%{transform:translate(4px,-18px) rotate(-2deg)} 100%{transform:translate(110px,-650px) rotate(13deg)} }
@keyframes flame-on { 0%{opacity:0;transform:scaleY(.2)} 12%{opacity:1} 55%{transform:scaleY(1.2)} 100%{opacity:1;transform:scaleY(.75)} }
@media (max-width:640px) { .launch-pad{min-height:390px}.bottle-rocket.left{left:calc(50% - 105px)}.bottle-rocket.right{right:calc(50% - 105px)}.launch-arm.left{left:calc(50% - 190px)}.launch-arm.right{right:calc(50% - 190px)} }
@media (prefers-reduced-motion:reduce) { .launch-pad.launching .launch-arm,.launch-pad.launching .bottle-rocket,.launch-pad.launching .flame{animation:none!important}.launch-pad.launching .flame{opacity:1} }
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

<section class="carbonation-release" id="carbonation-launch">
  <div class="eyebrow">Версия {version} · газики и два ракетных пуска</div>
  <h2>Квас не заканчивается в банке. Ему нужна карбонизация.</h2>
  <p>После первичного брожения дрожжи ещё живы. Небольшая точная порция сахара в закрытой ПЭТ-бутылке создаёт углекислый газ; холод затем удерживает его в напитке.</p>
  <div class="carbonation-grid">
    <article><strong>1. Процедить</strong>Убрать хлеб и крупный осадок, но не стерилизовать напиток: немного дрожжей должно остаться.</article>
    <article><strong>2. Прайминг</strong>Добавить <b>4 г сахара на 1 л</b>. Для бутылки 1,5 л — 6 г, примерно 1½ ровной чайной ложки.</article>
    <article><strong>3. Только ПЭТ</strong>Оставить 10–15% свободного объёма, слегка сжать бутылку, закрутить и поставить в тень.</article>
    <article><strong>4. Поймать давление</strong>При 20–24°C проверять через 4 часа; при 28°C — каждый час, начиная с первого. Стала упругой — сразу в холод.</article>
    <article><strong>5. Холод</strong>Выдержать 8–12 часов в холодильнике. Открывать медленно над раковиной, не встряхивая.</article>
  </div>
  <div class="carbonation-warning"><strong>Безопасность:</strong> не использовать стекло. Если ПЭТ стала каменной или раздулась — сразу охладить и осторожно стравить газ. Ракеты ниже существуют только на экране: реальные бутылки не запускать.</div>
  <div class="launch-pad" id="launch-pad" aria-label="Анимация одновременного запуска двух бутылок-ракет">
    <div class="launch-status" id="launch-status" aria-live="polite">СИСТЕМЫ ГОТОВЫ</div>
    <div class="launch-arm left" aria-hidden="true"></div>
    <div class="launch-arm right" aria-hidden="true"></div>
    <div class="bottle-rocket left" aria-hidden="true"><i class="bottle-cap"></i><i class="bottle-neck"></i><i class="bottle-body"></i><i class="fin left"></i><i class="fin right"></i><i class="flame"></i></div>
    <div class="bottle-rocket right" aria-hidden="true"><i class="bottle-cap"></i><i class="bottle-neck"></i><i class="bottle-body"></i><i class="fin left"></i><i class="fin right"></i><i class="flame"></i></div>
  </div>
  <button class="launch-button" id="launch-button" type="button">ЗАПУСТИТЬ ДВЕ БУТЫЛКИ-РАКЕТЫ</button>
</section>

<section class="comic-release" id="comic-guide">
  <div class="eyebrow">Версия {version} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>Новая схема доводит процесс до результата: настой, дрожжи, открытое первичное брожение, розлив в ПЭТ, 4 г сахара на литр, набор давления и обязательное охлаждение.</p>
  <p><strong>Главная мысль:</strong> первичное брожение не герметизировать; вторичную карбонизацию делать только в ПЭТ и остановить холодом, как только бутылка стала упругой.</p>
  <figure>
    <a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="Комикс КВАССИСТЕНТА: восемь этапов приготовления газированного кваса и финальный запуск бутылок-ракет" loading="lazy"></a>
    <figcaption>Векторная SVG-схема остаётся чёткой на телефоне. Финальный ракетный пуск — шутливая анимация; реальные бутылки должны оставаться в холодильнике.</figcaption>
  </figure>
</section>
"""
    text = text.replace(marker, section + marker, 1)

    launch_script = r"""
<script>
(() => {
  const pad = document.getElementById('launch-pad');
  const button = document.getElementById('launch-button');
  const status = document.getElementById('launch-status');
  if (!pad || !button || !status) return;
  let busy = false;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function launch() {
    if (busy) return;
    busy = true;
    pad.classList.remove('launching');
    void pad.offsetWidth;
    pad.classList.add('launching');
    button.disabled = true;
    status.textContent = reduceMotion ? 'ПУСК ПОДТВЕРЖДЁН' : '3 · 2 · 1 · ПУСК';
    setTimeout(() => { status.textContent = 'ДВА ПУСКА · ОРБИТА ДОСТИГНУТА'; }, reduceMotion ? 200 : 2600);
    setTimeout(() => {
      pad.classList.remove('launching');
      status.textContent = 'СИСТЕМЫ ГОТОВЫ';
      button.disabled = false;
      busy = false;
    }, reduceMotion ? 900 : 4400);
  }
  button.addEventListener('click', launch);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        observer.disconnect();
        setTimeout(launch, 450);
      }
    }, { threshold: .62 });
    observer.observe(pad);
  }
})();
</script>
"""
    text = text.replace("</body>", launch_script + "</body>", 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    comic = ROOT / f"dist/site/v{version}/assets/kvassistent-{version}-comic.svg"
    companion = ROOT / f"dist/site/v{version}/companion"
    feedback = ROOT / f"dist/site/v{version}/feedback"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="live-batch"', 'href="companion/"', "Один ИИ-агент — одна понятная партия кваса",
        'href="ru/instructions/"', "Простой рецепт", 'id="hot-fermentation"',
        'id="comic-guide"', "При 28°C банку убрать с прямого солнца",
        f"kvassistent-{version}-comic.svg", "Реальная партия — в простом комиксе",
        'id="community-feedback"', 'href="feedback/"', "kvassitent@gmail.com",
        'id="carbonation-launch"', "4 г сахара на 1 л", 'id="launch-pad"',
        "ЗАПУСТИТЬ ДВЕ БУТЫЛКИ-РАКЕТЫ", "IntersectionObserver",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")

    companion_required = (
        "index.html", "styles.css", "engine.js", "preferences.js", "app.js",
        "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "sw.js",
    )
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
    print(f"Built КВАССИСТЕНТ {meta['display']} with carbonation, synchronized bottle-rocket launches, live-batch companion, and comic guide")


if __name__ == "__main__":
    main()
