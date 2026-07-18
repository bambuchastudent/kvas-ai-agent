---
lang: de
doc_type: summary
title: KVASSISTENT — Kurzanleitung für Menschen
subtitle: Hausgemachter Zhizha-Kwas, Hitze, Sonne und Alkoholgrenzen
version: 1.1.1.1.1
---

<!-- section:overview -->
## Was ist das?

**KVASSISTENT** hilft einem Menschen, hausgemachten Zhizha-Kwas herzustellen, und bietet getrennte Regeln für KI-Agenten. Version 1.1.1.1.1 ergänzt untersuchte Regeln für 28°C, direkte Sonne und ehrliche Alkoholabschätzung.

<!-- section:baseline -->
## Basis für 3 Liter

- Wasser — 3 l;
- vollständig trockenes Brot/Zwieback — 180–220 g;
- besser: 150 g weiß + 50–70 g Roggen oder Borodinsky;
- Zucker oder Panela — 100–120 g;
- Malz — 20–30 g oder Roggenmehl — 10–20 g;
- erste Charge: 0,5–1 g Trockenhefe oder 2–3 g frische Hefe;
- spätere Chargen: 500 ml alter Kwas oder 3–5 EL Bodensatz.

<!-- section:process -->
## Kurzer Ablauf

1. Brot dunkelgolden rösten.
2. Mit kochendem Wasser 4–8 Stunden ziehen lassen.
3. Abseihen und nur die Flüssigkeit behalten.
4. Süße hinzufügen und auf 25–35°C abkühlen.
5. Starter hinzufügen und mit Tuch, Gaze oder lockerem Deckel abdecken.
6. 8–12 Stunden gären; bei 28°C nach 4–6 Stunden prüfen.
7. Bei normalem Geruch und Blasen in Plastikflaschen abfüllen.
8. 2–6 Stunden karbonisieren und bei fester Flasche kühlen.

<!-- section:heat -->
## 28°C Hitze und Sonne

28°C **im Schatten** ist möglich, aber schnell. Das Glas darf nicht in direkter Sonne stehen: Die Flüssigkeit kann deutlich heißer als die Luft werden. In den Schatten stellen, Flüssigkeit messen und häufig prüfen.

Zonen: 18–24°C ruhig; 25–27°C schnell; 28–30°C heiß und Prüfung ab 4 Stunden; 31–34°C kühler stellen; ab 35°C abkühlen und Haushaltsprotokoll stoppen.

<!-- section:alcohol -->
## Erreicht es in zwei Wochen 8%?

Nicht automatisch. In 3 l ergeben 100–120 g zugesetzter Zucker theoretisch höchstens etwa 2,2–2,6 Vol.-% aus diesem Zucker. Für theoretische 8% wären etwa 370 g vergärbarer Zucker nötig, praktisch mehr. Genaues ABV erfordert Anfangs-/Enddichte oder Laboranalyse.

Zwei Wochen bei 28°C sind kein schneller Basiskwas mehr, sondern eine verlängerte alkoholische und saure Gärung mit weniger vorhersehbarem Ergebnis.

<!-- section:sweeteners -->
## Zucker, Panela, Maltose und Malz

Panela ersetzt Zucker ungefähr 1:1. Maltose ist vergärbar, ersetzt aber Malzgeschmack und Enzyme nicht. Malzextrakt ist für Malzaroma meist besser.

<!-- section:state -->
## Chargenzustand

Der Agent speichert Luft- und Flüssigkeitstemperatur, Höchsttemperatur, direkte Sonne, Expositionszeit, Verschluss, Beobachtungen und Alkoholabschätzung. Unbekanntes bleibt `null`.

<!-- section:safety -->
## Sicherheit

Hauptgärung nicht luftdicht verschließen. Glas sofort aus der Sonne nehmen. Bei Schimmel, flaumigem Belag, farbigen Flecken, Schleim, Fäulnis-, Aceton-, Fleisch- oder Kanalgeruch wegschütten.

<!-- section:links -->
## Ressourcen

- Forschung: `docs/research-fermentation-heat.md`
- Agent: `agent-instructions/kvas-agent.de.md`
- Zustand: `agent-instructions/state-model.de.md`
- Schema: `agent-instructions/state.schema.json`
- Repository: https://github.com/bambuchastudent/kvas-ai-agent
