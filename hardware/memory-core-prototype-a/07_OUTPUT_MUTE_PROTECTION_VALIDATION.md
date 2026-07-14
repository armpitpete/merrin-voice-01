# 07_OUTPUT_MUTE_PROTECTION — Validation Record

## Current status

```text
SCHEMATIC-CAPTURE CONTRACT: PASS
EXACT Q70 / Q71 / U70 PIN-MAP CONTRACT: PASS
HEALTHY-RELEASE FAIL-MUTE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
U70 ACTUAL-BIAS SATURATION PROOF: PASS — 8.93:1 MARGIN
Q70 25 C DATASHEET-BOUND ATTENUATION: PASS — 61.50 dB
HASH-LOCKED DIMENSIONAL FOOTPRINT AUDIT: PASS
KICAD 10 HIERARCHICAL ERC: PASS — 0 ERRORS / 0 WARNINGS
COMMITTED-FILE BYTE-IDEMPOTENT RERUN: PASS
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

The realised LED path gives at least `5.304 mA`. At the most demanding calculated release load:

```text
RAIL_N12 magnitude = 12.6 V
R715 + R716 = 108.9 kOhm
VCE = 0.4 V
required collector current = 0.112 mA
guaranteed saturated test current = 1.000 mA
current margin = 8.93:1
```

The previous non-saturated CTR capability argument is withdrawn.

## Q70 mute-depth qualification

```text
R703 minimum at -1% = 118.8 kOhm
MMBFJ113 rDS(on) maximum at TJ = 25 C = 100 ohm
25 C datasheet-bound attenuation = 61.50 dB
```

This is not a full-temperature or production guarantee. Gate C must demonstrate at least `60 dB` measured attenuation across the declared operating temperature, device spread, signal conditions and assembled circuit.

## Dimensional footprint audit

The validator parses committed snapshots from KiCad's official footprint library and verifies their SHA-256 values before reading geometry.

```text
SOT-23.kicad_mod
sha256 f8fd6dd6411c47f6547df13b1efe33867682117b7fb6f2ea829d1d726d565887

SMDIP-4_W7.62mm.kicad_mod
sha256 5d9faa2287c41ae0b7930be347813bde5098acb8688513fff275fde904b532a0
```

Verified geometry:

```text
SOT-23 pad centres: (-0.9375,-0.95), (-0.9375,0.95), (0.9375,0)
SOT-23 pad size:    1.475 x 0.600 mm
SOT-23 courtyard:   3.860 x 3.400 mm

SMDIP-4 row spacing: 7.620 mm
SMDIP-4 pin pitch:   2.540 mm
SMDIP-4 pad size:    2.000 x 1.780 mm
SMDIP-4 courtyard:   10.140 x 5.580 mm
```

The audit covers pad numbering, pad centres, pad dimensions, pitch, pin-one orientation and courtyard coverage. PCB placement, neighbour clearances, creepage strategy and assembly process remain blocked.

## Fault timing and driver gate

```text
healthy MUTE_GATE estimate = -10.545 V
worst J113 cutoff boundary = -3.0 V
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

## Validation evidence

The promoted committed head `59b96b78891bc95c6c025fad70b9137c6c4241f4` passed dedicated workflow run `29339271573`:

```text
first-generation sheet capture             SKIPPED
committed exact-part amendment              CURRENT
25 C evidence annotation                    CURRENT
actual-bias saturation validator            PASS
exact symbol / physical-pin validator       PASS
hash-locked dimensional footprint validator PASS
shared U32 / hierarchy validator            PASS
KiCad 10 hierarchical ERC                   PASS
ERC policy                                  0 errors / 0 warnings
promotion                                   NO COMMITTED-FILE DIFF
```

## Gate decision

```text
Gate A — schematic architecture               REMAINS ACCEPTED
Gate B — Q70/Q71/U70 exact parts/footprints   PASS, SUBJECT TO NEW PR REVIEW
Gate C — measured mute/fault behaviour        NOT STARTED
Gate D — PCB / production                     BLOCKED
```

PR #46 remains unmerged and must return to draft for deliberate approval or rejection.
