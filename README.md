# Merrin Grief Synth — Constrained Grief

Merrin Grief Synth is a playable browser synth demo built around one emotional voice:

> constrained grief — dark, slow, weighted, fragile, lingering, remembered

It is not a general-purpose synth. It is a small Web Audio instrument for testing one focused sound identity.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Current status

**v3.8 MIDI input complete.**

The app is accepted as a browser-first Web Audio synth demo with MIDI keyboard input.

This version includes:

- playable browser synth
- continuous gate notes
- on-screen keyboard
- computer keyboard support
- MIDI keyboard input
- MIDI diagnostics and raw monitor tools
- MIDI panic / all-notes-off control
- active note buttons
- amplitude slider
- live oscilloscope accepted as basic/functional
- Shape: Pure / Hollow / Pressed
- Sub refined as weight, not bass boom
- Overtone refined as ache, not brightness
- slight Drift
- accepted landscape layout cleanup

## What this is

Merrin Grief Synth is a browser-based synth demo.

It runs directly in the browser using Web Audio. It is hosted on GitHub Pages and does not require a build step.

The app is useful for:

- testing the Merrin Grief Synth sound identity
- playing a small constrained voice
- checking how the controls shape the emotional character
- testing MIDI keyboard input against the same focused voice
- proving the instrument idea before larger synth/plugin work

## Current scope

This release is a browser-first Web Audio demo. Larger formats and systems can be treated as separate future tracks if the core voice proves useful.

Possible later directions include:

- VST plugin
- VCV Rack module
- DAW instrument
- preset synth
- sequencer
- MIDI controller app
- patch-cable simulator
- full modular synth system

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
- **MIDI diagnostics** — helps inspect MIDI note-on, note-off, and voice state while testing hardware input.
- **Raw MIDI monitor** — shows raw note/control messages while filtering MIDI clock and active-sensing spam.
- **MIDI panic** — releases all notes if a connected MIDI device misbehaves.

## Input support

The app can be played with:

- the on-screen note buttons
- a computer keyboard
- a USB/MIDI keyboard in supported desktop browsers

The note buttons light up while active, so the player can see which notes are sounding.

MIDI input has been tested for:

- device connection
- note-on
- note-off
- same-note retrigger
- fast tapping
- different notes
- held notes / small chords
- panic / all-notes-off
- repeated-note overload stability

## Browser support

Core browser synth playback works in modern desktop browsers that support Web Audio.

MIDI keyboard input uses the browser Web MIDI API. Use Chrome or Edge desktop for MIDI testing and playing.

MIDI input is not treated as supported on iPad, iPhone, or Safari in this version.

## Oscilloscope

The app includes a live oscilloscope.

It is accepted as basic and functional. Its job is to show that the waveform is alive and responding. It is not intended to be a full laboratory-grade scope.

## Design boundary

Do not expand this version into a general synth.

Avoid adding:

- presets
- sequencer features
- plugin framework work
- extra sound controls
- more layout polish
- pitch bend
- modulation wheel
- sustain pedal behaviour
- MIDI output
- MIDI channel routing
- recording
- delayed tremble work

The current accepted job is complete: a focused playable browser demo for **Merrin Grief Synth — Constrained Grief** with basic MIDI keyboard input.

## Release notes

### v3.8 — MIDI keyboard input

MIDI input pass.

- Added browser MIDI connection control.
- Added MIDI keyboard note-on and note-off support.
- Mapped MIDI note input to the existing synth voice engine.
- Kept the Constrained Grief sound path unchanged.
- Added simple velocity response.
- Added MIDI diagnostics, raw MIDI monitor, and MIDI panic tools.
- Fixed MIDI layout regression so diagnostics no longer shrink the synth controls.
- Fixed same-note retrigger behaviour.
- Fixed repeated-note overload by filtering MIDI real-time diagnostic spam.
- Confirmed MIDI reliability test pass after hardware testing.

No general synth expansion, sequencer work, plugin work, pitch bend, modulation wheel, MIDI output, recording, or channel-routing work.

### v3.7 — Final release notes and project README

Documentation pass.

- README updated to reflect the accepted v3.6 browser-demo state.
- Current controls and boundaries documented.
- Live app link included.
- Project clearly described as a browser synth demo, with larger synth/plugin directions kept separate from the current release.

No sound, control, or layout changes.

### v3.6 — Voice source shaping and layout acceptance

Accepted playable browser-synth state before MIDI.

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

Merrin Grief Synth should stay small and specific.

Its value is not feature count. Its value is the focused emotional voice.
