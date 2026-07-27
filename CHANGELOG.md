# Changelog

## 1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1

- Preserved the creator-authored mixed-language manifesto verbatim in `HUMAN_MANIFESTO.md` and placed the professional explanation beside it rather than replacing it.
- Added a cosmic landing-page treatment with stars, orbit lines, animated kvass bottle satellites, and reduced-motion support.
- Added a version-17 cosmic SVG poster built around **ЭТО ТВОЙ КВАС**, **HUMAN-AUTHORED COMES FIRST**, and **HUMANS BREW. AI GUIDES.**
- Added a secure Telegram webhook-bot scaffold and `/telegram/` entry page without committing a bot token or webhook secret.
- Aligned Codex, Gemini, and Claude Code with the same human-content, release, safety, and secret-management contract.
- Added dynamic release preparation and post-build enhancement so version-specific game, cache, landing, and latest metadata no longer depend on hardcoded release 16 values.
- Consolidated duplicate website pipelines into one build whose verified artifact is reused for the GitHub Release and `gh-pages` publication.
- Extended release and Cloudflare verification to cover the manifesto, cosmic layer, Telegram entry, latest metadata, and immutable version 17 URL.

## 1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1

- Added stable latest URLs at `/`, `/game/`, `/companion/`, and `/feedback/`; these paths now publish the current release without requiring the long version path.
- Kept `/v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1/` as the immutable address for release 16.
- Changed the Russian version copy to `Версия 16, потому что в ней единиц вот столько: 16. Пересчитай: v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1` and linked the explicit version string.
- Changed the game heading to **Глобальная игра на сфере** and kept the flat-screen joke separate from the real spherical game concept.
- Added complete globe-game localization for Russian, English, Spanish, German, Simplified Chinese, and Greek.
- Declared Russian and English as canonical knowledge sources and aligned all 12 human/AI publication documents by sections, quantities, risks, alcohol language, and URLs.
- Made English the universal fallback for non-Russian interfaces; Russian is no longer used as static fallback text in Spanish, German, Chinese, or Greek views.
- Changed the universal Live Batch HTML shell to English so non-Russian locales never flash Russian copy before JavaScript applies the selected locale.
- Added deterministic localization checks, Russian-leak detection, and release-build validation for all short latest aliases.
- Refreshed the PWA cache and included localized game assets for offline use.

## 1.1.1.1.1.1.1.1.1.1.1.1.1.1.1

- Moved the spherical globe game to the very top of the public landing page.
- Added a sticky header with quick links to the game, all links, human guides, AI guides, live batch, feedback, gallery, and GitHub.
- Added a header language chooser with direct actions for the selected human guide and AI-agent guide.
- Added a dedicated **Все ссылки сразу** section that exposes all major entry points from one screen.
- Changed the main version copy to `Версия 15, потому что в ней единиц вот столько: 15`.
- Updated the standalone globe game page to version 15 so the release number matches the landing page.
- Extended release verification for the landing-first game position, the top navigation, the header language switcher, and the new version phrase.

## 1.1.1.1.1.1.1.1.1.1.1.1.1.1

- Replaced the flat launch board with a dedicated spherical globe game.
- Added a standalone `companion/game/` page with a glossy globe, six launch sites, and bottle rockets flying outward from the sphere.
- Added automatic launches every 10 seconds and manual launches from every continent marker.
- Added one persistent total counter plus six per-continent counters stored locally with `localStorage`.
- Added pause, reset, manual-launch, and optional sound controls.
- Updated the public landing page with a version-14 globe preview and a direct **Играть на глобусе** action.
- Preserved the maximum-carbonation-without-alcohol game mode while clarifying the real-drink safety interpretation.
- Added a new versioned spherical-globe SVG poster and release validation for the game assets.

## 1.1.1.1.1.1.1.1.1.1.1.1.1

- Added a six-continent launch board: North America, South America, Europe, Africa, Asia, and Oceania.
- Added automatic bottle-rocket launches every 10 seconds, rotating across all six continents.
- Added a persistent local counter labeled `Запущено бутылок`, stored with `localStorage` so launches accumulate on the same device.
- Added a local reset action that clears the stored counter but keeps the timed launch system running.
- Added a dedicated release block for **maximum carbonation without alcohol**, emphasizing short PET carbonation, fast checks, and immediate chilling.
- Updated the versioned comic to show the six global launch points, local accumulation, and the no-alcohol max-carbonation path.
- Extended release verification so the build now requires six continents, the 10-second cadence text, local accumulation, and the no-alcohol carbonation block.

## 1.1.1.1.1.1.1.1.1.1.1.1

- Added a dedicated interactive launch pad with three clickable bottle rockets.
- Made each bottle fly in its own direction: left, upward, or right.
- Added a small corner counter labeled `Запущено бутылок`, increasing from 0 to 3 as launches happen.
- Counted each bottle only once until the user presses the reset button.
- Added a reset action so all bottle launches can be replayed in the same session.
- Updated the versioned comic to match the separate launch directions and counter behavior.
- Extended release verification so the build now requires the launch counter and all three directional rockets.

## 1.1.1.1.1.1.1.1.1.1

- Added a dedicated community feedback form for drink stories, recipes, photos, ideas, and bug reports.
- Routed submissions to `kvassitent@gmail.com` through FormSubmit with explicit data-transfer consent and a direct-email fallback.
- Prepared Instagram and TikTok channel links under the shared `@kvassistent` identity.
- Connected feedback and social entry points from both the public landing page and the installed PWA.
- Bumped the PWA cache generation so installed clients discover the new community links.

## 1.1.1.1.1.1.1.1.1

- Made language resolution deterministic: a saved choice wins, then the closest supported device language, then English.
- Added a multilingual privacy notice with full and essential-only consent choices.
- Added the celebratory cookie-and-kvass animation for both consent paths, including reduced-motion behavior.
- Reworked the service worker so installed PWAs receive fresh navigations, activate new releases immediately, and retain an offline fallback.
- Added 192 px and 512 px install icons plus stronger web-app manifest metadata.
- Expanded automated checks for language preference, consent, PWA assets, and the live Cloudflare deployment.
- Added Greek to the companion and made Simplified Chinese the target for Chinese device locales.
- Added Greek human and AI-agent publication pages plus both versioned PDFs to the main language gallery.
- Added an explicit, privacy-preserving nearby-café map search for finding kvass outside the home.

## 1.1.1.1.1.1.1.1

- Added **Live Batch**, a mobile-first consumer PWA for daily household fermentation check-ins.
- Added a deterministic, tested safety engine for temperature, direct sunlight, closure, surface, smell, taste, and extended warm fermentation.
- Added personal next-check timing, batch progress, local history, and a theoretical alcohol ceiling based on added sugar.
- Added a one-tap 28°C demo scenario and structured AI handoff with explicit unknowns and safety flags.
- Added local-first persistence, offline caching, installable metadata, JSON export, and Web Share support.
- Added interface support for Russian, English, Spanish, German, and Simplified Chinese.
- Integrated the PWA and its rule tests into the multilingual release build and CI verification.

## 1.1.1.1.1.1.1

- Added a versioned Serena configuration for Python and Bash symbol-aware navigation and editing.
- Registered Serena as a Codex MCP server and added repeatable setup and health checks.
- Connected Graphify to Codex and Git hooks for repository knowledge-graph updates.
- Added `AGENTS.md` guidance explaining when agents should use Graphify, Serena, or built-in tools.
- Made the next-version script carry the versioned comic asset and manifest reference forward automatically.
- Preserved the heat/sunlight research, multilingual publication, and comic guide from version 6.

## 1.1.1.1

- Changed the hero to **ТВОЙ ЛИЧНЫЙ КВАССИСТЕНТ**.
- Made the roles explicit above the fold: AI manages the batch, the person performs the physical steps, and the result is homemade kvass **Жижа**.
- Added a persistent brand contract and release checklist for future changes.
- Localized every human and AI-agent language card, including descriptions and action buttons, in Russian, English, Spanish, German, and Simplified Chinese.
- Added `lang` attributes to language cards and CI checks for all localized buttons.
- Fixed Cyrillic rendering in the locally generated social card on macOS.
- Added a local Python launcher that reuses `.venv` when available.

## 1.1.1

- Renamed the visible product identity to **КВАССИСТЕНТ** in uppercase.
- Reworked the landing page so the best concise instructions for people appear first.
- Split the landing page into separate **Для людей** and **Для ИИ-агентов** sections.
- Kept human summaries and AI-agent instructions as separate multilingual PDF and web documents.
- Added canonical release metadata in `release/version.json`.
- Added the append-one version rule: `1.1.1`, `1.1.1.1`, `1.1.1.1.1`, and so on.
- Added `ones_count`, displayed as `единиц: 3` for version 1.1.1.
- Added `scripts/next-ones-version.py` for generating the next custom release version.
- Made publication and live-verification workflows read the canonical version metadata.
- Added homepage validation for uppercase branding, human-first instructions, audience separation, and the unit counter.

## 1.1.0

- Added an animated golden beer-style background with rising bubbles to the landing page.
- Added `prefers-reduced-motion` support for the background animation.
- Added a data-driven gallery section for real successful community drinks.
- Added an honest empty state and contribution links instead of placeholder success stories.
- Added `gallery/drinks.json` and documentation for submitting a drink.
- Removed the obsolete optional GitHub Pages deployment job; Cloudflare Pages remains the verified publication target.
