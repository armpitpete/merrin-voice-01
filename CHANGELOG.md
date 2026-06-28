# Changelog

All notable project changes are summarised here.

## v3.8 — MIDI keyboard input complete

Status: accepted.

### Added

- Browser MIDI connection control.
- MIDI keyboard note-on and note-off support.
- MIDI note mapping into the existing Constrained Grief voice engine.
- Simple velocity response.
- MIDI diagnostics panel.
- Raw MIDI monitor.
- MIDI panic / all-notes-off control.
- MIDI diagnostics show/hide toggle.
- Raw MIDI monitor listener detach when diagnostics are hidden.
- Duplicate MIDI note filtering for devices or routes that send repeated identical events.
- README preview image.
- Release notes and public polish docs.

### Fixed

- Same-note MIDI retrigger behaviour.
- Repeated-note overload caused by MIDI real-time diagnostic spam.
- Layout shrink caused by MIDI diagnostics panels.
- Shape-source glide split, where Hollow / Pressed layers could jump to the target note while the main voice glided.
- Duplicate MIDI note-on / note-off events from one physical key press.

### Confirmed

- MIDI device connection.
- Note-on starts the voice.
- Note-off releases the voice.
- Same-note retrigger.
- Fast tapping.
- Different notes.
- Held notes / small chords within the current voice limit.
- MIDI panic.
- Repeated-note overload stability.
- Diagnostics toggle.
- Raw MIDI monitor detach.
- Duplicate MIDI event filtering.

### Out of scope

- VST plugin work.
- VCV Rack work.
- Sequencer work.
- Recording features.
- MIDI output.
- MIDI channel routing.
- Pitch bend.
- Modulation wheel.
- Sustain pedal behaviour.
- General-purpose synth expansion.

## v3.7 — Documentation and project framing

Status: accepted.

- README updated to reflect the browser-demo state.
- Project name reframed as Merrin Grief Synth.
- Current controls and boundaries documented.
- Live app link included.
- Larger synth/plugin directions kept separate from the current release.

## v3.6 — Voice source shaping and layout acceptance

Status: accepted.

- Shape added: Pure / Hollow / Pressed.
- Sub refined as weight, not bass boom.
- Overtone refined as ache, not brightness.
- Slight Drift added.
- Delayed tremble deferred.
- Landscape layout cleanup accepted.

## v3.5 — Voice balance and output safety

Status: accepted.

- Balanced the playable voice so it stayed controlled, safe, mournful, and usable.

## v3.4 — Continuous gate polish

Status: accepted.

- Improved press-and-release note behaviour so the app worked more like a playable instrument.

## v3.3 — Canon and emotion-shaped controls

Status: accepted.

- Added the main playable control set.
- Added diagnostic switches.
- Added active note display.
- Added basic oscilloscope support.
