# AI-readable change log

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

## 2026-07-29 — KVASSISTENT website release 23

- **Version or scope:** release 23, `v1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1`.
- **Changed:** clarified both filtering steps in Russian and English source guides using clean gauze, a folded bandage, or a food-grade filter bag; added a version 23 poster and release notes; added `touch-action: manipulation` to generated interactive elements; removed flickering flame and star animations; slowed decorative orbits, stops them on mobile, and fully disables motion under `prefers-reduced-motion`; debounced the compact-menu button; updated the Telegram page with release 23 filtering and feedback behavior.
- **Why:** implement every accumulated release-23 wish: explain exactly how to strain the wort, prevent seizure-like flashing, and stop double-tap zoom when users repeatedly press buttons without disabling ordinary pinch zoom.
- **Behavior:** the site is calmer by default, respects reduced-motion preferences, keeps normal page zoom available, and no longer zooms from rapid double taps on controls; recipe pages and Telegram use the same explicit filtering guidance.
- **Files and systems:** `release/version.json`, `scripts/finalize-release.py`, Russian and English publication sources, version 23 comic and release notes, generated latest/immutable website routes, Telegram page, game, companion, and feedback pages.
- **Verification:** Python syntax check for the finalizer completed locally. Full publication build, localization checks, artifact checks, Cloudflare Pages publication, and live URL verification remain to be completed by the release PR workflows.
- **Deployment:** not yet published at the time of this entry.
- **Remaining work:** open the release PR, require green publication checks, merge, verify the root and immutable version 23 URLs, then update deployment status if necessary.

## 2026-07-29 — AI change-log contract

- **Version or scope:** unreleased repository rule; current product release remains version 22.
- **Changed:** created `AI_CHANGELOG.md` and made it a mandatory part of every future change and release.
- **Why:** the project must always leave a concise, understandable handoff that another AI agent can read before continuing work.
- **Behavior:** no user-visible product change.
- **Files and systems:** `AI_CHANGELOG.md`, AI-agent instruction files in the website repository, and the companion Telegram-bot repository contract.
- **Verification:** checked that the required fields cover intent, implementation, validation, deployment, and remaining work.
- **Deployment:** documentation-only repository update; no website or Lambda deployment required.
- **Remaining work:** every future commit or PR must add its own newest entry above this one.
