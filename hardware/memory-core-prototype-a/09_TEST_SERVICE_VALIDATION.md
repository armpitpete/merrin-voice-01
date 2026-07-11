# 09_TEST_SERVICE — Validation Record

## Status

```text
GENERATED ARTIFACT: PASS
HIERARCHY / READ-ONLY CONTRACT: PASS
PROBE-ISOLATION CONTRACT: PASS
SERVICE HEADER LOGICAL-PIN CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PASS — 0 ERRORS / 0 WARNINGS
PASSING ARTIFACT PROMOTION: PASS
COMMITTED-FILE RERUN: PENDING
PCB / FOOTPRINT / FIXTURE / MECHANICAL AUTHORITY: NOT GRANTED
```

## Locked sheet boundary

Sheet 09 consumes exactly these read-only hierarchy inputs:

```text
RAIL_3V3
HARDWARE_FAULT_N
SHAPED_PRESENT
ADC_ANALOG_IN
RETURN_LIMITED
RETURN_FEED
ABSENCE_INFLUENCE
WET_MIX
```

Sheet 09 exports no hierarchy signal.

`SERVICE_TEST`, `RESET_CLEAR`, and `SAFE_MUTE` remain operating inputs between sheets 08 and 02. SWD remains on sheet 02. Power-branch current-measurement links remain a later physical implementation gate associated with sheet 01.

## Probe branches

Each accepted signal receives a separate local probe branch:

```text
RAIL_3V3           → 1 kΩ  → RAIL_3V3_PROBE
HARDWARE_FAULT_N   → 47 kΩ → HARDWARE_FAULT_N_PROBE
SHAPED_PRESENT     → 22 kΩ → SHAPED_PRESENT_PROBE
ADC_ANALOG_IN      → 22 kΩ → ADC_ANALOG_IN_PROBE
RETURN_LIMITED     → 22 kΩ → RETURN_LIMITED_PROBE
RETURN_FEED        → 22 kΩ → RETURN_FEED_PROBE
ABSENCE_INFLUENCE  → 22 kΩ → ABSENCE_INFLUENCE_PROBE
WET_MIX            → 22 kΩ → WET_MIX_PROBE
```

The sheet contains individual test points `TP900` through `TP907` for those probe nodes and `TP908` for service ground.

## First-pass loading constraints

```text
3.3 V through 1 kΩ to an accidental ground short ≈ 3.3 mA
3.3 V through 47 kΩ ≈ 70.2 µA maximum static service-drive current
22 kΩ into a 10 MΩ instrument adds approximately 0.22% loading
```

These values protect the source nets from direct connector shorts or low-impedance probing while remaining suitable for high-impedance bring-up measurement. They do not authorise a production fixture or measurement procedure.

## Logical service header

`J90` is a logical ten-position service header or pad grouping with no accepted footprint:

```text
1  GND
2  RAIL_3V3_PROBE
3  HARDWARE_FAULT_N_PROBE
4  SHAPED_PRESENT_PROBE
5  ADC_ANALOG_IN_PROBE
6  RETURN_LIMITED_PROBE
7  RETURN_FEED_PROBE
8  ABSENCE_INFLUENCE_PROBE
9  WET_MIX_PROBE
10 GND
```

The connector family, pitch, keying, fixture, pad geometry, footprint and physical location remain blocked.

## Verification evidence

The dedicated sheet-09 workflow passed:

- native generation of the read-only service sheet;
- exact eight-input hierarchy contract;
- no hierarchy outputs;
- eight probe-branch value and net contracts;
- nine test-point references;
- ten-position logical header pin allocation;
- blank service-header footprint;
- absence of the former temporary interface harness;
- rail-short, safety-net and high-impedance loading calculations;
- KiCad CLI `10.0.4` hierarchical ERC across all nine sheets;
- zero-error and zero-warning all-sheet policy.

ERC result:

```text
0 errors
0 warnings
```

The passing artifact was promoted in commit `e9daca2`.

## Remaining independent gates

- exact service connector or pad format;
- production fixture architecture;
- test-point footprints and access clearances;
- current-measurement links or zero-ohm options for major power branches;
- measured probe loading and fault injection limits;
- PCB placement and routing;
- all mechanical and panel decisions.

`09_TEST_SERVICE` is accepted at first-pass schematic-capture level. The committed-file rerun remains the final closure condition for this sheet.
