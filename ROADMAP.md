# Roadmap

Merrin Grief Synth should stay small and specific.

Its current browser job is complete: a browser-first emotional Web Audio proof-of-voice for one voice, **Constrained Grief**.

The browser synth is the reference instrument.

The long-term goal is a real circuit-board synth.

```text
Browser version = proof-of-voice / control reference.
Hardware version = final destination.
```

The next lane is not final demo media.

The next lane is to make the browser reference clean enough to translate into hardware.

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

## Active implementation lane

### v4.1 — Performance / advanced layout separation

Status: PR open.

Spec documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)
- [V4.1 — Performance / Advanced Layout Separation](docs/v4.1-performance-advanced-layout.md)

Purpose:

- Keep Merrin Voice 01 / Constrained Grief as the proven foundation.
- Treat the browser synth as the accepted proof-of-voice and control reference.
- Make the performance surface clear before hardware translation.
- Move browser/test/diagnostic controls into an advanced/test layer.
- Protect the project from becoming a general-purpose synth.
- Prepare for a later hardware translation spec.

V4.1 is layout/clarity work only.

Allowed:

- separate performance layer from advanced/test layer
- keep panic/release visible
- keep MIDI connection/status visible
- keep diagnostics available but advanced
- preserve current sound behaviour
- clarify browser-reference / hardware-destination status in docs

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
- PCB layout
- schematic design
- part selection
- BOM
- KiCad files
- hardware expansion work

## Next likely lane after V4.1

Only after V4.1 is accepted, the next real lane is:

```text
V5.0 — Hardware Translation Spec
```

V5.0 should translate the accepted browser reference into a circuit-board synth architecture.

V5.0 should decide:

- analogue / digital / hybrid split
- voice block architecture
- control scanning / MIDI / CV handling
- panel controls
- safety/reset behaviour
- LED/state behaviour using SLS-1
- panel/layout behaviour using HIL-1
- prototype boundary
- first-board scope

V5.0 should not start by opening KiCad.

## Later finish-demo lane

A real audio/video demo belongs after the reference/hardware stage is honest.

Do not record or commit final demo media while the project is still in browser-reference cleanup or hardware translation.

The later finish-demo lane may include:

- real audio/video demo recording
- browser reference walkthrough if clearly labelled as reference
- hardware prototype demo once hardware exists
- screenshot or GIF
- release page
- final public portfolio text
- GitHub Release and tag

The demo must not make a browser reference look like a finished hardware instrument.

## Future tracks

Each of these should be treated as a separate project or issue lane, not mixed into the current browser reference cleanup or the hardware translation spec.

### Possible browser reference polish

- Add a clearer beginner "how to play" section.
- Review mobile/tablet display without promising MIDI support there.
- Preserve current sound behaviour.
- Keep the page honest that it is a reference instrument.

### Possible sample pack

- Record a small set of Constrained Grief notes and phrases.
- Export labelled WAV files.
- Keep it as an audio asset project, not a synth-code expansion.

This belongs after the reference direction is stable.

### Possible VST concept

- Document required controls.
- Define the minimum viable plugin version.
- Do not start until the browser reference, whole-synth scope, and hardware direction remain stable.

### Possible VCV Rack concept

- Define a small module identity.
- Keep it emotion-shaped rather than general modular feature creep.

## Explicit non-goals for the current browser reference

- Becoming a general-purpose synth.
- Adding presets.
- Adding sequencer behaviour.
- Adding recording features.
- Adding MIDI output.
- Adding pitch bend or modulation wheel.
- Adding channel routing.
- Adding plugin framework work.
- Adding more sound controls just because they are possible.
- Pretending the browser reference is the final circuit-board synth.
