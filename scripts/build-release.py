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


def patch_landing(version: str) -> None:
    landing = ROOT / f"dist/site/v{version}/index.html"
    text = landing.read_text(encoding="utf-8")
    marker = '<section class="audience-section people" id="for-people">'
    if marker not in text:
        raise RuntimeError("Cannot find human section marker in landing page")

    css = """
.companion-release,.community-release,.heat-release,.globe-game-release,.comic-release{margin:30px 0;padding:clamp(24px,5vw,44px);border-radius:24px}
.companion-release{color:#f6f0df;background:radial-gradient(circle at 90% 5%,rgba(240,187,69,.2),transparent 36%),#17130d;border:1px solid #67522a}
.companion-release .eyebrow{color:#f0bb45}.companion-release h2{max-width:780px;margin:14px 0;color:#fff8e8;font-size:clamp(34px,6vw,64px);line-height:.98}.companion-release p{max-width:720px;color:#c8bea8}
.companion-benefits{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:26px 0}.companion-benefits article{padding:16px;border:1px solid #433a2c;border-radius:14px;background:rgba(255,255,255,.035);color:#c8bea8}.companion-benefits strong{display:block;margin-bottom:5px;color:#fff8e8}.companion-actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center}.companion-cta{display:inline-flex;align-items:center;gap:18px;padding:15px 20px;border-radius:999px;color:#17130d;background:#f0bb45;text-decoration:none;font-weight:850}.companion-secondary{color:#f0bb45;font-weight:750}
.community-release{border:2px solid #317054;background:linear-gradient(135deg,#effcf4,#fffdf7)}.community-release h2{max-width:760px;margin:10px 0;font-size:clamp(34px,6vw,60px);line-height:1}.community-release p{max-width:720px}.community-actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:22px}.community-social{color:#22573f;font-weight:800;text-decoration:none}
.heat-release{border:2px solid #d48a18;background:#fff5dc}.heat-release h2,.comic-release h2{margin-top:0}.heat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.heat-grid article{padding:14px;border-radius:12px;background:#fffdf7;border:1px solid #e7c98d}.heat-danger{margin-top:15px;padding:14px;border-left:5px solid #a52b20;background:#fff0ea}
.globe-game-release{position:relative;overflow:hidden;color:#eef5ff;border:2px solid #244b88;background:radial-gradient(circle at 50% 72%,rgba(38,117,213,.22),transparent 38%),linear-gradient(180deg,#0b1734,#040914)}.globe-game-release::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle,#fff 0 1px,transparent 1.4px);background-size:91px 91px;opacity:.26}.globe-game-release>*{position:relative}.globe-game-release .eyebrow{color:#ffdc7a}.globe-game-release h2{max-width:880px;margin:10px 0;color:#fff8e8;font-size:clamp(38px,7vw,72px);line-height:.94}.globe-game-release p{max-width:780px;color:#becce6}.globe-preview{display:grid;grid-template-columns:minmax(240px,1fr) minmax(260px,1fr);gap:24px;align-items:center;margin-top:24px}.mini-globe{position:relative;width:min(100%,430px);aspect-ratio:1;margin:auto;border-radius:50%;background:radial-gradient(circle at 30% 24%,#81d5ff 0 4%,#1e82d0 28%,#09569f 58%,#031c43 100%);box-shadow:inset -42px -20px 70px rgba(0,0,0,.58),0 0 48px rgba(62,154,255,.52);border:2px solid rgba(186,230,255,.65);overflow:hidden}.mini-globe::before{content:"";position:absolute;inset:12% 12% 18% 7%;background:#74ad4c;clip-path:polygon(4% 20%,18% 2%,34% 9%,42% 26%,34% 42%,27% 61%,18% 58%,10% 43%,0 39%,46% 25%,56% 9%,70% 12%,79% 27%,71% 38%,60% 39%,49% 30%,57% 45%,68% 43%,78% 55%,75% 77%,64% 92%,56% 70%,50% 52%,82% 18%,95% 10%,100% 28%,92% 47%,82% 52%,90% 67%,100% 74%,94% 88%,80% 91%,75% 75%,61% 66%)}.mini-globe::after{content:"";position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 27% 18%,rgba(255,255,255,.34),transparent 26%),radial-gradient(circle at 70% 75%,transparent 46%,rgba(0,0,0,.45) 82%)}.globe-dot{position:absolute;z-index:2;width:18px;height:18px;border-radius:50%;background:#f0bb45;box-shadow:0 0 0 5px rgba(240,187,69,.18),0 0 18px #f0bb45}.globe-dot:nth-child(1){left:24%;top:32%}.globe-dot:nth-child(2){left:35%;top:66%}.globe-dot:nth-child(3){left:51%;top:28%}.globe-dot:nth-child(4){left:54%;top:56%}.globe-dot:nth-child(5){left:73%;top:35%}.globe-dot:nth-child(6){left:79%;top:70%}.game-copy{display:grid;gap:12px}.game-copy article{padding:15px;border:1px solid rgba(255,255,255,.13);border-radius:16px;background:rgba(255,255,255,.045);color:#c6d3e9}.game-copy strong{display:block;margin-bottom:4px;color:#fff8e8}.game-cta{display:inline-flex;justify-content:center;align-items:center;margin-top:8px;padding:15px 22px;border-radius:999px;background:#f0bb45;color:#17110a;text-decoration:none;font-weight:950;letter-spacing:.03em}.game-cta:hover{filter:brightness(1.07);transform:translateY(-1px)}
.comic-release{border:2px solid #493a8a;background:#f6f3ff}.comic-release figure{margin:22px 0 0}.comic-release img{display:block;width:min(100%,860px);height:auto;margin:0 auto;border:3px solid #2b244d;border-radius:18px;background:#f8efd7;box-shadow:0 20px 55px rgba(43,36,77,.18)}.comic-release figcaption{max-width:860px;margin:12px auto 0;color:var(--muted)}
@media(max-width:720px){.globe-preview{grid-template-columns:1fr}.mini-globe{width:min(88vw,400px)}}
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
    <article><strong>Передача ИИ</strong>Структурированный handoff сохраняет подтверждённые факты и неизвестные.</article>
  </div>
  <div class="companion-actions"><a class="companion-cta" href="companion/">Открыть живую партию →</a><a class="companion-secondary" href="ru/instructions/">Инструкция для ИИ-агента →</a></div>
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
  <div class="heat-grid"><article><strong>18–24°C</strong><br>спокойный режим</article><article><strong>25–27°C</strong><br>проверка с 6 часов</article><article><strong>28–30°C</strong><br>только тень, проверка с 4 часов</article><article><strong>31°C+</strong><br>переставить в прохладу</article></div>
  <div class="heat-danger"><strong>Сейчас:</strong> убрать банку с солнца, прикрыть чистой тканью или неплотной крышкой и измерить температуру жидкости.</div>
</section>

<section class="globe-game-release" id="globe-game">
  <div class="eyebrow">КВАССИСТЕНТ · Версия 14 · настоящая игра на сфере</div>
  <h2>Глобус вместо плоской карты</h2>
  <p>Шесть континентов закреплены прямо на объёмной сфере. Бутылки-ракеты стартуют наружу каждые 10 секунд или по нажатию, а общий и континентальные счётчики локально сохраняются в браузере.</p>
  <div class="globe-preview">
    <div class="mini-globe" aria-hidden="true"><i class="globe-dot"></i><i class="globe-dot"></i><i class="globe-dot"></i><i class="globe-dot"></i><i class="globe-dot"></i><i class="globe-dot"></i></div>
    <div class="game-copy">
      <article><strong>6 точек на сфере</strong>Северная Америка, Южная Америка, Европа, Африка, Азия и Океания.</article>
      <article><strong>Автопуск: 10 секунд</strong>Следующая площадка выбирается по кругу; любую точку можно запускать вручную.</article>
      <article><strong>Локальное накопление</strong>Общий счёт и статистика каждого континента остаются на устройстве.</article>
      <article><strong>Максимум газиков без разгона алкоголя</strong>В игре — полный индикатор; в реальном рецепте — короткая ПЭТ-карбонизация и быстрый холод.</article>
      <a class="game-cta" href="companion/game/">ИГРАТЬ НА ГЛОБУСЕ →</a>
    </div>
  </div>
</section>

<section class="comic-release" id="comic-guide">
  <div class="eyebrow">Версия {version} · визуальная инструкция</div>
  <h2>Реальная партия — в простом комиксе</h2>
  <p>В версии 14 глобальная механика окончательно перенесена на сферу: шесть точек запуска находятся прямо на глобусе.</p>
  <figure><a href="assets/{comic_name}"><img src="assets/{comic_name}" alt="КВАССИСТЕНТ 14: глобус, шесть континентов и бутылки-ракеты" loading="lazy"></a><figcaption>Векторный постер версии 14 и отдельная интерактивная игра доступны прямо на сайте.</figcaption></figure>
</section>
"""
    text = text.replace(marker, section + marker, 1)
    landing.write_text(text, encoding="utf-8")


def verify(version: str) -> None:
    root = ROOT / f"dist/site/v{version}"
    landing = root / "index.html"
    comic = root / f"assets/kvassistent-{version}-comic.svg"
    companion = root / "companion"
    game = companion / "game/index.html"
    feedback = root / "feedback"
    text = landing.read_text(encoding="utf-8")
    required = [
        'id="live-batch"', 'href="companion/"', "Один ИИ-агент — одна понятная партия кваса",
        'href="ru/instructions/"', "Простой рецепт", 'id="hot-fermentation"',
        'id="globe-game"', 'href="companion/game/"', "Глобус вместо плоской карты",
        "Автопуск: 10 секунд", "Локальное накопление", "6 точек на сфере",
        'id="comic-guide"', f"kvassistent-{version}-comic.svg", "Реальная партия — в простом комиксе",
        'id="community-feedback"', 'href="feedback/"', "kvassitent@gmail.com",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Landing page misses release content: {missing}")
    if not comic.is_file() or comic.stat().st_size < 1000:
        raise RuntimeError(f"Comic asset was not copied: {comic}")
    if not game.is_file() or game.stat().st_size < 4000:
        raise RuntimeError(f"Globe game is missing or too small: {game}")
    game_text = game.read_text(encoding="utf-8")
    game_required = ["КВАССИСТЕНТ 14", "10 сек", "Сфера, а не плоская карта"]
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
    core = load_core()
    core.main()
    install_comic(version)
    install_companion(version)
    install_feedback(version)
    patch_landing(version)
    verify(version)
    print(f"Built КВАССИСТЕНТ {meta['display']} with the version-14 spherical globe game")


if __name__ == "__main__":
    main()
