---
lang: de
doc_type: summary
title: Kvas Zhizha - Zusammenfassung
subtitle: Reproduzierbarer hausgemachter Kwas für Menschen und KI-Agenten
version: 1.0.6
---

<!-- section:overview -->
## Was ist das?

**Kvas** ist eine offene Wissensbasis für sicheren und reproduzierbaren hausgemachten Kwas. **Zhizha** ist Marke und Charakter des Projekts. Version 1.0.6 bietet dieselbe Dokumentstruktur in fünf Sprachen als PDF und Webseite.

<!-- section:baseline -->
## Basis für 3 Liter

- Wasser - 3 l;
- vollständig trockenes Brot/Zwieback - 180-220 g;
- bevorzugt 150 g weiß + 50-70 g Roggen oder Borodinsky;
- Zucker oder Panela - 100-120 g;
- Malz - 20-30 g, oder Roggenmehl - 10-20 g;
- frische Hefe - 2-3 g, oder Trockenhefe - 0,5-1 g, nur für die erste Charge.

Für spätere Chargen keine neue Hefe zugeben; stattdessen 500 ml alten Kwas/Starter oder 3-5 EL Bodensatz verwenden.

<!-- section:process -->
## Kurzer Ablauf

1. Brot dunkelgolden rösten.
2. Mit kochendem Wasser übergießen und 4-8 Stunden ziehen lassen.
3. Abseihen und nur die Flüssigkeit behalten.
4. Süße hinzufügen und auf 25-35°C abkühlen.
5. Starter hinzufügen und 8-12 Stunden unter Tuch oder lockerem Deckel gären.
6. Bei normalem Geruch und Blasen in Plastikflaschen abfüllen.
7. 2-6 Stunden karbonisieren und kühlen, sobald die Flasche fest wird.
8. Mindestens 8 Stunden kalt stellen.

<!-- section:sweeteners -->
## Zucker, Panela, Maltose und Malz

Brot enthält überwiegend Stärke, und Hefe wandelt sie nicht selbst in Zucker um. Das einfache Verfahren braucht deshalb eine kontrollierte Süße. Panela ersetzt weißen Zucker ungefähr 1:1 und gibt Melassenoten. Maltose ist vergärbar, ersetzt aber weder Malzgeschmack noch Enzyme. Für Malzaroma ist Malzextrakt meist besser als reine Maltose.

<!-- section:state -->
## Chargenzustand

Der KI-Agent führt einen ausdrücklichen Zustand: `planning`, `bread_preparation`, `infusion`, `straining`, `cooling`, `inoculation`, `primary_fermentation`, `ready_to_bottle`, `bottling`, `bottle_conditioning`, `chilling`, `ready`, `discard` oder `unknown`. Unbekannte Werte bleiben `null`; Phasen wechseln nur nach Bestätigung des Nutzers.

<!-- section:safety -->
## Sicherheit

Die Hauptgärung darf nicht luftdicht verschlossen sein. Nach der Flaschengärung die Plastikflasche kühlen, sobald sie fest wird. Charge bei Schimmel, flaumigem Belag, farbigen Flecken, Schleim, fauligem Geruch, Acetongeruch, Fleisch- oder Kanalgeruch wegschütten.

<!-- section:links -->
## Ressourcen

- Agentenanweisung: `agent-instructions/kvas-agent.de.md`
- Zustandsmodell: `agent-instructions/state-model.de.md`
- JSON Schema: `agent-instructions/state.schema.json`
- Vollständiges Protokoll: `recipes/kvas-reproducible.md`
- Chargenprotokoll: `docs/batch-log-template.md`
- Repository: https://github.com/bambuchastudent/kvas-ai-agent
