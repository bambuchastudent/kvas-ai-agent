# KVASSISTENT project goal

## Product goal

KVASSISTENT is human-first AI for manual craft.

The person performs the physical work: prepares bread, water and starter, observes the batch, smells it, tastes it and decides what actually happened. AI keeps the batch state, explains risk, asks for evidence and proposes one next action without pretending it can see, smell or taste the kvass.

The product is not an automatic brewing machine. It is a local-first companion for real human work.

## Identity that must not be erased

Read [`HUMAN_MANIFESTO.md`](HUMAN_MANIFESTO.md) before changing the landing page, Devpost copy, project identity or release presentation.

The creator-written mixed Russian/English text is canonical and must stay verbatim. Polished explanations and translations belong beside it, never instead of it.

## Current user experience goals

- A person can understand the project on a phone without fighting the interface.
- Choosing a language performs an obvious action immediately.
- The sticky menu becomes compact while scrolling and can be expanded again.
- `/`, `/game/`, `/companion/`, `/feedback/` and `/telegram/` always point to the latest release.
- `/v<version>/` remains immutable.
- The Telegram path provides real feedback delivery once secrets are configured.
- The repository itself gives every coding agent enough context to plan, check and explain its work.

## Agent operating rules

Before editing, an agent must state:

1. the user-visible goal;
2. the repository context it read;
3. the files it expects to change;
4. the checks it will run;
5. any secret or deployment dependency it cannot complete itself.

Do not commit release work directly to `develop`. Use a branch and pull request, wait for CI, fix failures in the same branch, and merge only when the verified publication build is green.

## Release protocol

1. Change only `release/version.json` to the next append-one version.
2. Run `python scripts/prepare-release.py`.
3. Run the companion and localization tests.
4. Run `python scripts/build-release.py`.
5. Run `python scripts/enhance-release.py`; the release finalizer is attached by preparation.
6. Verify immutable and latest paths, all PDFs, the game, companion, human manifesto, mobile navigation, agent context and Telegram artifacts.
7. Publish one verified artifact to the GitHub Release and `gh-pages`.
8. Verify Cloudflare Pages after publication.

Every release appends one `.1` segment. `ones_count` must equal the number of version segments equal to `1`.

## Telegram deployment boundary

The code may be public. These values may not be committed, pasted into issues or PRs, included in screenshots or printed in logs:

- `TELEGRAM_BOT_TOKEN`;
- `TELEGRAM_WEBHOOK_SECRET`;
- `TELEGRAM_OWNER_CHAT_ID`;
- `TELEGRAM_ADMIN_SECRET`.

A release can publish the Worker and feedback form without these values, but the bot is not considered operational until the Cloudflare environment variables exist and `/api/telegram/admin/setup` completes successfully.

## Definition of done for a user-facing change

A change is complete only when:

- the user-visible problem is reproducible before the fix and absent afterward;
- mobile and desktop behavior are considered;
- human-authored content remains intact;
- no secret enters the repository;
- CI verifies the generated artifact rather than only source files;
- the final response states what is live, what is merely prepared and what still requires a human-owned credential.
