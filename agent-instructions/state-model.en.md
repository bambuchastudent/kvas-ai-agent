# Kvass Agent State Model

This file is mandatory for AI agents using this project.

The agent must maintain an explicit state for the current batch. State is built only from facts confirmed by the user. Unknown values stay `null`; never replace them with guesses.

## Stages

Use one `stage` value:

- `planning`
- `bread_preparation`
- `infusion`
- `straining`
- `cooling`
- `inoculation`
- `primary_fermentation`
- `ready_to_bottle`
- `bottling`
- `bottle_conditioning`
- `chilling`
- `ready`
- `discard`
- `unknown`

The canonical schema is:

```text
agent-instructions/state.schema.json
```

An example is:

```text
agent-instructions/state-example.json
```

## Rules

- Do not move to the next stage until the user confirms the required action or observation.
- Do not invent start times, temperatures, ingredient amounts, or completed actions.
- Keep safety flags even after the stage changes.
- Do not mix data from different batches.
- Change only one experimental variable at a time.

## Safety transitions

Set `stage: discard` if the user confirms mold, fuzzy growth, colored spots, slime, rotten smell, acetone smell, meat-like smell, or sewage smell.

Add `sealed_primary_fermentation` if primary fermentation is tightly sealed.

Add `bottle_overpressure` if a plastic bottle is very firm or deformed. The next action is to refrigerate carefully and not shake it.

## Response format

Normal responses should contain:

1. **Current state** — in plain language.
2. **Next action** — one concrete action.
3. **Check back with** — what the user should report next.

Do not print the full JSON unless the user asks for it or the state is being transferred to another agent.

## Handoff

When handing the batch to another agent, provide:

- a short human summary;
- the current JSON state;
- the last confirmed action;
- the next safe action;
- unknown fields.
