## Shared AI contract: Codex, GitHub Copilot coding agent, Gemini, and Claude Code

Read in this order before planning repository changes:

1. [`PROJECT_GOAL.md`](PROJECT_GOAL.md) — product goal, current UX priorities, deployment boundaries, and definition of done.
2. [`HUMAN_MANIFESTO.md`](HUMAN_MANIFESTO.md) — canonical creator-authored identity.
3. This `AGENTS.md` — shared repository and tool rules.
4. [`.github/copilot-instructions.md`](.github/copilot-instructions.md) when the work is performed by GitHub Copilot coding agent.

Before editing, state the user-visible goal, context read, files expected to change, checks to run, and any external credential or deployment step that remains owner-controlled.

The manifesto is canonical human-authored content. Preserve it verbatim, including mixed Russian/English language, capitalization, humour, spelling, and references to AI tools. A translation or polished explanation may be placed beside it, never instead of it. Do not silently correct, shorten, reorder, hide, or delete it.

KVASSISTENT is human-first AI for manual craft: the person performs the physical work and reports observations; AI remembers state, explains risks, requests evidence, and refuses to invent sensory facts.

Release rules:
- Never commit release work directly to `develop`; use a branch and pull request.
- Every release appends one `.1` segment.
- `ones_count` must match the version.
- `/` and short feature URLs point to latest.
- `/v<version>/` remains immutable.
- Telegram tokens, owner chat IDs, admin secrets, and webhook secrets must never enter the repository, issues, PRs, screenshots, or logs.
- Before release validation run `python scripts/prepare-release.py`; after `python scripts/build-release.py`, run `python scripts/enhance-release.py`.
- Merge only after the generated publication artifact is green in CI.

Tool-specific companion files: [`CLAUDE.md`](CLAUDE.md), [`GEMINI.md`](GEMINI.md), and [`.github/copilot-instructions.md`](.github/copilot-instructions.md). Codex follows this `AGENTS.md` directly.

## KVASSISTENT kitchen-agent entry point

If the user asks for help making, checking, or rescuing kvass rather than changing this repository, read [`AI_AGENT_START.md`](AI_AGENT_START.md) before responding. Follow its one-batch, confirmation-first, safety-first protocol.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Serena

This project has a versioned Serena configuration at `.serena/project.yml`.

Rules:
- Activate `kvas-ai-agent` with Serena before symbol-level code exploration or refactoring.
- Prefer Serena's symbol tools for Python and Bash definitions, references, and cross-file edits.
- Use Graphify for broad repository questions, documentation relationships, manifests, and impact paths across file formats.
- Use built-in file and shell tools for small text edits, generated artifacts, and non-code documents.
- After changing Python or Bash, let Serena refresh its index and run `graphify update .` before handoff.

## Tool setup

Run `npm run ai:setup` once per machine. It installs both CLIs, registers Serena as a Codex MCP server, installs Graphify hooks, creates the local graph, and indexes the Serena project.

Run `npm run ai:check` to verify the repository integration without changing it.
