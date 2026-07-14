# Exact-Part and Footprint Verification Register

## Authority

```text
Gate A — schematic acceptance       PASS / MERGED
Gate B — exact parts / footprints   ACTIVE
Gate C — bench acceptance           NOT STARTED
Gate D — PCB / production           BLOCKED
```

Gate B may correct schematic assumptions and assign individually reviewed package footprints. It does not authorise PCB placement, routing, fabrication, purchasing or production claims.

## Verification rule

An active device or connector is accepted only when all of the following are fixed and independently checked:

1. exact manufacturer and orderable part number;
2. manufacturer datasheet;
3. package designation and dimensions;
4. physical pin numbering and symbol mapping;
5. electrical limits at the actual circuit bias and fault states;
6. one reviewed KiCad footprint mapped to that package;
7. package-specific constraints transferred to later physical review;
8. explicit `ACCEPTED`, `BLOCKED` or `RETURN TO SCHEMATIC` status.

A generic class name, typical graph, assumed CTR or visually similar footprint is not acceptance evidence.

## Lane 01 — output mute and fault-control path

Detailed review:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`

Current result:

```text
Q70 MMBFJ113 output-mute JFET             ACCEPTED
Q71 PMV20XNE healthy-release MOSFET        ACCEPTED
U70 VO617A-3X007T optocoupler              ACCEPTED
POSITIVE-RAIL-LOSS FAIL-MUTE TOPOLOGY      ACCEPTED AT CALCULATED LEVEL
CALCULATED STATIC MUTE ATTENUATION         61.50 dB
FOOTPRINTS ASSIGNED                        3
MEASURED MUTE / POP / RAIL SEQUENCING      GATE C
```

### Accepted register

| Ref | Exact part | Package | Physical pins | KiCad footprint | Decision |
|---|---|---|---|---|---|
| Q70 | onsemi `MMBFJ113` | SOT-23 / TO-236 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` | ACCEPTED |
| Q71 | Nexperia `PMV20XNE` | SOT-23 / TO-236AB | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` | ACCEPTED |
| U70 | Vishay `VO617A-3X007T` | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` | ACCEPTED |

### Locked schematic results

```text
R703 = 120 kOhm 1%
MMBFJ113 rDS(on) maximum = 100 ohm
calculated worst static attenuation = 61.50 dB

PMV20XNE conservative gate estimate = 2.604 V
manufacturer RDS(on) guarantee point = 2.5 V

VO617A-3X007T minimum LED current estimate = 5.304 mA
selected CTR class minimum = 100% at 5 mA
calculated release-current requirement = 1.055 mA maximum initial

healthy MUTE_GATE estimate = -10.545 V
fault / +12 V loss crossing of -3 V = 12.57 ms
```

Measured mute depth, audible pop, exact rail ramps, load behaviour and endurance remain Gate C.

## Remaining Gate-B lanes

Proceed only after Lane 01 PR review:

1. input and output jacks;
2. SSI2164 package and control-law assumptions;
3. OPA1679 package and decoupling requirements;
4. Return limiter and clamp diodes;
5. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.
