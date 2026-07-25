# 05_MEMORY_GHOST_WET — Validation Record

## Status

```text
GENERATED ARTIFACT: PASS
HIERARCHY / EXPORT CONTRACT: PASS
SSI2164 SYMBOL / PHYSICAL-PIN CONTRACT: PASS
SHARED MULTI-UNIT DEVICE CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PASS — 0 ERRORS / 0 WARNINGS
COMMITTED-FILE RERUN: PASS — GENERATION SKIPPED
PCB / FOOTPRINT / MECHANICAL AUTHORITY: NOT GRANTED
```

## Locked sheet boundary

Inputs:

```text
RAIL_P12
RAIL_N12
MEMORY_DAC
GHOST_DAC
VCA_MEMORY_CTRL
VCA_GHOST_CTRL
VCA_WET_CTRL
```

Only this signal may leave sheet 05:

```text
WET_MIX
```

Memory, Ghost, wet-sum, SSI2164 current and control-filter nodes remain local.

## Shared SSI2164 ownership

`U60` is one physical five-unit device shared by sheets 05 and 06:

```text
unit 1 — Memory channel 1:    pin 2 IIN1, pin 3 VC1, pin 4 IOUT1
unit 2 — Ghost channel 2:     pin 7 IIN2, pin 6 VC2, pin 5 IOUT2
unit 3 — Return channel 3:    pin 15 IIN3, pin 14 VC3, pin 13 IOUT3 — sheet 06
unit 4 — wet-master channel:  pin 10 IIN4, pin 11 VC4, pin 12 IOUT4
unit 5 — common power:         MODE/GND/V−/V+ — sheet 06
```

The native validator requires exactly five SSI2164 unit instances across all sheets, references all equal to `U60`, values all equal to `SSI2164`, units exactly `1..5`, and no accepted footprint.

## Captured analogue path

Memory and Ghost each use:

```text
10 µF AC coupling
20 kΩ SSI2164 input resistor
220 Ω / 1.2 nF stability network
1 kΩ / 100 nF control isolation and filtering
20 kΩ / 100 pF OPA1679 current-to-voltage stage
```

Their outputs enter an equal inverting sum:

```text
R_MEMORY = 40.2 kΩ
R_GHOST  = 40.2 kΩ
R_FB     = 20.0 kΩ

per-branch magnitude = 20.0 / 40.2 ≈ 0.4975
combined equal full-scale magnitude ≈ 0.995
```

The sum is AC-coupled through SSI2164 channel 4, converted by the final OPA1679 stage, isolated by `47 Ω`, and exported as `WET_MIX`.

## Generator-boundary repairs

The pinned schematic API mirrors Y coordinates returned for pins in the project-local multi-unit SSI2164 symbol. Exact post-generation repairs move only the nine sheet-05 and six sheet-06 SSI2164 attachments to their actual native KiCad pin coordinates.

The same API accepts but does not serialise the hierarchical-label shape argument. Exact named post-generation repairs set only:

```text
WET_MIX = output
RETURN_LIMITED = output
RETURN_FEED = output
ABSENCE_INFLUENCE = output
```

Both repairs fail closed if an expected named label or coordinate is missing or duplicated.

## First passing artifact

The dedicated sheet-05 workflow passed:

- native sheet-05 and integrated sheet-06 generation;
- exact hierarchy-direction checks;
- official SSI2164 symbol and physical-pin mapping;
- units `1/2/4` on sheet 05 and units `3/5` on sheet 06;
- one-reference, one-value, no-duplicate-device enforcement;
- equal half-sum resistor and gain contract;
- KiCad CLI `10.0.4` hierarchical ERC;
- strict captured-sheet warning policy.

ERC result:

```text
0 errors
0 warnings
```

Only that passing native artifact was promoted in commit `917b98a`.

## Committed-file rerun

The follow-up workflow detected `05_MEMORY_GHOST_WET_CAPTURED` and skipped:

```text
generation
physical-coordinate repair
output-direction repair
promotion
```

It then passed the same native contract validator, KiCad 10 hierarchical ERC, and strict warning policy directly against committed files. The integrated Return workflow independently skipped Return generation and passed its shared-U60 ownership and ERC gates.

`05_MEMORY_GHOST_WET` is closed at schematic-capture level. Exact packages, footprints, physical placement, measured gain/control law, noise, distortion, loop safety and endurance remain later independent gates.


## SSI2164 buffered-control amendment

The accepted sheet now includes the relevant units of shared `U63 / OPA4196 CONTROL BUFFER`. The OPA4196 presents a high-impedance load to the existing control filter and drives the SSI2164 VC pin through 20 Ω with post-buffer 0 V / +3.3 V clamps. The OPA4196 and SSI2164 footprints remain blank; PCB and mechanical authority are not granted.
