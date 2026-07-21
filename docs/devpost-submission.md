# KVASSISTENT — Devpost submission copy

## Tagline

One jar. One verified state. One safe next action — from stale bread to kvass with an AI agent beside you.

## Inspiration

**One jar. One verified state. One safe next action.**

Recipes assume the kitchen will behave. Real kitchens do not. The room gets hotter, the jar sits in sunlight, a check-in happens late, and a person suddenly has a much harder question than “what is step four?” They need to know: **what should I do now, based on what is actually true?**

KVASSISTENT turns stale bread into a useful everyday drink and a messy physical process into a careful collaboration between human hands and a GPT-5.6-powered Codex agent. The human can see, smell, taste, and act. The agent can remember, reason, explain, and wait for evidence.

The unusual part is that the repository itself is part of the product. Any compatible AI agent that opens it finds a clear operating contract, not a pile of disconnected notes. It immediately learns how to guide one real batch without inventing observations or pretending to be a laboratory.

## What it does

KVASSISTENT guides a person from dry bread to chilled kvass through one calm loop:

1. **Current state** — only facts the person has confirmed.
2. **Next action** — one concrete step, not a wall of instructions.
3. **Report back with** — the observation needed before continuing.

The agent starts with five accessible questions: water volume, bread condition, starter, room temperature, and what has already happened. It never silently assumes that a step is complete.

The installable **Live Batch** companion then records temperature, time, sunlight, closure, surface, smell, and taste locally in the browser. A deterministic safety engine converts those observations into one next action. Its **AI safety brief** exposes the complete decision trace—temperature, surface, smell, closure, sunlight, timing, and explicit unknowns—so a person can see why the recommendation was made.

Mold, slime, dangerous smells, 35°C+ liquid, and sealed primary fermentation have explicit stop or corrective branches. Unknown values remain `null`; they are never filled with a plausible-sounding guess.

The batch can be handed to another AI agent as structured JSON containing the last confirmed action, next safe step, unknown fields, and safety flags. The PWA works offline, needs no account, stores batch history only on the device, and supports Russian, English, Spanish, German, and Simplified Chinese.

### Judge it in 60 seconds

1. Open the [one-click live scenario](https://kvassistent.pages.dev/v1.1.1.1.1.1.1.1/companion/?demo=1): a real-world check-in at 26 hours, 28°C, with direct sunlight.
2. Read the single recommended next action.
3. Expand **Why this advice?** and see the warm-temperature and sunlight signals separated from what the system cannot know.
4. Copy the AI safety brief to see a structured, inspectable handoff.
5. Open [`AI_AGENT_START.md`](https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/AI_AGENT_START.md) and watch the repository teach an AI agent the same protocol.

No signup, API key, rebuild, or test account is required.

## How we built it

This is not a chatbot wrapped around a recipe. It is a coordinated system with three layers:

- **Agent contract:** `AI_AGENT_START.md`, full multilingual instructions, a state model, JSON Schema, reproducible recipe, and safety checklist.
- **Decision engine:** deterministic rules that generate both the verdict and the explanation, preventing the interface from displaying a reason that disagrees with the action.
- **Local-first product:** an installable PWA with timed check-ins, history, offline support, multilingual UI, explainable signals, and structured agent handoff.

We used **Codex powered by GPT-5.6** as the engineering partner throughout the Build Week extension. Codex mapped cross-file dependencies, inspected the existing fermentation guidance, designed the agent entry point, implemented the Live Batch and safety-brief flow, expanded automated rule-engine tests, and verified the versioned publication pipeline. Graphify made repository-wide relationships queryable; Serena supported symbol-level changes in the Python and Bash build system.

The human product decision remained explicit: AI may organize evidence and recommend the next step, but it may not manufacture sensory evidence. That boundary shaped the schema, the UI, the tests, and every safety branch.

### What is new for Build Week

KVASSISTENT existed as a multilingual knowledge project before the event. During Build Week it was meaningfully extended into a working agent-native application:

- the **Live Batch** installable PWA;
- the deterministic safety and next-check engine;
- the explainable **AI safety brief**;
- local history and structured cross-agent handoff;
- the root-level `AI_AGENT_START.md` contract that activates any compatible AI agent from the repository link;
- a simple first-batch recipe embedded into the product;
- expanded automated tests and CI verification;
- the one-click judge scenario and versioned release `1.1.1.1.1.1.1.1`.

The dated commit history, README section **How Codex helped in this version**, release notes, and Codex session provide a clear boundary between prior work and the Build Week implementation.

## Challenges we ran into

The hardest problem was not generating more advice. It was deciding what the assistant must refuse to guess.

An AI agent cannot verify microbiological safety, smell a jar, or know that a person completed a step. A conventional conversational UI tends to smooth over those gaps. We made uncertainty a first-class product state instead: missing observations remain unknown, safety-sensitive signals interrupt normal progress, and every handoff carries `unknowns` and `safety_flags`.

The second challenge was making a detailed fermentation protocol feel effortless on a phone. We used progressive disclosure: one next action on the main path, with the decision trace available when the user or judge wants to inspect it.

The third was keeping natural-language guidance and executable behavior aligned across five languages. The shared state model, deterministic engine, test suite, and versioned publication pipeline keep those surfaces from drifting apart.

## Accomplishments that we're proud of

- **A repository link becomes an agent interface.** An AI agent can begin the correct one-batch protocol immediately after reading the project.
- **The demo is a real product, not a mockup.** It is installable, offline-capable, responsive, and usable without an account.
- **Every recommendation is inspectable.** The same rule engine produces the action and its safety brief.
- **Uncertainty is visible.** The product distinguishes observations, deductions, and unknowns instead of hiding them behind fluent prose.
- **The physical task remains human-centered.** AI supports hands-on judgment rather than replacing it.
- **The experience travels.** Five interface languages and structured JSON handoff let the same batch continue across people and agents.
- **Critical behavior is tested.** Mold, slime, unsafe smells, overheating, direct sunlight, closure, timing, and handoff branches are covered automatically.

Most importantly, KVASSISTENT turns AI from a recipe generator into a patient collaborator that waits for evidence.

## What we learned

For everyday AI, trust comes from pacing and boundaries. **One verified state, one safe action, one requested observation** is often more useful than a confident page of generated advice.

We learned that explainability does not need to mean a technical dashboard. In a kitchen it can simply mean: “I noticed 28°C and direct sunlight; I do not know what the surface smells like; move the jar now and report back.”

We also learned that a repository can be a product surface. When instructions, schemas, rules, tests, and a browser companion share one contract, an AI agent can join a real-world workflow without a proprietary integration or locked account.

## What's next for KVASSISTENT

Next we want optional camera-assisted check-ins with mandatory human confirmation, private on-device batch comparison, accessibility testing with first-time makers, and a reusable agent-contract template for other hands-on routines such as sourdough, pickling, and kombucha.

The larger vision is a family of local-first **Apps for Your Life** where AI helps people act on real objects in the real world—and earns trust by being precise about what it cannot observe.

## Built with

Codex, GPT-5.6, JavaScript, HTML, CSS, Python, PWA, JSON Schema, Markdown, Graphify, Serena

## Try it out

- Live product: https://kvassistent.pages.dev/
- One-click judge demo: https://kvassistent.pages.dev/v1.1.1.1.1.1.1.1/companion/?demo=1
- AI agent entry: https://github.com/bambuchastudent/kvas-ai-agent/blob/develop/AI_AGENT_START.md
- Source: https://github.com/bambuchastudent/kvas-ai-agent

## Three-minute judge path

1. Open the one-click demo and show the single recommended next action.
2. Expand “Why this advice?” to reveal the 28°C and direct-sunlight signals plus explicit unknowns.
3. Copy/share the AI safety brief to demonstrate a structured handoff.
4. Open `AI_AGENT_START.md` and show that the repository itself teaches any AI agent the same one-batch protocol.
5. End on the category promise: stale bread becomes a useful household routine, and AI remains accountable to human observations.
