# Merrin Voice 01

Interactive app prototype for explaining the **Merrin Voice 01 — Constrained Grief** Eurorack voice.

## Purpose

Explain how the Constrained Grief voice works by showing each module, the signal path, and the emotional job of every stage.

## Good enough for v0.1

A person can open the app, click through the five modules, and understand what each part does without reading the full technical spec.

## Current app

- Single static `index.html`
- No framework
- No build step
- Opens directly in a browser
- Explains the five modules and Merrin Link bus

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

## v0.1 boundary

This version explains the instrument.

It does **not** yet:

- generate audio
- save patches
- simulate electronics
- design PCBs
- act as a VCV Rack module

## Next likely version

`v0.2` should add a clearer Merrin Link / jumper view.
