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
- keyboard and MIDI input
- accepted emotional control language
- diagnostics and safe panic/release behaviour
- functional oscilloscope

### v4.0 — Whole-instrument definition complete

- browser reference separated from final hardware goal
- final destination corrected to circuit-board synth
- no final demo media authorised

Documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

### v4.1 — Performance / advanced layout separation complete

- performance surface shown first
- test and diagnostic controls moved into an advanced area
- no sound-engine changes

Document:

- [V4.1 — Performance / Advanced Layout Separation](docs/v4.1-performance-advanced-layout.md)

## Completed hardware-definition work

### v5.0 — Hardware Translation Spec complete

Locked architecture:

```text
Analogue Present path
+
shared digital Memory / Ghost / Return core
+
analogue nonlinear Return and safety path
```

Locked hardware heart:

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

- Memory Core Prototype A first
- external audio as Prototype A Present
- oscillator/quantizer deferred
- SMD-first electronics
- Thonkiconn-family 3.5 mm audio/CV jacks
- SLS-1 state indication
- HIL-1 layout rules

Documents:

- [V5.0 — Hardware Translation Spec](docs/v5.0-hardware-translation-spec.md)
- [V5.0 — SMD Construction Rule](docs/v5.0-smd-construction-rule.md)

### v5.1 — Memory Core Prototype A circuit-block design complete

V5.1 locked:

- Memory captures shaped Present after Pressure and Absence
- direct analogue Present bypasses the digital core
- one mono ADC ingress
- three DAC outputs: Memory, Ghost, Return send
- Return path must pass through Break, analogue Return shaping, and a hard limiter
- only limited Return may re-enter Memory or influence Absence
- signal-level and gain-staging targets
- boot/reset/mute/fault behaviour
- required test points
- SMD-oriented functional zones
- bench acceptance procedure

Document:

- [V5.1 — Memory Core Prototype A Circuit-Block Design](docs/v5.1-memory-core-prototype-a-circuit-block-design.md)

## Active lane

### v5.2 — Prototype A component architecture

Status: component architecture and schematic-sheet plan in review branch.

Documents:

- [V5.2 — Prototype A Component Architecture](docs/v5.2-prototype-a-component-architecture.md)
- [V5.2 — Prototype A Schematic Sheet Plan](docs/v5.2-prototype-a-schematic-sheet-plan.md)

## Locked V5.2 major components

| Function | Selection | Package target |
|---|---|---|
| MCU | STM32H743VIT6 | LQFP-100 |
| Audio converter | PCM3168A | HTQFP-64 |
| General audio op amp | OPA1679 | TSSOP-14 |
| Quad VCA | SSI2164 | SOP-16 |
| VCA control DAC | MCP4728 | MSOP-10 |
| 3.3 V supervisor | TPS3808G33 | SOT-23-6 |
| External watchdog | TPS3431 | VSON-8 |
| 5 V pre-regulator | TPS62160 | VSSOP-8 |
| 3.3 V regulator | TPS62160 | VSSOP-8 |
| Quiet codec LDO | TPS7A2050 | SOT-23-5 |
| Audio jacks | WQP518MA Thonkiconn | Through-hole PCB mount |
| Default passives | 0805 | 0805 |

0603 passives are allowed only where dense local circuitry makes 0805 impractical.

## Locked digital architecture

```text
48 kHz audio
24-bit PCM3168A conversion
32-bit MCU processing
2.0-second mono circular history
384,000-byte main history buffer
internal MCU SRAM only
```

Ghost and Return derive from the same retained history.

No external SDRAM, PSRAM, sample storage, filesystem, presets, USB audio, or MIDI are included in Prototype A.

## Locked conversion architecture

```text
1 codec ADC channel:
  shaped Present + limited Return

3 codec DAC channels:
  Memory
  Ghost
  Return send
```

The STM32 is audio clock master.

Preferred clock targets:

- 48 kHz LRCLK
- 12.288 MHz BCLK for eight 32-bit TDM slots
- 24.576 MHz MCLK, subject to final codec clock-mode verification

## Locked analogue-control architecture

SSI2164 channel allocation:

| Channel | Function |
|---|---|
| 1 | Memory level |
| 2 | Ghost level |
| 3 | Return level |
| 4 | wet master / hardware attenuation |

MCP4728 supplies normal-operation VCA control voltages.

A separate hardware clamp must force all wet/Return VCA paths to maximum safe attenuation during:

- power-up
- reset
- codec fault
- MCU fault
- watchdog fault

Firmware and stored DAC values cannot override the hardware clamp.

## Locked power architecture

Prototype A accepts protected ±12 V rails.

```text
+12 V → TPS62160 ≈5.5 V → TPS7A2050 → quiet 5 V codec analogue
+12 V → TPS62160 → 3.3 V digital
±12 V direct → OPA1679 / SSI2164 / analogue signal path
```

This is a prototype electrical choice, not a final enclosure-format decision.

## Exact audio jack

Prototype A uses:

```text
WQP518MA Thonkiconn
```

- J1 AUDIO IN
- J2 AUDIO OUT

Switched contacts, symbol pins, footprint, panel axis, and mechanical clearances must be checked against the current manufacturer drawing before PCB routing.

## V5.2 schematic hierarchy

```text
00_TOP
├── 01_POWER_PROTECTION
├── 02_MCU_CLOCK_DEBUG
├── 03_CODEC_CONVERSION
├── 04_INPUT_PRESSURE_ABSENCE
├── 05_MEMORY_GHOST_WET
├── 06_RETURN_BREAK_LIMITER
├── 07_OUTPUT_MUTE_PROTECTION
├── 08_CONTROLS_STATE
└── 09_TEST_SERVICE
```

The Return sheet may export only:

```text
RETURN_LIMITED
ABSENCE_INFLUENCE
```

Raw DAC Return, Break output, and nonlinear Return may not connect to the Memory-input summing node.

## V5.2 allowed work

- major component selection
- practical SMD package targets
- clock/sample-rate architecture
- buffer/resource budget
- power architecture
- watchdog/supervisor architecture
- jack variant selection
- hierarchical schematic planning
- schematic capture
- ERC and schematic review

## V5.2 forbidden work

- PCB placement
- PCB routing
- fabrication files
- purchasing
- production pricing
- oscillator work
- MIDI/CV/keyboard expansion
- display/preset/sequencer work
- final panel/enclosure design
- demo media

## Remaining V5.2 decisions during schematic capture

- exact HSE crystal/oscillator
- exact protection parts
- exact passive values
- regulator inductors and compensation
- exact nonlinear Break/Return devices
- final OPA1679 count
- exact power connector
- verified symbols and footprints
- ERC exceptions, if any

These may be decided only when they preserve the accepted V5.1 behaviour.

## Current stop point

```text
Review and accept the V5.2 component architecture.
```

After acceptance, the next task inside V5.2 is:

```text
Create the hierarchical Prototype A schematic.
```

PCB placement and routing remain blocked until:

- schematic is complete
- ERC passes
- Return safety is independently reviewed
- component packages are verified
- WQP518MA footprint and panel alignment are verified

## Later lanes

### PCB lane

Only after accepted schematic and ERC:

- PCB placement and routing
- ground/reference implementation
- panel alignment
- DRC
- fabrication outputs

### Internal voice source

Only after Memory Core Prototype A proves the grief engine:

- constrained Scale
- Tone / Shape / Sub / Overtone
- Glide / Drift
- Fade / Wither
- internal voice integration into Present

### Finish-demo lane

No final demo media during component, schematic, or PCB work.

A later demo must be honestly labelled as browser reference or hardware prototype.

## Permanent non-goals

- general-purpose synth expansion
- feature accumulation
- hidden menu dependence
- presets before behaviour is stable
- sequencer expansion
- unrelated plugin work
- allowing the oscillator to become more important than Memory / Ghost / Return
