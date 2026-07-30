# AI-readable change log

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
- **Behavior** — what a user or operator will notice; write `no user-visible change` when applicable;
- **Files and systems** — important files, workflows, services, URLs, or repositories affected;
- **Verification** — tests, CI, builds, live checks, or manual checks actually completed;
- **Deployment** — published, merged but not published, local only, or not applicable;
- **Remaining work** — known limitations, follow-ups, or `none`.

Do not write vague entries such as “updated files” or “fixed things.” Do not include tokens, passwords, private chat identifiers, access keys, webhook secrets, or other credentials.

---

## 2026-07-30 — KVASSISTENT website release 24

- **Version or scope:** release 24, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** replaced the homepage language redirect with six prominent inline buttons for Russian, English, Spanish, German, Simplified Chinese and Greek; embedded the built localized summaries into the homepage; switching replaces the visible content in place, keeps the root URL unchanged and remembers the choice locally; updated the release number, immutable URL, Telegram page, safety marker and build assertions.
- **Why:** language switching on the main demo page had to be obvious and must not navigate visitors to separate localization pages.
- **Behavior:** pressing RU, EN, ES, DE, 中文 or EL immediately changes the homepage content without loading a new page or changing the address; the selector stays visible and the chosen language is restored on the next visit.
- **Files and systems:** `release/version.json`, `scripts/finalize-release.py`, generated root and immutable version-24 homepage, six localized summary pages, Telegram page and release notes.
- **Verification:** source finalizer asserts all six controls, embedded localization payloads, local persistence, absence of `window.location.assign`, exact 24-part version and release-25 Telegram wording; full publication CI and live Cloudflare verification remain for the PR and merge workflow.
- **Deployment:** not yet published at the time of this entry.
- **Remaining work:** merge only after green publication CI, then verify the production root and immutable version 24 switch languages in place and the backend reports release 24.

## 2026-07-29 — KVASSISTENT 23 Add Drink form completion

- **Version or scope:** release 23 completion; version stays `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** restored a real form at `/feedback/` with author, contact, drink name, recipe/result description, optional photo URL, honeypot, accessible status messages, single-submit guard, and Telegram fallback; the form posts to the existing AWS backend and states that accepted drinks become release-24 tasks; updated release notes and form styles.
- **Why:** the release-23 feedback PR received a later valid request to fix the form for adding a drink; the already published page only linked to Telegram and therefore did not implement that wish.
- **Behavior:** visitors can submit a drink without opening Telegram; the button cannot fire concurrent duplicate requests; direct photo file upload remains available through `@kvassistent_bot`, while the web form accepts an optional public photo URL.
- **Files and systems:** `feedback/index.html`, `feedback/styles.css`, version-23 release notes, AWS feedback endpoint in the companion backend repository, generated latest and immutable version-23 website routes.
- **Verification:** publication CI and live generated-page verification completed successfully.
- **Deployment:** published.
- **Remaining work:** none.

## 2026-07-29 — KVASSISTENT website release 23

- **Version or scope:** release 23, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** clarified both filtering steps in Russian and English source guides using clean gauze, a folded bandage, or a food-grade filter bag; added a version 23 poster and release notes; added `touch-action: manipulation` to generated interactive elements; removed flickering flame and star animations; slowed decorative orbits, stopped them on mobile, and fully disabled motion under `prefers-reduced-motion`; debounced the compact-menu button; updated the Telegram page with release 23 filtering and feedback behavior.
- **Why:** implement the accumulated release-23 wishes: explain exactly how to strain the wort, prevent seizure-like flashing, and stop double-tap zoom when users repeatedly press buttons without disabling ordinary pinch zoom.
- **Behavior:** the site is calmer by default, respects reduced-motion preferences, keeps normal page zoom available, and no longer zooms from rapid double taps on controls; recipe pages and Telegram use the same explicit filtering guidance.
- **Files and systems:** `release/version.json`, `scripts/finalize-release.py`, Russian and English publication sources, version 23 comic and release notes, generated latest/immutable website routes, Telegram page, game, companion, and feedback pages.
- **Verification:** publication PR CI completed successfully; the `gh-pages` branch, version-23 tag, latest metadata, immutable manifest, touch rules, reduced-motion rules and Telegram page were verified after merge.
- **Deployment:** published.
- **Remaining work:** none.

## 2026-07-29 — AI change-log contract

- **Version or scope:** unreleased repository rule; current product release remains version 22 at the time of this historical entry.
- **Changed:** created `AI_CHANGELOG.md` and made it a mandatory part of every future change and release.
- **Why:** the project must always leave a concise, understandable handoff that another AI agent can read before continuing work.
- **Behavior:** no user-visible product change.
- **Files and systems:** `AI_CHANGELOG.md`, AI-agent instruction files in the website repository, and the companion Telegram-bot repository contract.
- **Verification:** checked that the required fields cover intent, implementation, validation, deployment, and remaining work.
- **Deployment:** documentation-only repository update; no website or Lambda deployment required.
- **Remaining work:** every future commit or PR must add its own newest entry above this one.
