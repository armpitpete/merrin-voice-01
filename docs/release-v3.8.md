# Merrin Grief Synth v3.8 Release Notes

## Release status

**v3.8 is complete for the current browser demo scope.**

Merrin Grief Synth is a browser-first Web Audio instrument built around one emotional voice: **Constrained Grief**.

This release adds tested MIDI keyboard input without turning the project into a general-purpose synth.

## Live app

https://armpitpete.github.io/merrin-voice-01/

## Completed in v3.8

- MIDI keyboard connection.
- MIDI note-on and note-off handling.
- Same-note retrigger support.
- Fast tapping stability.
- Different-note playing.
- Held notes / small chords within the current voice limit.
- MIDI panic / all-notes-off.
- Raw MIDI monitor.
- MIDI diagnostics toggle.
- Raw monitor detach when diagnostics are hidden.
- MIDI clock and active-sensing spam filtering.
- Duplicate note event filtering.
- Repeated-note overload fix.
- Shape glide fix for Hollow / Pressed source layers.
- README and public docs updated.

## Hardware test summary

Confirmed by live hardware testing:

- MIDI devices connect in Chrome / Edge desktop.
- Note-on starts the existing synth voice.
- Note-off releases the voice.
- Same-note retrigger works.
- Repeated-note playing no longer overloads the app.
- One physical key press is reduced to one useful note-on and one useful note-off when duplicate MIDI routes send repeated copies.
- Diagnostics can be hidden when not needed.

## Browser support

Core Web Audio playback works in modern desktop browsers.

MIDI keyboard input uses the Web MIDI API and should be tested in Chrome or Edge desktop.

MIDI input is not treated as supported on iPad, iPhone, or Safari in this release.

## Out of scope

The following are deliberately not part of v3.8:

- VST plugin work.
- VCV Rack work.
- DAW instrument work.
- Sequencer behaviour.
- Recording.
- MIDI output.
- MIDI channel routing.
- Pitch bend.
- Modulation wheel.
- Sustain pedal behaviour.
- Presets.
- General-purpose synth expansion.

## Demo media

A real audio/video demo should be recorded from the live app and added separately.

Suggested target:

- 20–40 seconds.
- Show one note, same-note retrigger, glide, Shape: Hollow / Pressed, and MIDI input.
- File path suggestion: `assets/demo/merrin-grief-synth-v38-demo.webm` or `assets/demo/merrin-grief-synth-v38-demo.mp4`.

Do not use a simulated or fake demo recording.
