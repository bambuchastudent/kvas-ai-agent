---
lang: es
doc_type: summary
title: Kvas Zhizha - Resumen
subtitle: Kvas casero reproducible para personas y agentes de IA
version: 1.1.0
---

<!-- section:overview -->
## Qué es

**Kvas** es una base de conocimientos abierta para preparar kvas casero de forma segura y reproducible. **Zhizha** es la marca y personalidad del proyecto. La versión 1.1.0 ofrece la misma estructura documental en cinco idiomas, en PDF y páginas web.

<!-- section:baseline -->
## Base para 3 litros

- agua - 3 l;
- pan completamente seco - 180-220 g;
- preferiblemente 150 g blanco + 50-70 g de centeno o Borodinsky;
- azúcar o panela - 100-120 g;
- malta - 20-30 g, o harina de centeno - 10-20 g;
- levadura fresca - 2-3 g, o seca - 0,5-1 g, solo para la primera tanda.

No se añade levadura nueva a las tandas siguientes; en su lugar se usan 500 ml de kvas viejo/fermento o 3-5 cucharadas de sedimento.

<!-- section:process -->
## Proceso corto

1. Tostar el pan hasta dorado oscuro.
2. Verter agua hirviendo y dejar 4-8 horas.
3. Colar y conservar solo el líquido.
4. Añadir el endulzante y enfriar a 25-35°C.
5. Añadir el fermento y fermentar 8-12 horas bajo tela o tapa suelta.
6. Cuando el olor sea normal y haya burbujas, embotellar en plástico.
7. Gasificar 2-6 horas y refrigerar cuando la botella esté firme.
8. Enfriar al menos 8 horas.

<!-- section:sweeteners -->
## Azúcar, panela, maltosa y malta

El pan contiene sobre todo almidón y la levadura no lo convierte por sí sola en azúcar. Por eso el método simple necesita un endulzante controlado. La panela sustituye al azúcar blanco aproximadamente 1:1 y aporta notas de melaza. La maltosa fermenta, pero no sustituye el sabor ni las enzimas de la malta. El extracto de malta suele ser mejor que la maltosa pura para el aroma.

<!-- section:state -->
## Estado de la tanda

El agente de IA mantiene un estado explícito: `planning`, `bread_preparation`, `infusion`, `straining`, `cooling`, `inoculation`, `primary_fermentation`, `ready_to_bottle`, `bottling`, `bottle_conditioning`, `chilling`, `ready`, `discard` o `unknown`. Los valores desconocidos permanecen `null`; las etapas cambian solo tras confirmación del usuario.

<!-- section:safety -->
## Seguridad

La fermentación principal no debe cerrarse herméticamente. Tras la gasificación, refrigerar la botella de plástico cuando esté firme. Tirar la tanda si hay moho, crecimiento peludo, manchas de color, baba, olor a podrido, acetona, carne o alcantarilla.

<!-- section:links -->
## Recursos

- Instrucción del agente: `agent-instructions/kvas-agent.es.md`
- Modelo de estado: `agent-instructions/state-model.es.md`
- JSON Schema: `agent-instructions/state.schema.json`
- Protocolo completo: `recipes/kvas-reproducible.md`
- Registro de tanda: `docs/batch-log-template.md`
- Repositorio: https://github.com/bambuchastudent/kvas-ai-agent
