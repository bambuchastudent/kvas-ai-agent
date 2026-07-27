# Gemini project contract for KVASSISTENT

Start with `AGENTS.md`, `AI_AGENT_START.md`, `HUMAN_MANIFESTO.md`, and `release/version.json`.

## Preserve the human voice

`HUMAN_MANIFESTO.md` is the creator's canonical text. It must remain verbatim, including mixed Russian and English, humour, spelling, capitalisation, and references to AI tools.

You may add a translation, explanation, summary, or polished presentation beside the original. Never replace, silently correct, shorten, reorder, or hide the original human text.

## Product principle

KVASSISTENT demonstrates human-first AI for manual work. A person performs the real physical process and reports observations. AI provides memory, structure, explanations, and safety boundaries without inventing sensory evidence.

## Release contract

- Append one `.1` for each release.
- Keep `ones_count` aligned with the version.
- Root and short feature paths are mutable aliases to latest.
- `/v<version>/` is immutable.
- Keep Telegram credentials exclusively in deployment secrets.

Use this validation order:

```bash
python scripts/prepare-release.py
python -m py_compile scripts/build-release.py scripts/prepare-release.py scripts/enhance-release.py
node scripts/test-companion.mjs
node scripts/test-localization.mjs
python scripts/build-release.py
python scripts/enhance-release.py
```

Check `/`, the immutable release, `/game/`, `/companion/`, `/feedback/`, `/telegram/`, and `latest-version.json` before declaring the release complete.
