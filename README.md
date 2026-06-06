# Merrin Voice 01

Interactive app prototype for explaining the **Merrin Voice 01 — Constrained Grief** Eurorack voice.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Purpose

Explain how the Constrained Grief voice works by showing each module, the signal path, and the emotional job of every stage.

## Good enough for v0.2

A person can open the app, click through the five modules, switch between linked voice mode and independent module mode, and understand what the rear Merrin Link bus does without reading the full technical spec.

## Current app

- Single static `index.html`
- No framework
- No build step
- Opens directly in a browser
- Explains the five modules and Merrin Link bus
- Includes one tiny Web Audio preview button
- Shows linked voice mode vs independent module mode
- Shows active / inactive rear bus line states
- Shows small module jumper notes
- Explains that front-panel patching can override the hidden rear link

## Locked signal path

```text
CV → MV-02 → MV-01 → MV-03 → MF-01 → MF-02 → Output
Gate → MV-03
```

## Concept path

```text
SCALE → TONE → ENVELOPE → ROOM → MEMORY
```

## Module order

1. `MV-02` — Melancholy Quantizer
2. `MV-01` — Somber Oscillator
3. `MV-03` — Lingering Voice
4. `MF-01` — Desolate Space
5. `MF-02` — Fading Echoes

## Merrin Link modes

### Linked voice mode

The rear Merrin Link bus connects the five modules as one pre-wired voice.

Active bus lines:

- `PITCH`
- `GATE`
- `AUD_A`
- `AUD_B`
- `AUD_C`
- `GND`

### Independent module mode

The modules are treated as separate Eurorack units.

Inactive bus lines:

- `PITCH`
- `GATE`
- `AUD_A`
- `AUD_B`
- `AUD_C`

`GND` remains always active as the shared reference.

## Front patch rule

If a front-panel cable is inserted, it can override the hidden Merrin Link connection.

## Version notes

### v0.1

Clickable signal guide with five module cards, detail panel, Merrin Link bus panel, and one tiny audio preview.

### v0.2

Adds the Merrin Link jumper view:

- linked voice mode / independent module mode toggle
- active / inactive bus line states
- module jumper notes
- front-panel patch override explanation

## Current boundary

This app explains the instrument and includes one tiny audio preview.

It does **not** yet:

- provide full synth controls
- save patches
- simulate electronics
- design PCBs
- act as a VCV Rack module
- simulate patch cables
