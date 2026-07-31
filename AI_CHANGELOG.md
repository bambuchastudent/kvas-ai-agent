# AI-readable change log

## 2026-07-31 — KVASSISTENT website release 29 clickable carbonation craft

- **Version or scope:** release 29, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`; next release 30.
- **Changed:** made the entire game globe clickable; added nearest-continent selection, keyboard launch, safe local-state recovery and a pure game-state module; replaced the fire rocket with an inverted kvass bottle whose cap unscrews, whose neck emits carbonation bubbles, and whose toilet-paper rolls unfold as wings; synchronized six languages and release metadata.
- **Why:** the globe looked interactive but tapping the sphere did nothing unless the user hit a small continent marker. The previous rocket also contradicted the product joke: KVASSISTENT should fly on carbonation, not fire.
- **Behavior:** tapping anywhere on the sphere launches from the nearest site; Enter or Space launches the next site; the bottle flies bottom-first with the neck trailing, bubble exhaust and paper wings; the game frames the real drink as a non-alcoholic target up to 0.5% ABV and does not claim an exact value without measurement.
- **Files and systems:** `companion/game/index.html`, `game.js`, `game-state.js`, `styles.css`, `i18n.js`, `scripts/test-game.mjs`, fast and full GitHub Actions workflows, release metadata, feedback page, publication manifest, gallery metadata, README and release notes.
- **Verification:** deterministic Node tests cover all six launch sites, countdown behavior, nearest-site selection and static interaction/animation contracts; PR CI runs the source tests, while the merge-only workflow repeats them against the generated immutable game and performs live marker checks after deployment.
- **Deployment:** proposed on branch `agent/release-v29-clickable-gas-craft`; publish after paired backend release 29 is green and merged.
- **Remaining work:** complete CI, merge both repositories, then manually tap the production sphere on a phone to confirm the visual timing and hit area feel right.

---

## 2026-07-30 — KVASSISTENT website release 28 results and stories

- **Version or scope:** release 28, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`; next release 29.
- **Changed:** replaced the stale Version 23 web form with a one-field result flow; added optional photo/video URL, local 1080×1920 story generation and a publication rail; synchronized every game title, description and language label with Version 28; expanded release preparation and CI guards; added `V2_PLAN.md`.
- **Why:** users should be able to show a real result without filling a long form, and published photos/video need a clear route into stories and a future gallery. The previous release still exposed numbers 16, 20, 23 and 24 in public surfaces.
- **Behavior:** a result requires only a short description; optional identity and media fields stay collapsed; the story maker keeps the photo in the browser and exports or shares a PNG; game localization cannot ship with stale numbers; exact URLs for the two already published photos are intentionally not invented and remain a Version 29 data task.
- **Files and systems:** `feedback/`, `feedback/stories/`, game i18n, release preparation, version consistency checks, release metadata, gallery publication entry points, README, release notes, package metadata and v2 roadmap.
- **Verification:** fast CI checks exact 28-unit metadata, form markers, story canvas/share markers, all six game labels and absence of known stale version strings; merge-only publication must build, deploy and live-check website release 28 against backend release 28.
- **Deployment:** merge to `develop` publishes Version 28 after the paired backend PR is green and merged.
- **Remaining work:** add direct public URLs for the two photos and one video as real gallery records; do not create fictional links.

---

## 2026-07-30 — KVASSISTENT website release 27 stable sticky menu

- **Version or scope:** release 27, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`; next release 28.
- **Changed:** stabilized the sticky homepage menu with separate enter/leave scroll thresholds, one `requestAnimationFrame` update per frame, state-change-only class updates, disabled geometry transitions, and compositor-safe rendering markers; added release metadata and notes.
- **Why:** the mobile menu visibly flashed because one `scrollY > 120` threshold could toggle repeatedly while the header itself changed height during scrolling.
- **Behavior:** the menu enters compact mode after 180 px and leaves it only above 72 px; scrolling near one threshold no longer causes rapid compact/expanded oscillation.
- **Files and systems:** `scripts/stabilize-sticky-menu.py`, generated root and immutable homepages, canonicalizer hook, `release/version.json`, README, release notes, backend status synchronization and this changelog.
- **Verification:** fast PR checks compile all scripts and validate version/localization contracts; the post-merge publication build must verify both generated homepages contain the hysteresis, rAF and no-transition markers, then live-check site and backend release 27.
- **Deployment:** merge to `develop` publishes website release 27 after backend release 27 is live.
- **Remaining work:** complete PR CI, merge, and verify the production menu on a mobile browser.

---

## 2026-07-30 — Fast pull-request and merge-only release pipeline

- **Version or scope:** release engineering after Version 26; product version remains 26.
- **Changed:** split pull-request validation from full publication; PRs now run Python compilation, version-contract checks and Node localization/companion tests only; the 12 PDFs, fonts, archives, GitHub Release, `gh-pages` publication and live Cloudflare/AWS verification run only after a merge to `develop`; removed completed release-25 and release-26 migration workflows and their obsolete one-off scripts.
- **Why:** the previous workflow installed fonts and PDF dependencies and rebuilt every publication artifact after each small PR commit, causing repeated minute-long runs and making a multi-fix release take close to an hour.
- **Behavior:** contributors receive fast feedback without waiting for PDF generation; one full release build still runs after merge and retains canonical-version, immutable-URL, Telegram and backend verification.
- **Files and systems:** `.github/workflows/version-consistency.yml`, new `.github/workflows/release.yml`, removed `.github/workflows/publish.yml`, release-specific workflows and migration scripts, GitHub Actions, GitHub Releases, `gh-pages` and Cloudflare Pages.
- **Verification:** the first clean fast PR run passed all version, Python, Companion and localization checks; its test commands completed in about 0.8 seconds and the complete GitHub job, including runner setup and cleanup, completed in about 4.5 seconds. The merge-only workflow remains responsible for building 12 PDFs, validating the site, publishing `gh-pages`, and checking production against the backend.
- **Deployment:** merged to `develop` in PR 28. This documentation-only status correction uses `[skip ci]` so it does not start a second publication build.
- **Remaining work:** observe the first merge-only release run; consider a prebuilt publication container only if that single post-merge build remains too slow.

---

## 2026-07-30 — KVASSISTENT release 26 public discovery

- **Version or scope:** release 26 public-discovery completion.
- **Changed:** made the root URL canonical; marked immutable release archives `noindex,follow`; added complete Open Graph and Twitter cards with a real 1200×800 image; generated `robots.txt`, expanded `sitemap.xml`, `_headers`, `llms.txt`, and public About, How it works, FAQ, Press and Changelog pages.
- **Why:** search engines, link previews and AI systems need one stable official URL and an explicit machine-readable description instead of competing version paths.
- **Behavior:** ordinary visitors and crawlers discover the latest product at `https://kvassistent.pages.dev/`; historical `/v.../` pages remain accessible but do not compete in search results.
- **Verification:** publication fails unless canonical/noindex metadata, social image, public pages and discovery files are present.
- **Deployment:** included in the Version 26 publication pipeline.
- **Remaining work:** after production deployment, submit the sitemap manually in Google Search Console and Bing Webmaster Tools.

---

## 2026-07-30 — KVASSISTENT website release 26

- **Version or scope:** release 26, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** normalized human, technical, next-release and immutable URL representations; replaced stale release-9 README links; made the homepage badge and Telegram wording dynamic; added strict URL-length validation.
- **Why:** the project mixed raw versions, `v`-prefixed versions, short `V25`, stale release-9 headings and shortened immutable URLs such as a 16-unit path.
- **Behavior:** users see `Версия 26`; technical links always use the exact 26-unit `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`; the unreleased successor is only `Версия 27`.
- **Files and systems:** `release/version.json`, `README.md`, `scripts/build-release.py`, `scripts/finalize-release.py`, `scripts/check-version-consistency.py`, release notes, publication CI and generated site.
- **Verification:** exact segment recount, regex validation of every current immutable URL, generator hardcode checks, Python compile and full publication workflow.
- **Deployment:** merge to `develop` publishes release 26.
- **Remaining work:** backend/Telegram repository must report release 26 and collect feedback for release 27 before final live verification.

---

## 2026-07-30 — KVASSISTENT website release 25

- **Version or scope:** release 25, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** put every non-Russian inline localization on a high-contrast light card; localized the complete sticky header for six languages; added a persistent `V25` badge; preserved single-page switching, current scroll position and local language preference; added release notes, demo pitch and poster.
- **Why:** the version-24 demo screenshot showed dark text on a dark space background, an untranslated Russian header and no visible version after switching languages.
- **Behavior:** RU, EN, ES, DE, 中文 and EL switch without navigation; both content and header change together; text stays readable; version remains visible while scrolling.
- **Files and systems:** release metadata, finalizer, publication workflow assertions, README, release notes, demo pitch, poster, generated latest and immutable site.
- **Verification:** migration assertions, Python compile, publication build, twelve PDFs, inline-language checks, contrast markers, localized-header markers, persistent badge checks and live Cloudflare verification.
- **Deployment:** merge to `develop` publishes version 25.
- **Remaining work:** none after green live verification.

---

This file is the chronological handoff for humans and AI agents working on KVASSISTENT.

## Mandatory rule

Every repository change must update this file in the **same commit or pull request**. Work is not complete until the new entry has been reread after tests and confirmed to match the actual diff and deployment state.

Keep the newest entry first. Write in clear, concrete language that another AI agent can continue from without reconstructing the whole conversation.

Each entry must contain:

- **Date** — `YYYY-MM-DD`;
- **Version or scope** — release number, full ones-version, or `unreleased`;
- **Changed** — exactly what was added, removed, or corrected;
- **Why** — the user-visible goal or reason;
- **Behavior** — what a person or system now experiences;
- **Files and systems** — affected repositories, paths, APIs, deployment targets or generated artifacts;
- **Verification** — tests, assertions, manual checks or deployment evidence;
- **Deployment** — whether it is proposed, merged, published or live;
- **Remaining work** — explicit follow-up, or `none`.
