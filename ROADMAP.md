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
- final demo media blocked until the hardware stage is honest

Documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

### v4.1 — Performance / advanced layout separation complete

- performance surface shown first
- diagnostic/test controls moved into an advanced area
- no sound-engine expansion

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

Also locked:

- Memory Core Prototype A first
- external audio as Prototype A Present
- oscillator and quantizer deferred
- SMD-first electronics
- WQP518MA/Thonkiconn 3.5 mm audio jacks
- SLS-1 state indication
- HIL-1 layout rules

Documents:

- [V5.0 — Hardware Translation Spec](docs/v5.0-hardware-translation-spec.md)
- [V5.0 — SMD Construction Rule](docs/v5.0-smd-construction-rule.md)

### v5.1 — Prototype A circuit-block design complete

Locked:

- Memory captures shaped Present after Pressure and Absence
- direct analogue Present bypasses the digital core
- one mono ADC ingress
- three DAC outputs: Memory, Ghost, Return send
- Return passes through Break, analogue shaping and hard limiting
- only `RETURN_LIMITED` may re-enter Memory or influence Absence
- signal-level and gain-staging targets
- boot/reset/mute/fault behaviour
- test points and bench acceptance procedure

Document:

- [V5.1 — Memory Core Prototype A Circuit-Block Design](docs/v5.1-memory-core-prototype-a-circuit-block-design.md)

### v5.2 — Component architecture accepted

Major selections:

| Function | Selection | Package target |
|---|---|---|
| MCU | STM32H743VIT6 | LQFP-100 |
| Audio converter | PCM3168A | HTQFP-64 |
| Audio op amp | OPA1679 | TSSOP-14 |
| Quad VCA | SSI2164 | SOP-16 |
| VCA control DAC | MCP4728 | MSOP-10 |
| 3.3 V supervisor | TPS3808G33 | SOT-23-6 |
| External watchdog | TPS3431 | VSON-8 |
| 5 V / 3.3 V pre-regulators | TPS62160 | VSSOP-8 |
| Quiet codec LDO | TPS7A2050 | SOT-23-5 |
| Audio jacks | WQP518MA Thonkiconn | through-hole PCB mount |
| Default passives | 0805 | 0805 |

Locked digital architecture:

```text
48 kHz audio
24-bit conversion
32-bit MCU processing
2.0-second mono circular history
384,000-byte history buffer
internal MCU SRAM only
```

Documents:

- [V5.2 — Prototype A Component Architecture](docs/v5.2-prototype-a-component-architecture.md)
- [V5.2 — Prototype A Schematic Sheet Plan](docs/v5.2-prototype-a-schematic-sheet-plan.md)
- [V5.2 — Component-Selection Risk Register](docs/v5.2-component-selection-risk-register.md)

### v5.2 — Schematic-capture preparation registers complete

Preparation records define the evidence gates for:

- MCU pin allocation
- codec clock/serial configuration
- current and thermal budgets
- SSI2164 clamp safety
- Return limiter independence
- watchdog/supervisor timing
- WQP518MA symbol/footprint verification

Documents:

- [V5.2 — Schematic Capture Preparation Review](docs/v5.2-schematic-capture-preparation-review.md)
- [V5.2 — MCU Pin Allocation Register](docs/v5.2-mcu-pin-allocation-register.md)
- [V5.2 — PCM3168A Clock and Interface Proof](docs/v5.2-pcm3168a-clock-and-interface-proof.md)
- [V5.2 — Power and Analogue Preflight Register](docs/v5.2-power-and-analogue-preflight-register.md)

## Active lane

### v5.2 — MCU pin and codec configuration proof

Status: review branch.

This lane closes the two digital schematic blockers without creating unvalidated KiCad files.

### Exact STM32 allocation

```text
PE2  SAI1_MCLK_A  → codec MCLK
PE3  SAI1_SD_B    ← codec ADC data
PE4  SAI1_FS_A    → codec frame sync
PE5  SAI1_SCK_A   → codec BCLK
PE6  SAI1_SD_A    → codec DAC data

PB8  I2C1_SCL
PB9  I2C1_SDA

PA0–PA7   eight panel ADC controls
PD8–PD15  safety and operating controls
PC6–PC9   SLS-1 state outputs

PH0/PH1   HSE reserved
PA13/PA14 SWD reserved
NRST       hardware reset reserved
```

Spare ADC pins PB0/PB1 and spare GPIO PB12–PB15 remain available but unallocated.

### Exact PCM3168A transport

```text
48 kHz LRCLK
12.288 MHz BCLK
24.576 MHz MCLK
8 × 32-bit TDM slots
24 significant bits
PCM3168A I2C address 0x44
MCP4728 I2C address 0x60
```

TDM use:

```text
DAC1 Memory
DAC2 Ghost
DAC3 Return send
ADC1 shaped Present + RETURN_LIMITED
```

Unused converters are muted, powered down where supported, and excluded from the Memory/wet paths.

Documents:

- [V5.2 — MCU Pin Allocation Register](docs/v5.2-mcu-pin-allocation-register.md)
- [V5.2 — PCM3168A Clock and Interface Proof](docs/v5.2-pcm3168a-clock-and-interface-proof.md)
- [V5.2 — MCU Pin and Codec Configuration Cross-Check](docs/v5.2-mcu-pin-and-codec-cross-check.md)

Closed for schematic preparation:

```text
R1  PCM3168A clock/configuration
R10 STM32H743VIT6 pin allocation
```

Partially closed:

```text
R11 unused codec channel digital state
```

R11 analogue termination remains a schematic task.

## Next bounded lane after acceptance

```text
V5.2 — Power and analogue safety calculations
```

Required work:

- 3.3 V typical/worst-case current budget
- quiet 5 V codec rail current, dropout and dissipation
- TPS62160 current/inductor/ripple calculations
- OPA1679 package/channel and ±12 V current count
- SSI2164 gain-law, safe attenuation and clamp network
- MCP4728 startup scaling
- TPS3808/TPS3431 timing
- independent analogue Return limiter and loop-gain calculation
- WQP518MA symbol/switching/footprint proof

That lane may select passive values required by the calculations.

It must still not begin PCB placement or routing.

## Native schematic gate

Native KiCad schematic capture may begin only when the remaining preflight calculations are explicit enough that the sheets do not hide unresolved safety behaviour.

Before schematic acceptance:

- every selected symbol and physical pin must be verified
- every supply pin must be decoupled
- unused codec analogue inputs must be terminated correctly
- Return safety must be independently reviewed
- ERC must pass with only documented intentional exceptions

## PCB gate

PCB placement and routing remain forbidden until:

- the hierarchical schematic is complete
- ERC passes
- every hardware-relevant risk is closed
- component packages are verified
- WQP518MA footprint and panel alignment are verified
- Return limiter independence is accepted

Only then may the project enter:

```text
V5.3 — Prototype A PCB placement and routing
```

## Later work

### Internal voice source

Only after Memory Core Prototype A proves the grief engine:

- constrained Scale
- Tone / Shape / Sub / Overtone
- Glide / Drift
- Fade / Wither
- internal voice integration into Present

### Finish-demo lane

No final demo media during component, schematic or PCB work.

A later demo must be honestly labelled as either:

- browser reference demonstration; or
- hardware prototype demonstration.

## Permanent non-goals

- general-purpose synth expansion
- feature accumulation
- hidden menu dependence
- presets before behaviour is stable
- sequencer expansion
- unrelated plugin work
- allowing the oscillator to become more important than Memory / Ghost / Return
