# Roadmap

Merrin Grief Synth should stay small and specific.

The browser instrument is the accepted proof-of-voice and control reference for **Constrained Grief**.

The final destination is a real circuit-board synth.

```text
Browser version = proof-of-voice / control reference.
Hardware version = final destination.
```

## Completed browser-reference work

### v3.8 — Voice and MIDI reference complete

- Constrained Grief voice identity
- on-screen keyboard
- computer keyboard input
- MIDI keyboard input
- MIDI diagnostics and raw monitor tools
- duplicate MIDI filtering
- Shape / Sub / Overtone / Drift
- Tone / Fade / Echo / Amplitude
- Scale / Glide / Weight / Wither
- functional oscilloscope
- safe release and MIDI panic behaviour

### v4.0 — Whole-instrument definition complete

- browser reference separated from final hardware goal
- final destination corrected to circuit-board synth
- performance controls separated conceptually from diagnostics
- no final demo media authorised

Spec documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

### v4.1 — Performance / advanced layout separation complete

- public performance surface shown first
- panic/release remains visible
- MIDI connection/status remains visible
- effect tests, Wither delay, and diagnostics moved into advanced/test area
- no sound-engine changes
- no demo media
- project goal corrected in the repo

Spec document:

- [V4.1 — Performance / Advanced Layout Separation](docs/v4.1-performance-advanced-layout.md)

## Active lane

### v5.0 — Hardware Translation Spec

Status: draft in progress.

Spec documents:

- [V5.0 — Hardware Translation Spec](docs/v5.0-hardware-translation-spec.md)
- [V5.0 — SMD Construction Rule](docs/v5.0-smd-construction-rule.md)

Purpose:

- translate the accepted browser reference into a circuit-board synth architecture
- preserve Merrin Voice 01 / Constrained Grief identity
- reconcile the established `Scale → Tone → Envelope → Room → Memory` canon with the newer hardware-heart decision
- lock the analogue / digital / hybrid split
- lock the Memory / Ghost / Return interaction
- define Absence, Pressure, and Break as hardware behaviours
- lock SMD-first electronic construction
- define the first prototype boundary
- define the next circuit-design lane

## Locked V5.0 direction

The hardware direction is hybrid.

```text
Analogue present path
+
shared digital Memory / Ghost / Return core
+
analogue nonlinear Return and safety path
```

The defining heart is:

```text
MEMORY
GHOST
RETURN
```

Support states/blocks:

```text
ABSENCE
PRESSURE
BREAK
```

Oscillators and quantisation are secondary support systems.

They must not be built before the grief engine is proven.

## Locked construction method

Merrin Grief Synth circuit boards are SMD-first.

```text
Electronic circuitry = surface mount by default.
Panel/mechanical hardware = through-hole where appropriate.
```

Through-hole exceptions may include:

- potentiometers
- jacks
- switches
- encoders
- power and board connectors
- programming/service headers
- test points
- mechanically stressed parts
- parts not reasonably available in SMD

Exact SMD packages remain deferred until component and schematic selection.

The later design should favour practical, inspectable, repairable SMD packages rather than unnecessarily tiny parts.

## First hardware prototype

```text
Memory Core Prototype A
```

Prototype A uses external audio as the Present signal.

Its job is to prove:

- Memory retains and degrades sound
- Ghost is derived from Memory and feels thin/detached
- Return alters future Memory behaviour
- Return influences Absence
- Pressure and Break create controlled damage
- feedback and reset remain safe

Prototype A is an SMD-first hardware design.

Temporary development headers, panel controls, and jacks may be through-hole, but the signal-processing and control circuitry must target SMD implementation.

Prototype A is not the final synth, oscillator board, final panel, or production PCB.

## V5.0 allowed work

- functional architecture
- analogue/digital boundaries
- signal-flow definition
- control-language translation
- SLS-1 state-light requirements
- HIL-1 panel-layout requirements
- SMD-first construction rules
- safety/reset requirements
- prototype boundary
- acceptance tests

## V5.0 forbidden work

- KiCad
- schematic capture
- PCB layout
- processor or component selection
- exact footprint/package selection
- BOM
- hardware shopping
- oscillator-board design
- final enclosure design
- demo media
- DBHT-1 expansion
- M A C work
- VST or VCV work
- sequencer work
- presets
- recording/export

## Next lane after V5.0 acceptance

```text
V5.1 — Memory Core Prototype A circuit-block design
```

V5.1 should define:

- detailed block boundaries
- signal levels
- gain staging
- conversion boundaries
- Return safety path
- reset/mute path
- test points
- bench acceptance procedure
- SMD-oriented circuit partitioning

V5.1 still should not begin PCB layout.

Schematic design follows only after the circuit-block design is accepted.

## Later lanes

### Internal voice-source translation

Only after Memory Core Prototype A proves the grief engine:

- translate constrained Scale behaviour
- translate Tone / Shape / Sub / Overtone
- translate Glide / Drift
- translate Fade / Wither and the Lingering Voice envelope
- decide how the internal voice joins the Present input

### Physical format decision

Do not decide final packaging before prototype evidence.

Later options may be evaluated against the evidence:

- integrated desktop instrument
- core voice plus separate effects
- linked Eurorack boards/modules

### Finish-demo lane

Do not record final demo media during hardware translation.

A later demo must be labelled honestly as either:

- browser reference demonstration, or
- hardware prototype demonstration

It must not present the browser reference as the finished circuit-board instrument.

## Permanent non-goals

- becoming a general-purpose synth
- adding features because they are technically possible
- hiding important behaviour behind menus
- presets before the instrument behaviour is stable
- sequencer expansion
- unrelated plugin frameworks
- allowing the oscillator to become more important than Memory / Ghost / Return
