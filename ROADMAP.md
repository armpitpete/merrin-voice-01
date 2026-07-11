# Roadmap

Merrin Grief Synth should stay small and specific.

Its current browser job is complete: a browser-first emotional Web Audio synth for one voice, **Constrained Grief**.

The next lane is not final demo media.

The next lane is to define the whole synth built around the existing Constrained Grief voice.

## Current release

### v3.8 — complete

- Browser synth demo.
- Constrained Grief voice identity.
- On-screen keyboard.
- Computer keyboard input.
- MIDI keyboard input.
- MIDI diagnostics and raw monitor tools.
- Diagnostics visibility toggle.
- Duplicate MIDI filtering.
- Shape glide fixed.
- README and release polish docs.

## Active planning lane

### v4.0 — Whole synth definition

Status: definition pass started.

Spec documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

Purpose:

- Define what the completed Merrin Grief Synth is meant to become.
- Keep Merrin Voice 01 / Constrained Grief as the proven foundation.
- Decide what belongs in the whole instrument before any finish-demo work.
- Protect the project from becoming a general-purpose synth.
- Define the smallest next implementation lane after the definition is accepted.

V4.0 is documentation/specification work only.

Allowed:

- define whole-synth scope
- define final signal path
- define main surface controls
- define diagnostics vs performance controls
- define required emotional behaviours
- define explicit non-goals
- define completion criteria before final demo
- identify the next small implementation lane

Not allowed:

- final demo media
- fake demo media
- new synth controls
- new sound behaviour
- sequencer work
- plugin work
- VCV Rack work
- MIDI output work
- general-purpose synth expansion
- DBHT-1 expansion work
- M A C controller work
- hardware expansion work

## Next likely implementation lane

Only after the V4.0 definition is accepted, the next likely implementation lane is:

```text
V4.1 — Separate performance layer from advanced/test layer
```

This should not add sound features.

## Later finish-demo lane

A real audio/video demo belongs after the whole synth is built and accepted.

Do not record or commit final demo media while the project is still in whole-synth definition.

The later finish-demo lane may include:

- real audio/video demo recording
- browser screenshot or GIF
- release page
- final public portfolio text
- GitHub Release and tag

The demo must show the finished synth, not an unfinished stage.

## Future tracks

Each of these should be treated as a separate project or issue lane, not mixed into the completed v3.8 browser demo or the v4.0 whole-synth specification.

### Possible browser polish

- Hide advanced test controls behind a simple mode.
- Add a clearer beginner "how to play" section.
- Review mobile/tablet display without promising MIDI support there.
- Preserve current sound behaviour.

This should happen only if it supports the whole-synth build and does not pretend to be final demo work.

### Possible sample pack

- Record a small set of Constrained Grief notes and phrases.
- Export labelled WAV files.
- Keep it as an audio asset project, not a synth-code expansion.

This belongs after the whole synth direction is stable.

### Possible VST concept

- Document required controls.
- Define the minimum viable plugin version.
- Do not start until the browser voice and whole-synth scope remain stable.

### Possible VCV Rack concept

- Define a small module identity.
- Keep it emotion-shaped rather than general modular feature creep.

## Explicit non-goals for the current browser demo

- Becoming a general-purpose synth.
- Adding presets.
- Adding sequencer behaviour.
- Adding recording features.
- Adding MIDI output.
- Adding pitch bend or modulation wheel.
- Adding channel routing.
- Adding plugin framework work.
- Adding more sound controls just because they are possible.
