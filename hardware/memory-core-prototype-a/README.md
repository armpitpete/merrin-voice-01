# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
01_POWER_PROTECTION COMPLETE / ERC VALIDATED
08_CONTROLS_STATE COMPLETE / ERC VALIDATED
02_MCU_CLOCK_DEBUG COMPLETE / ERC VALIDATED
03_CODEC_CONVERSION COMPLETE / ERC VALIDATED
06_RETURN_BREAK_LIMITER COMPLETE / ERC VALIDATED
04_INPUT_PRESSURE_ABSENCE COMPLETE / ERC VALIDATED
05_MEMORY_GHOST_WET NEXT
PCB WORK BLOCKED
```

This folder contains the native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

Component-level circuitry is being added one sheet at a time. Full hierarchical ERC is run after each bounded capture.

The project is not yet a completed hardware schematic or production-ready design.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch       CAPTURED / ERC VALIDATED
├── 02_MCU_CLOCK_DEBUG.kicad_sch        CAPTURED / ERC VALIDATED
├── 03_CODEC_CONVERSION.kicad_sch       CAPTURED / ERC VALIDATED
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch CAPTURED / ERC VALIDATED
├── 05_MEMORY_GHOST_WET.kicad_sch       NEXT CAPTURE
├── 06_RETURN_BREAK_LIMITER.kicad_sch   CAPTURED / ERC VALIDATED
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD
├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED
└── 09_TEST_SERVICE.kicad_sch           INTERFACE SCAFFOLD
```

## Locked interface constraints

- Direct Present remains outside the digital core.
- Memory captures shaped Present after Pressure and Absence.
- PCM3168A conversion uses one ADC ingress and three DAC roles: Memory, Ghost and Return send.
- Return passes through Break, analogue Return shaping and the independent limiter boundary.
- Sheet 06 may export only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`.
- Sheet 04 accepts only fixed `RETURN_FEED` and bounded `ABSENCE_INFLUENCE` from sheet 06.
- Direct Present splits after protected, AC-coupled unity buffering and before Pressure or Absence.
- `ADC_ANALOG_IN` is formed only from `SHAPED_PRESENT` plus fixed `RETURN_FEED`.
- Raw Return, Break, limiter-internal and clamp nets remain excluded from sheet 04.
- `WATCHDOG_HEARTBEAT` enters the power/protection and hardware-fault system.
- TMUX1574 safe-control release remains a controls/safety-sheet responsibility.
- Eight panel controls and three operating inputs are explicit signals between sheets 08 and 02.
- Global ground is established from sheet 01 and shared by captured sheets.
- Captured analogue sheets receive the accepted ±12 V rails.

The machine-readable interface list is stored in `hierarchy-manifest.json`.

## Captured sheet 01 — Power / Protection

Captured protected ±12 V entry, regulated 3.3 V and quiet 5 V domains, supervision, watchdog, `HARDWARE_FAULT_N`, test points and global GND.

Validation:

```text
0 ERC errors
no temporary interface-harness warnings on 01_POWER_PROTECTION
```

Still open:

- active-device footprints;
- exact inductors, capacitors, protection parts and connector;
- capacitor derating and copper-dependent thermal checks;
- TPS3431 VSON land-pattern and assembly verification.

## Captured sheet 08 — Controls / State / Safe Selector

Captured MCP4728 normal controls, TMUX1574 fail-safe selection, hardware-fault override, four bounded SSI2164 controls, eight panel ADC controls, operating inputs and SLS-1 state drivers.

Locked selector rule:

```text
SEL low  = +3.3 V safe attenuation
SEL high = MCP4728 normal control
HARDWARE_FAULT_N low forces SEL low
```

Validation:

```text
0 ERC errors
no temporary interface-harness warnings on 08_CONTROLS_STATE
```

Still open:

- exact MCP4728 and TMUX1574 footprints;
- exact panel controls, LEDs and transistor parts;
- measured release/fault timing;
- MCP4728 EEPROM and bring-up proof;
- measured SSI2164 control range after sheets 05 and 06 are integrated.

## Captured sheet 02 — MCU / Clock / Debug

Captured the STM32H743VIT6 LQFP-100 physical-pin map, SAI1 TDM transport, I²C1, panel/safety/state signals, supplies, references, 24.576 MHz HSE bypass source, SWD and unused-pin treatment.

Validation:

```text
100 physical MCU pins encoded
selected-pin contract passed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 02_MCU_CLOCK_DEBUG
committed-file rerun passed with generation skipped
```

Still open:

- exact STM32H743VIT6 footprint verification;
- exact 24.576 MHz oscillator and footprint;
- decoupling physical placement;
- oscillator signal-integrity review;
- SWD connector choice and mechanics;
- CubeMX `.ioc` and generated clock-tree proof;
- measured MCLK/BCLK/LRCLK timing;
- SRAM/DMA linker placement and firmware resource proof.

## Captured sheet 03 — Codec / Conversion

Captured PCM3168A power/control/TDM, one differential ADC ingress, Memory/Ghost/Return DAC reconstruction, analogue level translation, and explicit unused-channel treatment.

Locked ADC level relationship:

```text
2 Vpp internal nominal
→ 1.333 Vpp differential ADC input
→ approximately −12.6 dBFS

6 Vpp internal headroom limit
→ 4.0 Vpp differential ADC input
→ approximately −3.0 dBFS
```

Locked DAC filter basis:

```text
TI Figure 61
R1 = 7.5 kΩ
R2 = 5.6 kΩ
R3 = 360 Ω
C1 = 3.3 nF
C2 = 680 pF
gain ≈ 0.747
f−3 dB ≈ 53 kHz
```

Validation:

```text
64 PCM3168A pins plus PowerPAD encoded
codec hierarchy and selected-pin contract passed
project-local PCM3168A and OPA1679 symbols parsed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 03_CODEC_CONVERSION
committed-file rerun passed with generation skipped
```

Still open:

- exact PCM3168A HTQFP-64 PowerPAD footprint verification;
- exact OPA1679 TSSOP-14 footprint verification;
- exact ferrite, coupling and reference capacitors;
- measured ADC full-scale and filter response;
- measured DAC reconstruction response and gain;
- codec register readback and inactive-channel firmware proof;
- measured reset/mute sequencing and pop behaviour;
- PowerPAD thermal-via and ground-plane review.

## Captured sheet 06 — Return / Break / Limiter

Captured signal route:

```text
RETURN_DAC
  ↓
SSI2164 channel 3 Return VCA
  ↓
OPA1679 current-to-voltage stage
  ↓
bounded Break stage
  ↓
unity Return normaliser
  ↓
independent dual-polarity limiter
  ↓
RETURN_LIMITED
  ├── fixed 0.6816 RETURN_FEED
  └── bounded ABSENCE_INFLUENCE
```

Locked limiter/feed relationship:

```text
buffered references: ±2.5 V
plus Schottky forward drop
→ approximately 5.4–5.6 Vpp at RETURN_LIMITED

RETURN_FEED magnitude
= 27.4 kΩ / 40.2 kΩ
= 0.6816 nominal
< 0.696 at 1% resistor worst case

5.6 Vpp × 0.6816
≈ 3.82 Vpp maximum nominal RETURN_FEED
```

Validation:

```text
SSI2164 channel-3 and power pin coordinates explicitly checked
all five SSI2164 schematic units present
fixed-feed resistor/value contract passed
restricted-export contract passed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 06_RETURN_BREAK_LIMITER
committed-file rerun passed with generation and repair skipped
```

Still open:

- exact SSI2164 SOP-16 footprint and physical-pin review;
- exact OPA1679 TSSOP-14 footprints;
- exact soft-clip, Schottky and control-clamp diode selections;
- measured SSI2164 control law and unity-gain point;
- measured Break and normaliser gain;
- measured limiter thresholds and recovery;
- measured complete loop gain;
- independent Return safety review after integrated analogue capture;
- 30-minute worst-setting endurance test;
- replacement of reserved SSI2164 units when sheet 05 is captured.

## Captured sheet 04 — Input / Pressure / Absence

Captured signal route:

```text
WQP518MA / Thonkiconn input
  ↓
quiet no-cable normal
  ↓
series protection + rail clamps + RF rejection
  ↓
AC coupling + unity input buffer
  ├── DIRECT_PRESENT
  └── Pressure
        ↓
      Return-derived Absence attenuation
        ↓
      SHAPED_PRESENT
        ↓
      inverting unity Memory sum with fixed RETURN_FEED
        ↓
      ADC buffer and 47 Ω isolation
        ↓
      ADC_ANALOG_IN
```

Captured functions:

- switched mono input-jack application symbol;
- grounded normal contact for deterministic quiet no-cable operation;
- 1 kΩ input protection, ±12 V Schottky rail clamps, 1 MΩ reference and 220 pF RF filtering;
- AC coupling and post-coupling bias;
- unity OPA1679 input buffer;
- isolated `DIRECT_PRESENT` split before Pressure and Absence;
- unity inverting Pressure stage with feedback soft clipping and controlled high-frequency loss;
- bounded `ABSENCE_INFLUENCE` mapping to approximately −8 V through 0 V JFET gate drive;
- J113-class shunt attenuation after Pressure;
- buffered `SHAPED_PRESENT`;
- equal-resistor inverting Memory sum using only `SHAPED_PRESENT` and fixed `RETURN_FEED`;
- final ADC buffer and isolation;
- test points across the complete ingress and shaping chain.

Locked Memory-input relationship:

```text
ADC_ANALOG_IN = -(SHAPED_PRESENT + RETURN_FEED)

shaped input resistor = 20 kΩ
fixed Return input resistor = 20 kΩ
feedback resistor = 20 kΩ
```

The inverting Memory sum restores the accepted loop polarity from the inverting sheet-06 `RETURN_FEED`.

Validation:

```text
input/output hierarchy contract passed
restricted Return-import contract passed
quiet normal and Direct Present split captured
Pressure resistor equality captured
Absence control mapping captured
Memory-sum resistor equality captured
ADC buffer/export boundary repaired and checked
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 04_INPUT_PRESSURE_ABSENCE
committed-file rerun passed with generation and repair skipped
```

Still open:

- independent WQP518MA physical-pin and footprint verification;
- Thonkiconn mechanical alignment and panel clearance;
- exact input-clamp and Pressure diode selections;
- exact J113-class device, pin map, footprint and `VGS(off)` spread;
- measured no-cable noise and plug-in transient behaviour;
- measured input impedance and overvoltage current;
- measured Pressure threshold, symmetry, gain and bandwidth;
- measured Absence control law, attenuation, distortion and recovery;
- measured Memory-sum headroom and full loop polarity/gain;
- bench confirmation that Direct Present remains unaffected by Pressure, Absence and Return.

## ERC policy

The schematic is checked with:

```text
KiCad CLI 10.0.4
official KiCad CI container
pinned container digest
```

Current staged-capture policy:

```text
0 ERC errors required
isolated_pin_label warnings allowed only on sheets that remain temporary scaffolds
captured sheets may not retain temporary interface-harness warnings
```

Remaining scaffold warnings are temporary and are not accepted permanent exceptions.

## Active capture order

```text
[x] 01_POWER_PROTECTION
[x] 08_CONTROLS_STATE
[x] 02_MCU_CLOCK_DEBUG
[x] 03_CODEC_CONVERSION
[x] 06_RETURN_BREAK_LIMITER
[x] 04_INPUT_PRESSURE_ABSENCE
[ ] 05_MEMORY_GHOST_WET        NEXT
[ ] 07_OUTPUT_MUTE_PROTECTION
[ ] 09_TEST_SERVICE
[ ] 00_TOP final interface and ERC review
```

Sheet 05 must capture the Memory, Ghost and wet analogue paths, consume `MEMORY_DAC`, `GHOST_DAC`, and the three accepted SSI2164 control signals, replace the reserved SSI2164 channel placeholders currently held on sheet 06, and export only `WET_MIX`.

## Still blocked

- PCB placement
- PCB routing
- fabrication outputs
- parts purchasing
- production pricing
- final mechanical layout
- oscillator or internal voice-source work
- MIDI/CV expansion
- sequencer work
- demo media

## Gate before PCB work

PCB work may begin only after:

- all nine sheets contain accepted component-level circuitry;
- hierarchical ERC passes;
- every symbol pin and package is verified;
- exact footprints receive independent review;
- WQP518MA mechanical alignment is proven;
- Return safety receives schematic-stage independent review;
- remaining hardware risks are closed or transferred to explicit bounded bench tests.
