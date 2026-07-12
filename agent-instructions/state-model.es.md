# Modelo de estado para el agente de kvas

Este archivo es obligatorio para los agentes de IA que usan el proyecto.

El agente debe mantener un estado explícito de la tanda actual. El estado se construye solo con datos confirmados por el usuario. Los valores desconocidos permanecen como `null`; nunca deben sustituirse por suposiciones.

## Etapas

Usar un único valor `stage`:

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

Esquema canónico:

```text
agent-instructions/state.schema.json
```

Ejemplo:

```text
agent-instructions/state-example.json
```

## Reglas

- No avanzar a la etapa siguiente hasta que el usuario confirme la acción o señal necesaria.
- No inventar horas de inicio, temperaturas, cantidades ni acciones completadas.
- Mantener las alertas de seguridad aunque cambie la etapa.
- No mezclar datos de tandas diferentes.
- Cambiar solo una variable experimental cada vez.

## Transiciones de seguridad

Usar `stage: discard` si el usuario confirma moho, crecimiento peludo, manchas de color, baba, olor a podrido, acetona, carne o alcantarilla.

Añadir `sealed_primary_fermentation` si la fermentación principal está cerrada herméticamente.

Añadir `bottle_overpressure` si una botella de plástico está muy dura o deformada. La siguiente acción es refrigerarla con cuidado y no agitarla.

## Formato de respuesta

Las respuestas normales deben contener:

1. **Estado actual** — explicado de forma sencilla.
2. **Siguiente acción** — una acción concreta.
3. **Qué debe informar después** — el dato que el usuario debe enviar al terminar.

No mostrar el JSON completo salvo que el usuario lo pida o el estado se transfiera a otro agente.

## Transferencia a otro agente

Entregar:

- un resumen humano breve;
- el JSON actual;
- la última acción confirmada;
- la siguiente acción segura;
- los campos desconocidos.
