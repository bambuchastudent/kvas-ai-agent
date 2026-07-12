---
lang: en
doc_type: summary
title: Kvas Zhizha - Summary
subtitle: Reproducible homemade kvass for people and AI agents
version: 1.0.5
---

<!-- section:overview -->
## What this is

**Kvas** is an open knowledge base for safe and reproducible homemade kvass. **Zhizha** is the project brand and personality. Version 1.0.5 provides the same document structure in five languages, as PDFs and web pages.

<!-- section:baseline -->
## 3-liter baseline

- water - 3 l;
- fully dry bread crackers - 180-220 g;
- preferably 150 g white + 50-70 g rye or Borodinsky;
- sugar or panela - 100-120 g;
- malt - 20-30 g, or rye flour - 10-20 g;
- fresh yeast - 2-3 g, or dry yeast - 0.5-1 g.

Later batches may use 500 ml old kvass or 3-5 tbsp sediment.

<!-- section:process -->
## Short process

1. Toast bread until dark golden.
2. Pour over boiling water and infuse for 4-8 hours.
3. Strain and keep only the liquid.
4. Add sweetener and cool to 25-35°C.
5. Add starter and ferment for 8-12 hours under cloth or a loose lid.
6. When the smell is normal and bubbles appear, bottle in plastic.
7. Carbonate for 2-6 hours and refrigerate as soon as the bottle becomes firm.
8. Chill for at least 8 hours.

<!-- section:sweeteners -->
## Sugar, panela, maltose, and malt

Bread contains mostly starch, and yeast does not turn it into sugar by itself. A controlled sweetener is therefore needed in the simple recipe. Panela replaces white sugar roughly 1:1 and adds molasses notes. Maltose can ferment but does not replace malt flavor or enzymes. Malt extract is usually better than pure maltose for malt aroma.

<!-- section:state -->
## Batch state

The AI agent maintains one explicit state: `planning`, `bread_preparation`, `infusion`, `straining`, `cooling`, `inoculation`, `primary_fermentation`, `ready_to_bottle`, `bottling`, `bottle_conditioning`, `chilling`, `ready`, `discard`, or `unknown`. Unknown values remain `null`; stages change only after user confirmation.

<!-- section:safety -->
## Safety

Primary fermentation must not be tightly sealed. After bottle conditioning, refrigerate a plastic bottle as soon as it becomes firm. Discard the batch for mold, fuzzy growth, colored spots, slime, rotten smell, acetone smell, meat-like smell, or sewage smell.

<!-- section:links -->
## Resources

- AI agent instruction: `agent-instructions/kvas-agent.en.md`
- State model: `agent-instructions/state-model.en.md`
- JSON Schema: `agent-instructions/state.schema.json`
- Full protocol: `recipes/kvas-reproducible.md`
- Batch log: `docs/batch-log-template.md`
- Repository: https://github.com/bambuchastudent/kvas-ai-agent
