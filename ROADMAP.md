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
- diagnostics and safe panic/release behaviour
- accepted emotional control language
- functional oscilloscope

### v4.0 — Whole-instrument definition complete

- browser reference separated from final hardware goal
- final destination corrected to circuit-board synth
- performance controls separated conceptually from diagnostics
- no final demo media authorised

Documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

### v4.1 — Performance / advanced layout separation complete

- public performance surface shown first
- panic/release and MIDI status remain visible
- test and diagnostic controls moved into an advanced area
- no sound-engine changes
- no demo media

Document:

- [V4.1 — Performance / Advanced Layout Separation](docs/v4.1-performance-advanced-layout.md)

## Completed hardware-definition work

### v5.0 — Hardware Translation Spec complete

The hardware direction is locked as:

```text
Analogue Present path
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

Support blocks:

```text
ABSENCE
PRESSURE
BREAK
```

V5.0 also locked:

- Memory Core Prototype A as the first hardware build
- external audio as the Prototype A Present source
- oscillator and quantizer work deferred
- SMD-first electronic construction
- through-hole mechanical exceptions only where appropriate
- Thonkiconn-family 3.5 mm PCB-mount jacks as the default audio/CV connector
- exact components, packages, jack variants, and footprints deferred
- SLS-1 state-light requirements
- HIL-1 layout requirements
- no schematic or PCB work in V5.0

Documents:

- [V5.0 — Hardware Translation Spec](docs/v5.0-hardware-translation-spec.md)
- [V5.0 — SMD Construction Rule](docs/v5.0-smd-construction-rule.md)

## Active lane

### v5.1 — Memory Core Prototype A circuit-block design

Status: draft in review branch.

Document:

- [V5.1 — Memory Core Prototype A Circuit-Block Design](docs/v5.1-memory-core-prototype-a-circuit-block-design.md)

Purpose:

- define detailed functional blocks
- define signal direction and capture points
- define signal-level targets
- define gain staging
- define ADC/DAC functional boundaries
- define Return safety and bounded feedback
- define boot/reset/mute/fault behaviour
- define test points
- define SMD-oriented functional zones
- define Thonkiconn audio-jack roles
- define bench acceptance tests

## Locked V5.1 refinement

Memory captures the shaped Present signal after Pressure and Absence.

```text
Raw input
  ↓
Pressure
  ↓
Absence
  ↓
Shaped Present
  ├── direct analogue Present path
  └── Memory-input summing node
```

Limited Return re-enters only through the Memory-input summing node.

Raw Return may not bypass:

```text
Break
↓
analogue Return nonlinearity
↓
hard Return limiter
```

## V5.1 signal targets

Prototype A targets:

- expected external input range of approximately 0.2–10 Vpp after trim
- non-damaging input survival within ±12 V at the jack
- 2 Vpp nominal internal analogue audio
- at least 6 Vpp internal headroom before unintended clipping
- approximately −12 dBFS nominal converter ingress
- below −3 dBFS converter peak target before intended limiting
- approximately 2 Vpp nominal output
- no more than 10 Vpp maximum normal output
- approximately 0.85 maximum normal small-signal Return loop gain
- bounded complete Return behaviour at every valid setting

These are prototype design targets, not final production-format claims.

## V5.1 functional conversion channels

The design requires:

```text
1 functional mono ADC ingress
3 functional DAC outputs:
  Memory
  Ghost
  Return send
```

The exact converter device count and architecture remain deferred.

## V5.1 safety rules

- direct Present bypasses the digital core
- boot begins with wet and Return paths muted
- reset forces Return to zero before clearing Memory
- core fault forces ERROR-MUTED
- hard Return limiting remains active independently of normal DSP behaviour
- final output remains independently controllable
- no path may bypass the Return limiter

## V5.1 allowed work

- circuit-block architecture
- interface and level targets
- functional conversion-channel count
- safety logic
- test-point requirements
- bench procedure
- SMD-oriented circuit partitioning
- jack-role definition

## V5.1 forbidden work

- exact component selection
- processor, ADC, DAC, or codec selection
- resistor/capacitor values
- exact SMD packages
- exact Thonkiconn variant or footprint
- schematic capture
- KiCad project creation
- PCB placement or routing
- BOM
- purchasing
- oscillator work
- MIDI/CV expansion
- final panel/enclosure work
- demo media

## Next lane after V5.1 acceptance

```text
V5.2 — Prototype A schematic and component-selection lane
```

V5.2 may:

- select active and passive parts
- select practical SMD packages
- select exact Thonkiconn variants and verified footprints
- select converter and control architecture
- capture the schematic
- run ERC and schematic-stage checks

V5.2 must not begin PCB placement or routing until the schematic, Return safety paths, and ERC results are accepted.

## Later lanes

### PCB lane

Only after accepted schematic and ERC:

- PCB placement
- routing
- ground/reference implementation
- panel alignment
- design-rule checking
- fabrication outputs

### Internal voice-source translation

Only after Memory Core Prototype A proves the grief engine:

- constrained Scale behaviour
- Tone / Shape / Sub / Overtone
- Glide / Drift
- Fade / Wither and the Lingering Voice envelope
- internal voice integration into Present

### Physical format decision

Do not lock final packaging before prototype evidence.

Possible later formats:

- integrated desktop instrument
- core voice plus separate effects
- linked Eurorack boards/modules

### Finish-demo lane

Do not record final demo media during architecture, circuit-block, schematic, or PCB work.

A later demo must be labelled honestly as either:

- browser reference demonstration, or
- hardware prototype demonstration

It must not present the browser reference as the finished circuit-board instrument.

## Permanent non-goals

- becoming a general-purpose synth
- adding features because they are possible
- hiding important behaviour behind menus
- presets before behaviour is stable
- sequencer expansion
- unrelated plugin frameworks
- allowing the oscillator to become more important than Memory / Ghost / Return
