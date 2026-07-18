---
lang: en
doc_type: summary
title: KVASSISTENT — human quick guide
subtitle: Homemade Zhizha kvass, hot weather, sunlight, and alcohol limits
version: 1.1.1.1.1
---

<!-- section:overview -->
## What this is

**KVASSISTENT** helps a person make homemade Zhizha kvass and gives AI agents a separate state-management protocol. Version 1.1.1.1.1 adds researched rules for 28°C fermentation, direct sunlight, and honest alcohol estimates.

<!-- section:baseline -->
## 3-liter baseline

- water — 3 l;
- fully dry bread crackers — 180–220 g;
- preferably 150 g white + 50–70 g rye or Borodinsky;
- sugar or panela — 100–120 g;
- malt — 20–30 g or rye flour — 10–20 g;
- first batch: 0.5–1 g dry or 2–3 g fresh yeast;
- later batches: 500 ml old kvass or 3–5 tbsp sediment.

<!-- section:process -->
## Short process

1. Toast bread dark golden.
2. Infuse in boiling water for 4–8 hours.
3. Strain and keep only the liquid.
4. Add sweetener and cool to 25–35°C.
5. Add starter and cover with cloth, gauze, or a loose lid.
6. Ferment 8–12 hours; at 28°C check after 4–6 hours.
7. Bottle in plastic when smell is normal and bubbles are present.
8. Condition for 2–6 hours and refrigerate as soon as the bottle becomes firm.

<!-- section:heat -->
## 28°C heat and sunlight

28°C **in shade** is acceptable but fast. Never keep the jar in direct sunlight: the liquid can become much hotter than the air. Move it to shade, measure liquid temperature, and check it frequently.

Operating zones:

- 18–24°C — steady;
- 25–27°C — fast, check from 6 hours;
- 28–30°C — hot, shade only, check from 4 hours;
- 31–34°C — move cooler;
- 35°C or above — cool and stop the household protocol.

<!-- section:alcohol -->
## Will it reach 8% in two weeks?

Not automatically. Alcohol is limited by fermentable sugar, not by time and heat alone. In 3 l, 100–120 g added sugar gives a theoretical maximum of about 2.2–2.6% ABV from that sugar alone. A theoretical 8% would require roughly 370 g fermentable sugar, and more in practice. Exact ABV requires original/final gravity or laboratory measurement.

Two weeks at 28°C is no longer the standard quick-kvass process; it is extended alcoholic and acidic fermentation with less predictable results.

<!-- section:sweeteners -->
## Sugar, panela, maltose, and malt

Panela replaces white sugar roughly 1:1. Maltose can ferment but does not replace malt flavor or enzymes. Malt extract is usually more useful than pure maltose for malt character.

<!-- section:state -->
## Batch state

The AI agent records air and liquid temperatures, peak temperature, direct sunlight, warm exposure time, closure, observations, and alcohol estimate. Unknown values remain `null`.

<!-- section:safety -->
## Safety

Do not tightly seal primary fermentation. Remove the jar from sunlight immediately. Discard for mold, fuzzy growth, colored spots, slime, rotten smell, acetone smell, meat-like smell, or sewage smell.

<!-- section:links -->
## Resources

- Heat research: `docs/research-fermentation-heat.md`
- Agent instruction: `agent-instructions/kvas-agent.en.md`
- State model: `agent-instructions/state-model.en.md`
- JSON Schema: `agent-instructions/state.schema.json`
- Repository: https://github.com/bambuchastudent/kvas-ai-agent
