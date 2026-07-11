# 07_OUTPUT_MUTE_PROTECTION — Validation Record

## Status

```text
GENERATED ARTIFACT: PASS
HIERARCHY / NO-EXPORT CONTRACT: PASS
OUTPUT GAIN / HEADROOM CONTRACT: PASS
FAIL-MUTE CONTROL CONTRACT: PASS
OPA1679 SYMBOL / PHYSICAL-PIN CONTRACT: PASS
SHARED MULTI-UNIT DEVICE CONTRACT: PASS
PROVISIONAL CONTROL-SYMBOL CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PASS — 0 ERRORS / 0 WARNINGS
COMMITTED-FILE RERUN: PASS — GENERATION SKIPPED
PCB / FOOTPRINT / MECHANICAL AUTHORITY: NOT GRANTED
```

## Locked sheet boundary

Inputs:

```text
RAIL_P12
RAIL_N12
DIRECT_PRESENT
WET_MIX
HARDWARE_FAULT_N
```

No audio or control net leaves sheet 07 through the hierarchy. The protected output jack, output-level node, mute nodes and protection nodes are local to this sheet.

## Shared OPA1679 ownership

`U32` remains one physical OPA1679 shared by sheets 03 and 07:

```text
unit 1 — channel A, Return DAC conversion — sheet 03
unit 2 — channel B, Direct/Wet final half-sum — sheet 07
unit 3 — channel C, output-level buffer — sheet 07
unit 4 — channel D, post-mute output driver — sheet 07
unit 5 — common V+/V− power unit — sheet 03
```

Official TSSOP-14 channel pins:

```text
A: pin 3 IN+, pin 2 IN−, pin 1 OUT
B: pin 5 IN+, pin 6 IN−, pin 7 OUT
C: pin 10 IN+, pin 9 IN−, pin 8 OUT
D: pin 12 IN+, pin 13 IN−, pin 14 OUT
power: pin 4 V+, pin 11 V−
```

The validator requires exactly five `U32 / OPA1679` unit instances across sheets 03 and 07, units exactly `1..5`, no duplicate U32 package and no accepted footprint. The complete Prototype A allocation remains seven physical OPA1679 packages.

## Final output path

```text
DIRECT_PRESENT ─40.2 kΩ─┐
                         ├─ U32B equal inverting half-sum
WET_MIX       ─40.2 kΩ─┘        │
                                ├─ 20.0 kΩ feedback
                                ↓
                         passive 10 kΩ output level
                                ↓
                         U32C unity buffer
                                ↓
                         10 kΩ mute isolation
                                ↓
                         J113-class shunt mute
                                ↓
                         U32D post-mute driver
                                ↓
                         10 µF bipolar AC coupling
                                ↓
                         1 kΩ output protection
                                ↓
                         rail clamps + RF/reference network
                                ↓
                         logical WQP518MA output jack
```

## Output gain and headroom

```text
R_DIRECT = 40.2 kΩ
R_WET    = 40.2 kΩ
R_FB     = 20.0 kΩ

per-branch magnitude = 20.0 / 40.2 ≈ 0.4975
6 Vpp Direct + 6 Vpp Wet calculated maximum ≈ 5.97 Vpp
```

The output-level control is passive and can only attenuate. The calculated normal output therefore remains below the locked `10 Vpp` ceiling before bench tolerances and clipping tests.

## Fail-muted control

A low or undefined `HARDWARE_FAULT_N` lights the isolated fault optocoupler and clamps the JFET mute gate toward `0 V`, turning the shunt mute on. A healthy high fault line switches the inverter on, extinguishes the optocoupler and allows the gate to move toward the negative rail through the controlled release network.

First-pass calculated values:

```text
negative pull = 100 kΩ to −12 V
power-off pull = 1 MΩ to GND
mute capacitor = 1 µF
healthy steady gate ≈ −10.91 V
healthy release time constant ≈ 90.9 ms

+12 V fault pull-up = 2.2 kΩ
opto LED resistor = 3.3 kΩ
estimated LED current ≈ 1.96 mA
assumed 50% CTR first-pass fault clamp ≈ 12.7 ms
```

These calculations are schematic constraints, not acceptance of exact optocoupler, JFET, NPN or capacitor parts. Fault response, release timing, pop suppression and mute depth remain later measured gates.

## Provisional symbols

The logical NPN fault inverter and output-level potentiometer use project-local application symbols with explicit logical pins and blank footprints:

```text
Q71: BASE / COLLECTOR / EMITTER
RV700: LOW / WIPER / HIGH
```

The optocoupler and output jack also use project-local logical symbols. Exact devices, package pin maps, footprints, panel mechanics and jack alignment are not accepted by this capture gate.

## Generator-boundary repairs

The pinned schematic API mirrors Y coordinates for the project-local multi-unit U32 symbol after component positions are snapped to the native KiCad grid. The repair reads each serialized U32 unit position and moves only its named labels to the corresponding official physical pin coordinates. The repair fails closed if the expected unit or label is missing or duplicated.

## Verification evidence

The dedicated sheet-07 workflow passed:

- native regeneration of sheet 03 with U32 units 1/5;
- native generation of sheet 07 with U32 units 2/3/4;
- official OPA1679 pin-map validation;
- one-device, five-unit U32 ownership validation;
- seven-package OPA1679 allocation validation;
- Direct/Wet gain and calculated headroom validation;
- fail-muted control and first-pass timing validation;
- provisional control-symbol and blank-footprint validation;
- logical output-jack and no-export boundary validation;
- KiCad CLI `10.0.4` hierarchical ERC;
- strict captured-sheet warning policy.

ERC report:

```text
0 errors
0 warnings
```

The first passing artifact was promoted in commit `265f4ad`.

## Committed-file rerun

The follow-up workflow detected `07_OUTPUT_MUTE_PROTECTION_CAPTURED` and skipped:

```text
sheet-03 regeneration
sheet-07 generation
U32 coordinate repair
promotion
```

It then passed both sheet-07 validators, KiCad 10 hierarchical ERC and the strict captured-sheet warning policy directly against committed files.

`07_OUTPUT_MUTE_PROTECTION` is closed at schematic-capture level. Exact components, packages, footprints, PCB placement, output-jack mechanics, measured output level, load drive, mute depth, fault timing, pop behaviour, protection current and endurance remain later independent gates.
