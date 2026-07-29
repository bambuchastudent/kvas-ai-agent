# Claude Code contract for KVASSISTENT

Read these files before changing the project:

1. `AGENTS.md`
2. `AI_CHANGELOG.md`
3. `AI_AGENT_START.md`
4. `HUMAN_MANIFESTO.md`
5. `release/version.json`

## Non-negotiable creator rule

`HUMAN_MANIFESTO.md` is canonical human-authored material. Preserve it verbatim, including mixed Russian/English language, capitalization, humour, spelling, and the line mentioning Codex, Gemini, and Claude.

Professional copy, explanations, and translations may appear beside the manifesto, but never replace, silently correct, shorten, or hide it.

## Product idea

KVASSISTENT is human-first AI for manual craft. The person performs the physical work and provides observations. AI remembers state, explains risk, and requests evidence without claiming to see, smell, taste, or verify the batch.

## Mandatory change log

Every code, documentation, configuration, workflow, generated-artifact, release, fix, or rollback change must update `AI_CHANGELOG.md` in the same commit or pull request. Add the newest entry first and include the reason, observable behavior, affected files and systems, completed verification, deployment state, and remaining work. Reread the entry after tests and make sure it matches the actual diff. Never include secrets or vague claims.

## Releases

- Every release appends one `.1` segment.
- `ones_count` equals the number of version segments equal to `1`.
- `/` and short feature URLs point to the latest release.
- `/v<version>/` remains immutable.
- Never commit Telegram tokens or webhook secrets.
- A release is incomplete until `AI_CHANGELOG.md` records its final verification and publication state.

Before validating a release, run:

```bash
python scripts/prepare-release.py
python -m py_compile scripts/build-release.py scripts/prepare-release.py scripts/enhance-release.py
node scripts/test-companion.mjs
node scripts/test-localization.mjs
python scripts/build-release.py
python scripts/enhance-release.py
```

Verify the root, immutable release, `/game/`, `/companion/`, `/feedback/`, `/telegram/`, and `latest-version.json`.
