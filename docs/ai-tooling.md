# Graphify + Serena

The repository uses two complementary AI-development tools:

- **Graphify** builds a persistent cross-file knowledge graph. Use it for repository-wide questions, documentation and manifest relationships, dependency paths, and impact analysis.
- **Serena** runs as an MCP server and adds symbol-aware navigation and editing. This project enables its Python and Bash language servers.

Generated Graphify output and Serena caches stay local. The portable configuration lives in `AGENTS.md`, `.serena/project.yml`, and the setup scripts.

## One-time setup

Requirements: Git, Codex, and [uv](https://docs.astral.sh/uv/).

```bash
npm run ai:setup
```

The command:

1. installs or updates `graphifyy` and `serena-agent`;
2. adds Graphify instructions and Codex/Git hooks;
3. registers Serena as a Codex MCP server with the `codex` context;
4. builds `graphify-out/graph.json` locally;
5. indexes the Serena project.

The script changes user-level Codex configuration in addition to repository-local files. Review it before running on managed machines.

## Daily use

```bash
npm run ai:check
npm run graph:update
graphify query "How is the release version propagated?"
graphify affected "release/version.json"
```

In Codex, ask Serena to activate the current directory if it has not activated automatically. Use Serena for symbols and references; use Graphify for broad relationships across code, recipes, translations, release metadata, and publication inputs.

## Files and generated data

- `AGENTS.md` — agent rules shared through Git.
- `.serena/project.yml` — shared Serena project settings.
- `.serena/project.local.yml` — optional local overrides; ignored by Git.
- `graphify-out/` — generated local graph; ignored by Git.
- `.codex/hooks.json` — machine-specific Graphify hook; ignored by Git.

## Official documentation

- [Graphify AI coding tools](https://graphify.net/ai-coding-tools/)
- [Serena repository](https://github.com/oraios/serena)
- [Serena: Codex connection](https://oraios.github.io/serena/02-usage/030_clients.html#codex-cli-and-app)
- [Serena project workflow](https://oraios.github.io/serena/02-usage/040_workflow.html)
