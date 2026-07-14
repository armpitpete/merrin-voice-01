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
05_MEMORY_GHOST_WET COMPLETE / ERC VALIDATED
07_OUTPUT_MUTE_PROTECTION COMPLETE / ERC VALIDATED
09_TEST_SERVICE COMPLETE / ERC VALIDATED
00_TOP FINAL INTEGRATED REVIEW COMPLETE / ERC VALIDATED
PR #45 SCHEMATIC ACCEPTANCE REVIEW COMPLETE
FOOTPRINT / PCB / FABRICATION / PURCHASING BLOCKED
```

This folder contains the native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

The V5.2 component-level schematic-capture lane is complete. All nine sheets and the final integrated hierarchy pass committed-file validation and KiCad ERC.

The design remains a reviewed prototype schematic candidate, not production-ready hardware. Exact parts, footprints, measured behaviour, placement, routing, mechanics, fabrication and purchasing remain separate gates.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch       CAPTURED / ERC VALIDATED
├── 02_MCU_CLOCK_DEBUG.kicad_sch        CAPTURED / ERC VALIDATED
├── 03_CODEC_CONVERSION.kicad_sch       CAPTURED / ERC VALIDATED
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch CAPTURED / ERC VALIDATED
├── 05_MEMORY_GHOST_WET.kicad_sch       CAPTURED / ERC VALIDATED
├── 06_RETURN_BREAK_LIMITER.kicad_sch   CAPTURED / ERC VALIDATED
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch CAPTURED / ERC VALIDATED
├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED
└── 09_TEST_SERVICE.kicad_sch           CAPTURED / ERC VALIDATED
```

## Locked interface constraints

- Direct Present remains outside the digital core.
- Memory captures shaped Present after Pressure and Absence.
- PCM3168A conversion uses one ADC ingress and three DAC roles: Memory, Ghost and Return send.
- Return passes through Break, analogue Return shaping and the independent limiter boundary.
- Sheet 06 may export only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`.
- Sheet 05 consumes only the accepted Memory/Ghost DAC and SSI2164 control signals and exports only `WET_MIX`.
- U60 is one physical SSI2164: units 1/2/4 are on sheet 05; units 3/5 are on sheet 06.
- U32 is one physical OPA1679: units 1/5 are on sheet 03; units 2/3/4 are on sheet 07.
- Sheet 07 consumes only `DIRECT_PRESENT`, `WET_MIX`, `HARDWARE_FAULT_N` and the accepted ±12 V rails.
- Sheet 07 exports no hierarchical audio or control net; the protected output jack remains local.
- Sheet 09 consumes eight accepted read-only service signals and exports no hierarchy net.
- `SERVICE_TEST`, `RESET_CLEAR`, and `SAFE_MUTE` remain operating signals between sheets 08 and 02, not sheet-09 service commands.
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

The final hierarchy review is recorded in `00_TOP_FINAL_INTEGRATED_REVIEW.md`. The PR-level schematic, footprint, bench and merge decision is recorded in `PR45_SCHEMATIC_ACCEPTANCE_REVIEW.md`.

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
- measured SSI2164 control range across the integrated sheet-05 and sheet-06 channels.

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
single U60 device split across sheet 05 units 1/2/4 and sheet 06 units 3/5
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
- measured complete loop gain and polarity;
- fault-neutralisation and rail-sequencing proof;
- 30-minute worst-setting endurance test.

## Captured sheet 05 — Memory / Ghost / Wet

Captured signal route:

```text
MEMORY_DAC → SSI2164 channel 1 → OPA1679 I/V ┐
                                               ├→ equal half-sum
GHOST_DAC  → SSI2164 channel 2 → OPA1679 I/V ┘
                                               ↓
                                    SSI2164 channel 4 wet master
                                               ↓
                                            WET_MIX
```

Locked shared-device ownership:

```text
U60 unit 1 = Memory channel 1   pins 2 IIN1, 3 VC1, 4 IOUT1
U60 unit 2 = Ghost channel 2    pins 7 IIN2, 6 VC2, 5 IOUT2
U60 unit 3 = Return channel 3   pins 15 IIN3, 14 VC3, 13 IOUT3   sheet 06
U60 unit 4 = wet-master channel pins 10 IIN4, 11 VC4, 12 IOUT4
U60 unit 5 = common power       sheet 06
```

Locked wet-sum relationship:

```text
Memory input resistor = 40.2 kΩ
Ghost input resistor  = 40.2 kΩ
feedback resistor     = 20.0 kΩ

branch magnitude = 20.0 / 40.2 ≈ 0.4975
two equal full-scale branches ≈ 0.995 total
```

Validation:

```text
native generation passed
hierarchy and WET_MIX-only export contract passed
SSI2164 symbol and official physical-pin contract passed
single-device five-unit U60 ownership contract passed
no duplicate SSI2164 physical device created
KiCad 10 hierarchical ERC passed
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
integrated Return workflow rerun passed with generation skipped
```

Still open:

- exact SSI2164 SOP-16 footprint and independent package-pin review;
- exact OPA1679 TSSOP-14 footprint review;
- exact coupling, stability and decoupling capacitor selections;
- measured Memory and Ghost VCA control laws;
- measured Memory/Ghost branch gain and wet-sum headroom;
- measured wet-master attenuation range, noise, distortion and recovery;
- integrated analogue loop gain and safety bench gates;
- PCB placement, routing and all physical implementation gates.

## Captured sheet 07 — Output / Mute / Protection

Captured signal route:

```text
DIRECT_PRESENT ─40.2 kΩ─┐
                         ├─ U32B equal half-sum
WET_MIX       ─40.2 kΩ─┘        ↓
                         passive output level
                                ↓
                         U32C level buffer
                                ↓
                         fail-muted JFET shunt
                                ↓
                         U32D post-mute driver
                                ↓
                         AC coupling + output protection
                                ↓
                         logical WQP518MA mono output
```

Locked output relationship:

```text
Direct input resistor = 40.2 kΩ
Wet input resistor    = 40.2 kΩ
feedback resistor     = 20.0 kΩ

per-branch magnitude = 20.0 / 40.2 ≈ 0.4975
6 Vpp Direct + 6 Vpp Wet calculated maximum ≈ 5.97 Vpp
passive output level can only attenuate
```

Locked shared-device ownership:

```text
U32 unit 1 = Return converter A — sheet 03
U32 unit 2 = final half-sum B — sheet 07
U32 unit 3 = output-level buffer C — sheet 07
U32 unit 4 = post-mute driver D — sheet 07
U32 unit 5 = common power — sheet 03
```

Fail-muted control:

```text
fault or undefined HARDWARE_FAULT_N → optocoupler on → MUTE_GATE toward 0 V → shunt mute on
healthy HARDWARE_FAULT_N → optocoupler off → MUTE_GATE toward −10.91 V
healthy release time constant ≈ 90.9 ms
first-pass 50% CTR fault-clamp estimate ≈ 12.7 ms
```

Validation:

```text
native sheet-03 / sheet-07 generation passed
no-export hierarchy contract passed
shared five-unit U32 ownership and official-pin contract passed
seven physical OPA1679 package allocation passed
Direct/Wet gain and calculated output-headroom contract passed
fail-muted control and first-pass timing contract passed
provisional control symbols use explicit logical pins and blank footprints
logical WQP518MA output boundary passed
KiCad 10 hierarchical ERC passed
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
```

Still open:

- exact OPA1679 TSSOP-14 footprint review;
- exact J113-class mute device, pin map, footprint, `VGS(off)` and on-resistance spread;
- exact optocoupler and NPN fault-inverter parts and packages;
- asymmetric rail-arrival and rail-loss behaviour;
- exact output-level potentiometer and WQP518MA physical pin/footprint review;
- panel alignment and jack clearance;
- measured output level, load drive, noise and distortion;
- measured mute depth, fault timing, release timing and pop behaviour;
- measured output-clamp current, back-power behaviour and endurance;
- all PCB placement, routing and physical implementation gates.

## Captured sheet 09 — Test / Service

Captured read-only access:

```text
RAIL_3V3          → 1 kΩ probe isolation
HARDWARE_FAULT_N  → 47 kΩ probe isolation
SHAPED_PRESENT    → 22 kΩ probe isolation
ADC_ANALOG_IN     → 22 kΩ probe isolation
RETURN_LIMITED    → 22 kΩ probe isolation
RETURN_FEED       → 22 kΩ probe isolation
ABSENCE_INFLUENCE → 22 kΩ probe isolation
WET_MIX           → 22 kΩ probe isolation
```

The isolated probe nodes feed individual test points `TP900` through `TP907`. `TP908` provides service ground. A logical ten-position header or pad grouping provides the eight probe nodes plus two grounds; it has no accepted footprint.

Locked hierarchy boundary:

```text
inputs:  RAIL_3V3, HARDWARE_FAULT_N, SHAPED_PRESENT, ADC_ANALOG_IN,
         RETURN_LIMITED, RETURN_FEED, ABSENCE_INFLUENCE, WET_MIX
outputs: none
```

First-pass isolation calculations:

```text
3.3 V through 1 kΩ short limit ≈ 3.3 mA
3.3 V through 47 kΩ ≈ 70.2 µA
22 kΩ into a 10 MΩ instrument adds approximately 0.22% loading
```

Validation:

```text
native read-only service capture passed
eight-input / no-output hierarchy contract passed
eight probe branches and nine test points passed
logical ten-position service header pin map passed
blank connector-footprint boundary passed
former temporary interface harness removed
KiCad 10 hierarchical ERC passed across all nine sheets
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
```

Still open:

- exact service connector or pad format;
- production fixture architecture;
- test-point footprints and access clearances;
- current-measurement links for major power branches;
- measured probe loading and fault-injection limits;
- all PCB placement, routing and mechanical implementation gates.

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

Final component-capture policy:

```text
0 ERC errors required
0 ERC warnings required
all nine component sheets required
parent and child hierarchy directions must match
former temporary harnesses forbidden
```

All nine component sheets and `00_TOP` report `0 errors, 0 warnings` from committed files.

## Completed capture order

```text
[x] 01_POWER_PROTECTION
[x] 08_CONTROLS_STATE
[x] 02_MCU_CLOCK_DEBUG
[x] 03_CODEC_CONVERSION
[x] 06_RETURN_BREAK_LIMITER
[x] 04_INPUT_PRESSURE_ABSENCE
[x] 05_MEMORY_GHOST_WET
[x] 07_OUTPUT_MUTE_PROTECTION
[x] 09_TEST_SERVICE
[x] 00_TOP final interface and ERC review
[x] PR #45 schematic acceptance and transferred-gate review
```

The recommended merge strategy for PR #45 is a deliberate squash merge after human review. The PR remains draft. Exact-part and footprint verification must begin in a separate later lane and may return assumptions to schematic review.

## Still blocked

- exact footprint acceptance;
- PCB placement;
- PCB routing;
- fabrication outputs;
- parts purchasing;
- production pricing;
- final mechanical layout;
- oscillator or internal voice-source work;
- MIDI/CV expansion;
- sequencer work;
- demo media.

## Gate before PCB work

PCB work may begin only after:

- PR #45 is deliberately reviewed and merged;
- exact manufacturer parts and package pin maps are verified;
- exact footprints receive independent review;
- WQP518MA / Thonkiconn mechanical alignment is proven;
- Return loop, limiter and fault behaviour pass the transferred bench gates;
- output mute, sequencing, load, clamp and endurance behaviour pass the transferred bench gates;
- remaining hardware risks are closed or transferred to explicit bounded tests with acceptance criteria.

Passing the schematic gate does not authorise PCB work.