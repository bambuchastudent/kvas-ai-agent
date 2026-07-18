---
lang: es
doc_type: summary
title: KVASSISTENT — guía rápida para personas
subtitle: Kvas Zhizha casero, calor, sol y límites de alcohol
version: 1.1.1.1.1
---

<!-- section:overview -->
## Qué es

**KVASSISTENT** ayuda a una persona a preparar kvas Zhizha y ofrece por separado un protocolo para agentes de IA. La versión 1.1.1.1.1 añade reglas investigadas para 28°C, luz solar directa y estimación honesta del alcohol.

<!-- section:baseline -->
## Base para 3 litros

- agua — 3 l;
- pan completamente seco — 180–220 g;
- mejor: 150 g blanco + 50–70 g de centeno o Borodinsky;
- azúcar o panela — 100–120 g;
- malta — 20–30 g o harina de centeno — 10–20 g;
- primera tanda: 0,5–1 g de levadura seca o 2–3 g fresca;
- tandas siguientes: 500 ml de kvas viejo o 3–5 cucharadas de sedimento.

<!-- section:process -->
## Proceso corto

1. Tostar el pan hasta dorado oscuro.
2. Verter agua hirviendo durante 4–8 horas.
3. Colar y conservar solo el líquido.
4. Añadir el endulzante y enfriar a 25–35°C.
5. Añadir el fermento y cubrir con tela, gasa o tapa suelta.
6. Fermentar 8–12 horas; a 28°C revisar a las 4–6 horas.
7. Embotellar en plástico con olor normal y burbujas.
8. Gasificar 2–6 horas y refrigerar cuando la botella esté firme.

<!-- section:heat -->
## Calor de 28°C y sol

28°C **a la sombra** es aceptable pero rápido. No dejar el frasco al sol directo: el líquido puede calentarse mucho más que el aire. Moverlo a la sombra, medir la temperatura del líquido y revisarlo con frecuencia.

Zonas: 18–24°C estable; 25–27°C rápida; 28–30°C caliente y revisión desde 4 horas; 31–34°C mover a un lugar fresco; 35°C o más enfriar y detener el protocolo doméstico.

<!-- section:alcohol -->
## ¿Llegará a 8% en dos semanas?

No automáticamente. En 3 l, 100–120 g de azúcar añadido dan un máximo teórico aproximado de 2,2–2,6% vol. solo a partir de ese azúcar. Para un 8% teórico harían falta unos 370 g de azúcar fermentable, y más en la práctica. El porcentaje exacto requiere densidad inicial/final o análisis de laboratorio.

Dos semanas a 28°C ya no son el proceso rápido básico, sino una fermentación alcohólica y ácida prolongada y menos predecible.

<!-- section:sweeteners -->
## Azúcar, panela, maltosa y malta

La panela sustituye al azúcar aproximadamente 1:1. La maltosa fermenta, pero no sustituye el sabor ni las enzimas de la malta. El extracto de malta suele ser mejor para el aroma.

<!-- section:state -->
## Estado de la tanda

El agente registra temperatura ambiente y del líquido, máxima temperatura, sol directo, tiempo de exposición, cierre, observaciones y estimación de alcohol. Lo desconocido queda como `null`.

<!-- section:safety -->
## Seguridad

No cerrar herméticamente la fermentación principal. Retirar inmediatamente el frasco del sol. Tirar la tanda si hay moho, crecimiento peludo, manchas de color, baba, olor a podrido, acetona, carne o alcantarilla.

<!-- section:links -->
## Recursos

- Investigación: `docs/research-fermentation-heat.md`
- Agente: `agent-instructions/kvas-agent.es.md`
- Estado: `agent-instructions/state-model.es.md`
- Schema: `agent-instructions/state.schema.json`
- Repositorio: https://github.com/bambuchastudent/kvas-ai-agent
