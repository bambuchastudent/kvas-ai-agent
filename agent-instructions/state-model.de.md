# Zustandsmodell für den Kwas-Agenten

Diese Datei ist für KI-Agenten, die dieses Projekt verwenden, verpflichtend.

Der Agent muss einen ausdrücklichen Zustand für die aktuelle Charge führen. Der Zustand basiert nur auf vom Nutzer bestätigten Daten. Unbekannte Werte bleiben `null`; sie dürfen nicht durch Vermutungen ersetzt werden.

## Phasen

Einen einzelnen `stage`-Wert verwenden:

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

Kanonisches Schema:

```text
agent-instructions/state.schema.json
```

Beispiel:

```text
agent-instructions/state-example.json
```

## Regeln

- Erst zur nächsten Phase wechseln, wenn der Nutzer die nötige Handlung oder Beobachtung bestätigt.
- Keine Startzeiten, Temperaturen, Mengen oder ausgeführten Handlungen erfinden.
- Sicherheitswarnungen auch nach einem Phasenwechsel beibehalten.
- Daten verschiedener Chargen nicht vermischen.
- Immer nur eine experimentelle Variable gleichzeitig ändern.

## Sicherheitsübergänge

`stage: discard` setzen, wenn Schimmel, flaumiger Belag, farbige Flecken, Schleim, fauliger Geruch, Acetongeruch, Fleischgeruch oder Kanalgeruch bestätigt werden.

`sealed_primary_fermentation` hinzufügen, wenn die Hauptgärung luftdicht verschlossen ist.

`bottle_overpressure` hinzufügen, wenn eine Plastikflasche sehr fest oder verformt ist. Nächste Handlung: vorsichtig kühlen und nicht schütteln.

## Antwortformat

Normale Antworten sollen enthalten:

1. **Aktueller Zustand** — einfach erklärt.
2. **Nächster Schritt** — eine konkrete Handlung.
3. **Danach melden** — welche Beobachtung der Nutzer anschließend mitteilen soll.

Das vollständige JSON nur auf Wunsch oder bei der Übergabe an einen anderen Agenten zeigen.

## Übergabe

Bei der Übergabe an einen anderen Agenten liefern:

- kurze verständliche Zusammenfassung;
- aktuellen JSON-Zustand;
- letzte bestätigte Handlung;
- nächste sichere Handlung;
- unbekannte Felder.
