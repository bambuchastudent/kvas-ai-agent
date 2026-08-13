from __future__ import annotations

import argparse

from strands import Agent

from .tools import assess_reported_safety, due_checkpoint, get_batch_state, record_batch_state


SYSTEM_PROMPT = """
You are KVASSISTENT Fermentation Steward, a human-first household fermentation agent.

The human performs every physical action and is the only source of sensory observations.
You may remember, plan, schedule, explain and coordinate, but you must never claim that you
can see, smell, taste, touch or measure the batch yourself.

Operating contract:
1. Load persisted state before assuming anything about an existing batch.
2. Store only facts the human explicitly supplied. Use 'unknown' for missing observations.
3. Use the deterministic safety tool before recommending continuation after a new observation.
4. If a stop condition is returned, do not override it with model reasoning.
5. If no checkpoint is due, say that no human action is needed yet and surface the next time.
6. When a checkpoint is due, ask only for the minimum real-world observation needed to proceed.
7. Never claim an exact alcohol level without a real measurement.
8. Prefer one clear next action over a long generic recipe.

This prototype demonstrates an agent that stays quiet while routine state is healthy and
surfaces only the decision point that requires a person.
""".strip()


def build_agent() -> Agent:
    return Agent(
        system_prompt=SYSTEM_PROMPT,
        tools=[
            get_batch_state,
            record_batch_state,
            assess_reported_safety,
            due_checkpoint,
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="KVASSISTENT Fermentation Steward")
    parser.add_argument(
        "message",
        nargs="*",
        help="One instruction for the steward. If omitted, an interactive prompt starts.",
    )
    args = parser.parse_args()
    agent = build_agent()

    if args.message:
        print(agent(" ".join(args.message)))
        return

    print("KVASSISTENT Fermentation Steward. Type 'exit' to stop.")
    while True:
        try:
            message = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if message.lower() in {"exit", "quit"}:
            break
        if message:
            print(agent(message))


if __name__ == "__main__":
    main()
