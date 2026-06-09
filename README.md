# Merrin Voice 01 — Constrained Grief

Merrin Voice 01 is a playable browser synth demo built around one emotional voice:

> constrained grief — dark, slow, weighted, fragile, lingering, remembered

It is not a general-purpose synth. It is a small Web Audio instrument for testing one focused sound identity.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Current status

**v3.7 documentation pass complete.**

The app itself is accepted at the current v3.6 browser-demo state.

This version includes:

- playable browser synth
- continuous gate notes
- on-screen keyboard
- computer keyboard support
- active note buttons
- amplitude slider
- live oscilloscope accepted as basic/functional
- Shape: Pure / Hollow / Pressed
- Sub refined as weight, not bass boom
- Overtone refined as ache, not brightness
- slight Drift
- accepted landscape layout cleanup

## What this is

Merrin Voice 01 is a browser-based synth demo.

It runs directly in the browser using Web Audio. It is hosted on GitHub Pages and does not require a build step.

The app is useful for:

- testing the Merrin Voice 01 sound identity
- playing a small constrained voice
- checking how the controls shape the emotional character
- proving the instrument idea before larger synth/plugin work

## What this is not

This is not yet:

- a VST plugin
- a VCV Rack module
- a DAW instrument
- a preset synth
- a sequencer
- a MIDI controller app
- a patch-cable simulator
- a full modular synth system

## Main controls

### Playable controls

- **Tone** — changes the voice from darker to brighter within the allowed emotional range.
- **Fade** — changes how quickly the note arrives and disappears.
- **Echo** — changes the remembered/distant quality of the sound.
- **Amplitude** — controls output level.

### Voice-shaping controls

- **Shape** — Pure / Hollow / Pressed.
- **Sub** — adds weight without turning into bass boom.
- **Overtone** — adds ache without becoming bright or shiny.
- **Drift** — adds slight instability.

### Emotion-shaped controls

- **Scale** — chooses the pitch field.
- **Glide** — controls how notes slide.
- **Weight** — changes the heaviness of the sound.
- **Wither** — controls fragile movement in the voice.

### Test controls

- **All effects off** — gives a cleaner baseline for checking the sound.
- **Normal voice** — restores the accepted voice shape.
- **Effect test switches** — allow individual sound parts to be checked.

## Keyboard support

The app can be played with:

- the on-screen note buttons
- a computer keyboard

The note buttons light up while active, so the player can see which notes are sounding.

## Oscilloscope

The app includes a live oscilloscope.

It is accepted as basic and functional. Its job is to show that the waveform is alive and responding. It is not intended to be a full laboratory-grade scope.

## Design boundary

Do not expand this version into a general synth.

Avoid adding:

- presets
- MIDI
- sequencer features
- plugin framework work
- extra controls
- more layout polish
- delayed tremble work

The current accepted job is complete: a focused playable browser demo for **Merrin Voice 01 — Constrained Grief**.

## Release notes

### v3.7 — Final release notes and project README

Documentation pass.

- README updated to reflect the accepted v3.6 browser-demo state.
- Current controls and boundaries documented.
- Live app link included.
- Project clearly described as a browser synth demo, not a plugin or DAW instrument.

No sound, control, or layout changes.

### v3.6 — Voice source shaping and layout acceptance

Accepted current playable state.

- Shape added: Pure / Hollow / Pressed.
- Sub refined as weight, not bass boom.
- Overtone refined as ache, not brightness.
- Slight Drift added.
- Delayed tremble deferred.
- Landscape layout cleanup accepted.

### v3.5 — Voice balance and output safety

Balanced the playable voice so it stayed controlled, safe, mournful, and usable.

### v3.4 — Continuous gate polish

Improved press-and-release note behaviour so the app worked more like a playable instrument.

### v3.3 — Canon and emotion-shaped controls

Added the main playable control set, diagnostic switches, active note display, and basic oscilloscope support.

## Final note

Merrin Voice 01 should stay small and specific.

Its value is not feature count. Its value is the focused emotional voice.
