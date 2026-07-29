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

## 2026-07-29 — AI change-log contract

- **Version or scope:** unreleased repository rule; current product release remains version 22.
- **Changed:** created `AI_CHANGELOG.md` and made it a mandatory part of every future change and release.
- **Why:** the project must always leave a concise, understandable handoff that another AI agent can read before continuing work.
- **Behavior:** no user-visible product change.
- **Files and systems:** `AI_CHANGELOG.md`, AI-agent instruction files in the website repository, and the companion Telegram-bot repository contract.
- **Verification:** checked that the required fields cover intent, implementation, validation, deployment, and remaining work.
- **Deployment:** documentation-only repository update; no website or Lambda deployment required.
- **Remaining work:** every future commit or PR must add its own newest entry above this one.
