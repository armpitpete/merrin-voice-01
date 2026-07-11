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
- circuit-board synth established as final destination
- final demo media blocked until the hardware stage is honest

Documents:

- [V4.0 — Whole Synth Build Spec](docs/whole-synth-build-spec-v4.0.md)
- [V4.0 — Whole Synth Definition Pass](docs/v4.0-whole-synth-definition-pass.md)

### v4.1 — Performance / advanced layout separation complete

- performance surface shown first
- test/diagnostic controls moved into an advanced area
- no sound-engine expansion

Document:

- [V4.1 — Performance / Advanced Layout Separation](docs/v4.1-performance-advanced-layout.md)

## Completed hardware-definition work

### v5.0 — Hardware Translation Spec

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

Support:

```text
ABSENCE
PRESSURE
BREAK
```

Also locked:

- Memory Core Prototype A first
- external audio as Present
- oscillator/quantizer deferred
- SMD-first electronics
- WQP518MA Thonkiconns
- SLS-1 and HIL-1

Documents:

- [V5.0 — Hardware Translation Spec](docs/v5.0-hardware-translation-spec.md)
- [V5.0 — SMD Construction Rule](docs/v5.0-smd-construction-rule.md)

### v5.1 — Circuit-block design

Locked:

- Memory captures shaped Present after Pressure/Absence
- direct analogue Present bypasses digital core
- mono ADC ingress
- Memory, Ghost and Return DAC outputs
- Return passes through Break, analogue shaping and hard limiting
- only `RETURN_LIMITED` may re-enter Memory
- signal, reset/fault and bench-test requirements

Document:

- [V5.1 — Memory Core Prototype A Circuit-Block Design](docs/v5.1-memory-core-prototype-a-circuit-block-design.md)

### v5.2 — Component architecture

| Function | Selection | Package target |
|---|---|---|
| MCU | STM32H743VIT6 | LQFP-100 |
| Audio converter | PCM3168A | HTQFP-64 |
| Audio op amp | OPA1679 | TSSOP-14 |
| Quad VCA | SSI2164 | SOP-16 |
| VCA control DAC | MCP4728 | MSOP-10 |
| Fail-safe VCA selector | TMUX1574 | TSSOP-16 |
| Supervisor | TPS3808G33 | SOT-23-6 |
| Watchdog | TPS3431 | VSON-8 |
| Buck regulators | TPS62160 | VSSOP-8 |
| Quiet codec LDO | TPS7A2050 | SOT-23-5 |
| Audio jacks | WQP518MA | through-hole PCB mount |
| Default passives | 0805 | 0805 |

Digital architecture:

```text
48 kHz
24-bit conversion
32-bit processing
2.0-second mono history
384,000-byte history buffer
internal MCU SRAM only
```

Documents:

- [V5.2 — Component Architecture](docs/v5.2-prototype-a-component-architecture.md)
- [V5.2 — Safe Selector Amendment](docs/v5.2-component-architecture-amendment-safe-selector.md)
- [V5.2 — Schematic Sheet Plan](docs/v5.2-prototype-a-schematic-sheet-plan.md)
- [V5.2 — Risk Register](docs/v5.2-component-selection-risk-register.md)

### v5.2 — Digital blockers closed

```text
PE2  SAI1_MCLK_A  → codec MCLK
PE3  SAI1_SD_B    ← codec ADC data
PE4  SAI1_FS_A    → codec frame sync
PE5  SAI1_SCK_A   → codec BCLK
PE6  SAI1_SD_A    → codec DAC data

PB8/PB9   I2C1
PA0–PA7   panel ADC
PD8–PD15  safety/user controls
PC6–PC9   SLS-1
```

```text
48 kHz LRCLK
12.288 MHz BCLK
24.576 MHz MCLK
8 × 32-bit TDM
PCM3168A 0x44
MCP4728 0x60
```

Documents:

- [V5.2 — MCU Pin Allocation](docs/v5.2-mcu-pin-allocation-register.md)
- [V5.2 — PCM3168A Proof](docs/v5.2-pcm3168a-clock-and-interface-proof.md)
- [V5.2 — Digital Cross-Check](docs/v5.2-mcu-pin-and-codec-cross-check.md)

## Active lane

### v5.2 — Power and analogue safety calculations

Status: review branch.

Documents:

- [Power, Current and Thermal Budget](docs/v5.2-power-current-and-thermal-budget.md)
- [SSI2164 / MCP4728 Fail-Safe Control](docs/v5.2-ssi2164-mcp4728-fail-safe-control.md)
- [Return Limiter and OPA1679 Allocation](docs/v5.2-return-limiter-and-opamp-allocation.md)
- [Supervisor, Watchdog and Thonkiconn Proof](docs/v5.2-supervisor-watchdog-and-thonkiconn-proof.md)
- [Power and Analogue Preflight](docs/v5.2-power-and-analogue-preflight-register.md)

## Locked power targets

```text
3.3 V design load = 500 mA
quiet 5 V design load = 265 mA
±12 V analogue-core allowance = 100 mA per rail
bench planning:
  +12 V = 425 mA
  −12 V = 110 mA
```

Regulator starting points:

```text
3.3 V rail:
  RTOP = 374 kΩ
  RBOTTOM = 120 kΩ
  nominal = 3.293 V
  L = 2.2 µH
  COUT = 22 µF effective target

quiet-5 V pre-rail:
  RTOP = 698 kΩ
  RBOTTOM = 120 kΩ
  nominal = 5.453 V
  L = 3.3 µH
  COUT = 22 µF effective target
```

The 3.3 µH quiet-pre-rail correction keeps the first-pass design in continuous conduction at the 265 mA load.

## Locked fail-safe VCA control

```text
SSI control range = 0 V to +3.3 V
0 V = unity
+3.3 V ≈ maximum attenuation
negative control forbidden
```

TMUX1574:

```text
safe/default input = +3.3 V
normal input = MCP4728
SEL low = safe
SEL high = normal
hardware fault can force SEL low
```

MCP4728 EEPROM requests `0xFFF` on every channel, but the hardware selector remains authoritative.

## Locked timing distinction

```text
20 ms = asserted fault to wet/Return suppression
```

TPS3431 remains the slower independent hang detector:

```text
approximately 200 ms nominal
approximately 170–230 ms window
```

It does not claim 20 ms hang detection.

## Corrected Return safety

```text
combined small-signal transfer from core Return source
through DAC-R, Break and analogue Return to RETURN_LIMITED
≤ 1.000
```

Hard limit and fixed feed:

```text
RET-01
→ 2.2 kΩ
→ clamp to buffered ±2.5 V references
→ RETURN_LIMITED
→ RIN 40.2 kΩ / RF 27.4 kΩ
→ nominal feed 0.6816
→ 1% worst-case 0.6954
```

Calculated normal loop gain remains below 0.70 and below the 0.85 ceiling.

Headroom:

```text
5.6 Vpp clamp × 0.6816 = 3.82 Vpp Return
3.82 Vpp + 2.00 Vpp Present = 5.82 Vpp
```

This remains below the 6 Vpp internal target.

## OPA1679 count

```text
7 × OPA1679
28 provisional assigned channels
56.0 mA per rail typical
78.4 mA per rail worst-case
```

Native schematic accounting must confirm the allocation.

## WQP518MA status

Accepted for schematic:

```text
pin 1 sleeve
pin 2 tip
pin 3 normally-connected tip switch
```

Still blocked before PCB:

- independent footprint check
- barrel keepout/hole
- panel axis and hardware stack
- physical sample measurement

## Risk state

Closed for schematic preparation:

```text
R3 SSI2164 safety
R4 MCP4728 startup architecture
R6 quiet-5 V calculation
R7 3.3 V budget
R9 OPA1679 count/current
```

Partly closed:

```text
R5 watchdog timing accepted; footprint/assembly open
R8 jack symbol/switching accepted; footprint/mechanical open
R12 Return calculation accepted; schematic/bench proof open
```

Still open:

```text
R2 SRAM/DMA firmware placement
R11 unused codec analogue treatment
```

## Next gate after acceptance

```text
V5.2 — Native hierarchical schematic capture and ERC
```

Hierarchy:

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

- symbols and physical pins verified
- passive values preserve accepted calculations
- all supply pins decoupled
- unused codec analogue inputs correctly terminated
- Return safety independently reviewed
- ERC passes with documented exceptions only

## PCB gate

PCB placement, routing, fabrication and purchasing remain forbidden until:

- hierarchical schematic is complete
- ERC passes
- hardware-relevant risks close
- packages and footprints are independently verified
- WQP518MA panel alignment is accepted
- Return limiter independence is accepted

Only then may the project enter:

```text
V5.3 — Prototype A PCB placement and routing
```

## Later work

Internal voice source begins only after Prototype A proves the grief engine.

No final demo media during component, schematic or PCB work.

## Permanent non-goals

- general-purpose synth expansion
- feature accumulation
- hidden menu dependence
- presets before behaviour is stable
- sequencer expansion
- unrelated plugin work
- allowing the oscillator to become more important than Memory / Ghost / Return
