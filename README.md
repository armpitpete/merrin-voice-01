# Merrin Voice 01

Interactive browser app for explaining and playing the **Merrin Voice 01 — Constrained Grief** synth voice.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Current status

**v3.3 is complete.**

Merrin Voice 01 is now a playable one-emotion synth test app. It keeps the voice inside the locked emotional field: constrained grief.

The app currently supports:

- playable browser synth voice
- clean raw sine baseline test mode
- emotion-shaped controls
- individual effect test switches
- live stable oscilloscope
- active note display on the keyboard
- full chromatic scale
- visible Fade envelope values
- Wither delay testing

## One-emotion identity

Merrin Voice 01 is not a generic synth.

It is a constrained melancholic voice shaped through:

```text
Scale → Tone → Envelope → Room → Memory
```

Controls should stay inside this field:

- darker
- slower
- more distant
- more fragile
- more weighted
- more lingering
- more unstable
- more remembered

Avoid directions that turn it into a generic bright synth, aggressive lead, snappy pluck, sparkly reverb, or clean hi-fi delay.

## Current app

- Single static `index.html`
- No framework
- No build step
- Runs directly in the browser
- Uses Web Audio
- Hosted on GitHub Pages

## Main controls

### Playable controls

- `Tone` — Dark / Soft / Bright
- `Fade` — Short / Linger / Long
- `Echo` — Near / Deep / Memory

### Emotion-shaped controls

- `Scale` — Natural Minor / Harmonic Minor / Chromatic
- `Glide` — Slow / Slower / Heavy
- `Weight` — Light / Weighted / Deep
- `Wither` — Still / Tremble / Frail

## Scales

### Natural Minor

```text
C · D · Eb · F · G · Ab · Bb · C
```

Keyboard shortcuts:

```text
A S D F G H J K
```

### Harmonic Minor

```text
C · D · Eb · F · G · Ab · B · C
```

Keyboard shortcuts:

```text
A S D F G H J K
```

### Chromatic

```text
C · C# · D · Eb · E · F · F# · G · Ab · A · Bb · B · C
```

Keyboard shortcuts:

```text
A W S E D F T G Y H U J K
```

## Fade envelope readout

The app now shows the envelope values for the selected Fade mode.

Current values:

```text
Short  → Attack 180 ms · Hold 250 ms  · Release end 1250 ms
Linger → Attack 550 ms · Hold 1100 ms · Release end 3200 ms
Long   → Attack 900 ms · Hold 2100 ms · Release end 5400 ms
```

This makes Fade easier to test without adding more controls.

## Wither delay

The Wither section includes a delay slider:

```text
0–1200 ms
```

Purpose:

```text
0 ms      → Wither starts immediately
450 ms    → Wither starts after the note has settled
800+ ms   → Wither arrives late in the fade
```

## Effect test switches

The app includes diagnostic switches so the sound can be tested from a clean sine baseline.

Available effect switches:

- `Sub`
- `Overtone`
- `Filter`
- `Glide`
- `Wither`
- `Room`
- `Echo`

Test workflow:

```text
1. Press All effects off.
2. Confirm clean sine.
3. Turn on one effect.
4. Play notes.
5. Listen for the unwanted behaviour.
6. Turn that effect off.
7. Test the next effect.
```

## Oscilloscope

The app includes a live stable oscilloscope.

Purpose:

- show the waveform while the sound is playing
- lock to the wave so the display is readable
- support testing raw sine vs shaped voice output

## Active note display

When notes are played, the matching on-screen note buttons light up.

This supports overlapping note tests, for example:

```text
Fade: Long
Press C, E, G quickly
```

The active buttons clear after their own fade time.

## Locked signal path

```text
CV → MV-02 → MV-01 → MV-03 → MF-01 → MF-02 → Output
Gate → MV-03
```

## Module order

1. `MV-02` — Melancholy Quantizer / Scale
2. `MV-01` — Somber Oscillator / Tone
3. `MV-03` — Lingering Voice / Envelope
4. `MF-01` — Desolate Space / Room
5. `MF-02` — Fading Echoes / Memory

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

### v0.6

Adds selected module bus focus:

- highlights relevant Merrin Link bus lines when a module is selected
- adds a short focus note showing which bus lines the selected module uses
- keeps the app as a teaching page, not a patch simulator

### v0.7

Adds guided signal path walkthrough controls:

- `Previous stage`
- `Next stage`
- selected module follows the walkthrough
- module detail and bus focus update with the current stage

### v0.8

Adds a clickable walkthrough stage progress strip:

- `Scale`
- `Tone`
- `Envelope`
- `Room`
- `Memory`
- active chip follows the selected stage
- clicking a chip jumps directly to that stage

### v0.9

Adds a compact whole-voice summary panel:

- shows `Scale → Tone → Envelope → Room → Memory`
- gives each stage a plain one-line explanation
- helps the user understand the full voice path at a glance

### v1.0

Release check and freeze:

- visible app label updated to v1.0
- footer updated to v1.0
- summary card label updated to v1.0
- README updated to v1.0
- stable teaching baseline preserved

### v2.0

Design decision:

- full controls should be playable and still support understanding
- v1.0 teaching guide remains preserved as the baseline
- first playable build should stay small

### v2.1

Adds playable controls:

- `Tone`: dark / soft / bright
- `Fade`: short / linger / long
- `Echo`: near / deep / memory
- controls affect the Web Audio voice sample
- each control has a plain explanation sentence

### v2.2

Links playable controls to teaching stages:

- `Tone` focuses `MV-01` / Tone
- `Fade` focuses `MV-03` / Envelope
- `Echo` focuses `MF-02` / Memory
- walkthrough sentence, stage chip, and bus focus update with the matching stage

### v3.0

Creates the fully working synth roadmap:

- v3.1 real playable note engine
- v3.2 proper synth engine state
- v3.3 canon / emotion-shaped controls
- v3.4 presets / patch memory
- v3.5 performance polish

### v3.1

Adds the first real playable note engine:

- fixed one-octave on-screen keyboard
- click/tap note playback
- computer keyboard support
- pitch changes per note
- envelope triggers per note
- Tone / Fade / Echo still affect the sound

### v3.2

Refactors the browser synth into a cleaner engine shape:

- one shared synth state
- clean tone settings function
- clean fade settings function
- clean echo settings function
- one shared note trigger function
- voice sample button and keyboard both use the same note engine
- existing sound and controls remain in place

### v3.3

Adds canon / emotion-shaped controls and testing tools:

- `Scale`: Natural Minor / Harmonic Minor / Chromatic
- `Glide`: Slow / Slower / Heavy
- `Weight`: Light / Weighted / Deep
- `Wither`: Still / Tremble / Frail
- full chromatic keyboard
- active note highlighting
- clean sine baseline test mode
- individual effect test switches
- Wither delay slider
- visible Fade envelope readout
- live stable oscilloscope

## Current boundary

This app is now a playable browser synth prototype and diagnostic test surface for Merrin Voice 01.

It does **not** yet:

- save patches
- provide presets
- include MIDI
- include a sequencer
- include octave switching
- include plugin framework
- simulate patch cables
- simulate electronics
- design PCBs
- act as a VCV Rack module
