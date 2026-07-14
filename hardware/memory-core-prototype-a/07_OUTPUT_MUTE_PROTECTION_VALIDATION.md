# 07_OUTPUT_MUTE_PROTECTION — Validation Record

## Current status

```text
SCHEMATIC-CAPTURE CONTRACT: PASS
EXACT Q70 / Q71 / U70 PIN-MAP CONTRACT: PASS
HEALTHY-RELEASE FAIL-MUTE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
U70 ACTUAL-BIAS SATURATION PROOF: PASS
Q70 25 C DATASHEET-BOUND ATTENUATION: 61.50 dB
DIMENSIONAL FOOTPRINT AUDIT: PENDING CURRENT PR RERUN
KICAD 10 HIERARCHICAL ERC: PENDING CURRENT PR RERUN
MEASURED MUTE / POP / RAIL SEQUENCING: NOT ACCEPTED
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
```

## Exact parts

| Ref | Exact part | Physical pins | Assigned footprint |
|---|---|---|---|
| Q70 | onsemi MMBFJ113 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia PMV20XNE | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay VO617A-3X007T | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

## U70 actual-bias saturation proof

The release path is evaluated from the guaranteed saturated operating point, not from the non-saturated CTR figure.

Vishay guarantees:

```text
IF = 5 mA
IC = 1.0 mA
VCE(sat) <= 0.4 V
```

The realised LED path, using `RAIL_P12 = -5%`, both LED resistors at `+1%`, and `VF = 1.65 V`, gives:

```text
minimum estimated IF = 5.304 mA
```

At the most demanding release load used by the validator:

```text
RAIL_N12 magnitude = +5%
R715 and R716 = -1%
VCE = 0.4 V
required collector current = 0.112 mA maximum
guaranteed saturated test current = 1.000 mA
current margin = 8.93:1
```

The previous `5.304 mA collector capability` and `1.055 mA initial load` statements are withdrawn. The corrected proof follows the actual resistor load line.

## Q70 mute-depth qualification

```text
R703 minimum at -1% = 118.8 kOhm
MMBFJ113 rDS(on) maximum at TJ = 25 C = 100 ohm
25 C datasheet-bound attenuation = 61.50 dB
```

This is not a full-temperature or production guarantee. Gate C must demonstrate at least `60 dB` measured attenuation across the declared operating temperature, device spread, signal conditions and assembled circuit.

## Dimensional footprint audit

`OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json` records manufacturer package dimensions and pin orientation.

The dedicated validator extracts the actual footprint files from the pinned KiCad `10.0.4` image and checks:

- SOT-23 pad centres, pad sizes, two-lead-side orientation and courtyard envelope;
- option-7 SMD-4 row spacing, pin pitch, pad sizes, pin-1 orientation and courtyard envelope;
- compatibility with the manufacturer package maxima;
- the continued prohibition on PCB placement and assembly acceptance.

This is stronger than checking the footprint library names alone.

## Fault timing and driver gate

```text
healthy MUTE_GATE estimate = -10.545 V
worst J113 cutoff boundary = -3.0 V
R716 x C710 nominal time constant = 10 ms
calculated crossing time = 12.57 ms
schematic target = less than 20 ms

PMV20XNE conservative gate estimate = 2.604 V
PMV20XNE guaranteed RDS(on) test point = 2.5 V
```

## Unchanged boundaries

- sheet 07 exports no hierarchy net;
- `U32` remains one physical OPA1679 split across sheets 03 and 07;
- the output jack remains a separate exact-part and mechanical gate;
- measured mute depth, pop energy, rail sequencing, load drive and endurance remain Gate C;
- PCB placement, routing, fabrication and purchasing remain blocked.

## Required closure evidence

The current committed PR head must pass:

1. the corrected actual-bias validator;
2. the dimensional footprint validator against the pinned KiCad files;
3. exact pin and instance validation;
4. shared-U32 and hierarchy validation;
5. KiCad 10 hierarchical ERC with zero errors and zero warnings;
6. a committed-file rerun with no promotion diff.

The Gate-B decision remains subject to a new PR review after those checks pass.
