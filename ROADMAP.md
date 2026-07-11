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
- circuit-board synth established as the final destination
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

Hardware heart:

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
- signal-level, reset/fault and bench-test requirements

Document:

- [V5.1 — Memory Core Prototype A Circuit-Block Design](docs/v5.1-memory-core-prototype-a-circuit-block-design.md)

### v5.2 — Component architecture complete

Major selections:

| Function | Selection | Package target |
|---|---|---|
| MCU | STM32H743VIT6 | LQFP-100 |
| Audio converter | PCM3168A | HTQFP-64 |
| Audio op amp | OPA1679 | TSSOP-14 |
| Quad VCA | SSI2164 | SOP-16 |
| VCA control DAC | MCP4728 | MSOP-10 |
| Safe VCA-control selector | TMUX1574 | TSSOP-16 |
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

### v5.2 — Digital schematic blockers closed

Exact MCU allocation:

```text
PE2  SAI1_MCLK_A  → codec MCLK
PE3  SAI1_SD_B    ← codec ADC data
PE4  SAI1_FS_A    → codec frame sync
PE5  SAI1_SCK_A   → codec BCLK
PE6  SAI1_SD_A    → codec DAC data

PB8/PB9   shared I2C1 control bus
PA0–PA7   eight panel ADC controls
PD8–PD15  safety and operating controls
PC6–PC9   SLS-1 state outputs
```

Exact codec transport:

```text
48 kHz LRCLK
12.288 MHz BCLK
24.576 MHz MCLK
8 × 32-bit TDM slots
PCM3168A address 0x44
MCP4728 address 0x60
```

Documents:

- [V5.2 — MCU Pin Allocation Register](docs/v5.2-mcu-pin-allocation-register.md)
- [V5.2 — PCM3168A Clock and Interface Proof](docs/v5.2-pcm3168a-clock-and-interface-proof.md)
- [V5.2 — MCU Pin and Codec Configuration Cross-Check](docs/v5.2-mcu-pin-and-codec-cross-check.md)

Closed for schematic preparation:

```text
R1  PCM3168A clock/configuration
R10 STM32H743VIT6 pin allocation
```

## Active lane

### v5.2 — Power and analogue safety calculations

Status: review branch.

Documents:

- [V5.2 — Prototype A Power, Current and Thermal Budget](docs/v5.2-power-current-and-thermal-budget.md)
- [V5.2 — SSI2164 / MCP4728 Fail-Safe Control](docs/v5.2-ssi2164-mcp4728-fail-safe-control.md)
- [V5.2 — Return Limiter and OPA1679 Allocation](docs/v5.2-return-limiter-and-opamp-allocation.md)
- [V5.2 — Supervisor, Watchdog and Thonkiconn Proof](docs/v5.2-supervisor-watchdog-and-thonkiconn-proof.md)

### Locked power targets

```text
3.3 V design load = 500 mA
quiet 5 V design load = 265 mA
±12 V analogue-core allowance = 100 mA per rail
prototype bench allocation:
  +12 V = 425 mA
  −12 V = 110 mA
```

TPS62160 starting values:

```text
3.3 V rail:
  RTOP = 374 kΩ
  RBOTTOM = 120 kΩ
  nominal = 3.293 V

5 V pre-rail:
  RTOP = 698 kΩ
  RBOTTOM = 120 kΩ
  nominal = 5.453 V

both rails:
  L = 2.2 µH
  CIN = 10 µF local minimum target
  COUT = 22 µF effective target
```

### Locked fail-safe VCA control

```text
SSI2164 control range = 0 V to +3.3 V
0 V    = unity maximum
+3.3 V = approximately −100 dB attenuation
negative control voltage forbidden
```

TMUX1574 selection:

```text
safe/default input = +3.3 V attenuation reference
normal input = MCP4728 output
SEL low = safe attenuation
SEL high = normal DAC control
hardware fault can always force SEL low
```

MCP4728 EEPROM safe request:

```text
VREF = VDD
GAIN = 1
normal mode
all four DAC codes = 0xFFF
```

The EEPROM state is secondary; the hardware selector is authoritative.

### Locked timing interpretation

```text
20 ms requirement = asserted fault to wet/Return suppression
```

TPS3431 remains the slower independent MCU-hang detector:

```text
approximately 200 ms nominal
approximately 170–230 ms documented window
```

It does not claim to detect a frozen MCU within 20 ms.

### Locked Return safety

```text
RET-01
→ 2.2 kΩ series resistor
→ Schottky clamp to buffered ±2.5 V references
→ RETURN_LIMITED
→ fixed feed gain 30.1 kΩ / 40.2 kΩ
→ nominal magnitude 0.7488
→ 1% worst-case approximately 0.764
```

SSI Return gain cannot exceed unity, so calculated normal small-signal loop gain remains below 0.85.

Only `RETURN_LIMITED` may cross the Return-sheet feedback boundary.

### Locked OPA1679 count

```text
7 × OPA1679
28 assigned channels
56.0 mA per rail typical
78.4 mA per rail worst-case
```

No casual spare op-amp package is authorised.

### WQP518MA status

Accepted for schematic:

```text
pin 1 sleeve
pin 2 tip
pin 3 normally-connected tip switch
```

Still required before PCB:

- independent footprint check against current manufacturer drawing
- barrel keepout/hole check
- panel axis and nut/washer clearance
- physical sample measurement

A community library marked incomplete is reference-only.

## Risk state after this lane

Closed for schematic preparation:

```text
R3  SSI2164 control safety
R4  MCP4728 startup architecture
R6  quiet 5 V rail calculation
R7  3.3 V current budget
R9  OPA1679 count/current
```

Partially closed:

```text
R5  watchdog timing accepted; footprint/assembly open
R8  jack symbol/switching accepted; footprint/mechanical open
R12 Return calculation accepted; schematic/bench proof open
```

Still open:

```text
R2  SRAM/DMA firmware placement
R11 unused codec analogue treatment
```

## Next gate after acceptance

```text
V5.2 — Native hierarchical schematic capture and ERC
```

Schematic capture must use the accepted hierarchy:

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

Before schematic acceptance:

- every selected symbol and physical pin is verified
- passive values preserve the accepted calculations
- every supply pin is decoupled
- unused codec analogue inputs are terminated correctly
- Return safety is independently reviewed
- ERC passes with only documented intentional exceptions

## PCB gate

PCB placement, routing, fabrication and purchasing remain forbidden until:

- the hierarchical schematic is complete
- ERC passes
- hardware-relevant risks are closed
- component packages are independently verified
- WQP518MA footprint and panel alignment are accepted
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
