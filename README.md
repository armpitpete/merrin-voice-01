# Merrin Voice 01

Interactive app prototype for explaining the **Merrin Voice 01 — Constrained Grief** Eurorack voice.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Purpose

Explain how the Constrained Grief voice works by showing each module, the signal path, and the emotional job of every stage.

## Good enough for v0.5

A person can open the app, click through the five modules, switch between linked voice mode and independent module mode, understand front-panel override examples, slightly change the voice sample, and read the page smoothly without a large layout gap.

## Current app

- Single static `index.html`
- No framework
- No build step
- Opens directly in a browser
- Explains the five modules and Merrin Link bus
- Includes one tiny Web Audio preview button
- Includes tiny sound controls: `Brightness` and `Echo`
- Shows linked voice mode vs independent module mode
- Shows active / inactive rear bus line states
- Shows small module jumper notes
- Explains that front-panel patching can override the hidden rear link
- Shows two front-panel override examples
- Improves page flow and bus readability for v0.5

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

## Front-panel override examples

### External pitch overrides Merrin pitch

- Default linked path: `MV-02 → PITCH → MV-01`
- Front patch: external pitch cable into `MV-01 1V/OCT`
- Result: MV-01 follows the external pitch instead of the Merrin Link pitch normal

### External audio enters the space stage

- Default linked path: `MV-03 → AUD_B → MF-01`
- Front patch: external audio cable into `MF-01 AUDIO IN`
- Result: MF-01 processes the external audio instead of the normal Merrin Voice path

## Tiny sound controls

### Brightness

- `Dark`
- `Darker`

This changes the low-pass filtering on the voice preview.

### Echo

- `Short`
- `Long`

This changes the delay timing and feedback on the voice preview.

## v0.5 readability pass

v0.5 improves mobile/page flow and bus readability.

Changes:

- Moves the `Current boundary` card out of the right sidebar
- Makes the boundary card a full-width transition section
- Shortens bus-line descriptions so they are easier to read
- Reduces the large empty gap before the front-panel override examples

## Version notes

### v0.1

Clickable signal guide with five module cards, detail panel, Merrin Link bus panel, and one tiny audio preview.

### v0.2

Adds the Merrin Link jumper view:

- linked voice mode / independent module mode toggle
- active / inactive bus line states
- module jumper notes
- front-panel patch override explanation

### v0.3

Adds front-panel override examples:

- external pitch overrides the Merrin Link pitch normal
- external audio enters the space stage instead of the normal Merrin Voice path

### v0.4

Adds tiny sound controls for the existing Web Audio preview:

- `Brightness`: dark / darker
- `Echo`: short / long

### v0.5

Improves mobile/page flow and bus readability:

- smoother top-to-bottom page flow
- full-width boundary card
- shorter bus-line wording
- reduced empty space before override examples

## Current boundary

This app explains the instrument and includes one tiny audio preview with simple controls.

It does **not** yet:

- provide full synth controls
- save patches
- simulate electronics
- design PCBs
- act as a VCV Rack module
- simulate patch cables
