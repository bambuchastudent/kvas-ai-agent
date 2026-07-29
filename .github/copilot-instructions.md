# GitHub Copilot coding-agent instructions for KVASSISTENT

Read these files before proposing changes:

1. [`PROJECT_GOAL.md`](../PROJECT_GOAL.md)
2. [`HUMAN_MANIFESTO.md`](../HUMAN_MANIFESTO.md)
3. [`AI_CHANGELOG.md`](../AI_CHANGELOG.md)
4. [`AGENTS.md`](../AGENTS.md)

The repository is the product contract. Preserve human-authored identity and report uncertainty honestly.

## Required first response

Before editing, summarize:

- **Goal** — the user-visible result;
- **Context read** — which canonical files and relevant code paths were inspected;
- **Plan** — files and steps;
- **Checks** — tests and generated-artifact verification;
- **Deployment boundary** — secrets, accounts or external actions that still require the owner.

Do not begin with a large rewrite when a focused fix is possible.

## Mandatory AI-readable change log

Every repository change must update [`AI_CHANGELOG.md`](../AI_CHANGELOG.md) in the same commit or pull request. The newest entry must explain what changed, why, user-visible behavior, affected files and systems, verification actually completed, deployment state, and remaining work. Use explicit `no user-visible change` or `none` where appropriate. Reread the entry after checks and make sure it matches the diff and live state. Never put secrets, private identifiers, or vague claims in the log.

## Branch and release discipline

- Never commit release work directly to `develop`.
- Create a branch and pull request.
- Keep fixes in the same PR until CI is green.
- Merge only after the publication artifact passes.
- For a new release, edit only `release/version.json`; preparation synchronizes generated metadata.
- A release is incomplete until `AI_CHANGELOG.md` records final checks and publication state.
- Run, in order:

```bash
python scripts/prepare-release.py
node scripts/test-companion.mjs
node scripts/test-localization.mjs
python scripts/build-release.py
python scripts/enhance-release.py
```

`prepare-release.py` attaches `scripts/finalize-release.py` to the enhancement step.

## Product invariants

- The person makes the kvass; AI guides, remembers and explains.
- Unknown sensory facts remain unknown.
- `HUMAN_MANIFESTO.md` remains verbatim and visible.
- `/`, `/game/`, `/companion/`, `/feedback/` and `/telegram/` point to latest.
- `/v<version>/` is immutable.
- All six localizations keep equivalent safety and quantity information.
- Missing non-Russian UI text falls back to English, never Russian.

## UI acceptance rules

For the landing page:

- changing `#header-language-select` must cause an immediate, obvious navigation to the chosen localized guide;
- a stored language value must not leave the selector showing one language while the visible page stays in another;
- on mobile, the sticky top bar must compact after scrolling;
- the compact bar must retain the brand, language selector and an accessible menu button;
- the menu button must expand the hidden navigation without requiring the user to scroll back to the top.

## Telegram acceptance rules

The generated site must contain working direct links to the deployed Telegram bot and describe its current capabilities accurately. The website must not claim that an obsolete form or worker is operational when the real bot is hosted elsewhere.

Never commit or print:

- `TELEGRAM_BOT_TOKEN`;
- `TELEGRAM_WEBHOOK_SECRET`;
- `TELEGRAM_OWNER_CHAT_ID`;
- `TELEGRAM_ADMIN_SECRET`.

A prepared integration without configured secrets is **prepared**, not **operational**. State that distinction in the PR, `AI_CHANGELOG.md`, and final report.

## Handoff format

When work is complete, report:

1. what changed;
2. what CI verified;
3. what was published;
4. what still requires a human-owned credential;
5. exact latest and immutable URLs;
6. confirmation that `AI_CHANGELOG.md` was updated and reread.
