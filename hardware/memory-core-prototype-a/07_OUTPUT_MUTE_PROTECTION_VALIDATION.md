# 07_OUTPUT_MUTE_PROTECTION — Validation Record

## Current status

```text
SCHEMATIC-CAPTURE CONTRACT: PASS
EXACT Q70 / Q71 / U70 PIN-MAP CONTRACT: PASS
HEALTHY-RELEASE FAIL-MUTE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
Q70 CASE 318-08 INDEPENDENT DIMENSIONAL AUDIT: PASS
Q71 TO-236AB INDEPENDENT DIMENSIONAL AUDIT: PASS
U70 OPTION-7 SMD-4 DIMENSIONAL AUDIT: PASS
U70 25 C DATASHEET-BOUND SATURATION PROOF: PASS — 8.93:1
Q70 25 C DATASHEET-BOUND ATTENUATION: PASS — 61.50 dB
IMMUTABLE KICAD FOOTPRINT PROVENANCE: PASS
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

## U70 25 C datasheet-bound saturation proof

The load line is evaluated from Vishay's saturated electrical-characteristics condition, not from the non-saturated CTR figure:

```text
Tamb = 25 C unless otherwise specified
IF = 5 mA
IC = 1.0 mA
VCE(sat) <= 0.4 V
minimum estimated LED current = 5.304 mA
required release current      = 0.112 mA
saturated test current        = 1.000 mA
calculated margin             = 8.93:1
```

This is a 25 C datasheet-bound proof. **Full-temperature release behaviour remains Gate C.**

## Q70 mute-depth qualification

```text
R703 minimum at -1%                    = 118.8 kOhm
MMBFJ113 rDS(on) maximum at TJ = 25 C = 100 ohm
25 C datasheet-bound attenuation       = 61.50 dB
```

Gate C must demonstrate at least `60 dB` measured attenuation across the declared operating temperature, device spread, signal conditions and assembled circuit.

## Independent dimensional audits

### Q70 — onsemi CASE 318-08

```text
body length maximum       3.04 mm
body width maximum        1.40 mm
overall lead span maximum 2.64 mm
outer lead pitch range    1.78 to 2.04 mm
lead width maximum        0.50 mm
lead length maximum       0.69 mm
```

The validator compares Q70's own package record directly with the accepted SOT-23 pad geometry. Q70 no longer inherits Q71's package result.

### Q71 — Nexperia TO-236AB

Q71 is independently checked against its own TO-236AB body, lead and pitch limits.

### U70 — Vishay option-7 SMD-4

U70 is independently checked for row spacing, lead pitch, pad dimensions, pin-one orientation and courtyard coverage.

## Immutable footprint provenance

The project-local footprints are byte-for-byte copies from the official `KiCad/kicad-footprints` repository at immutable commit:

```text
7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
```

```text
SOT-23.kicad_mod
Git blob 50a8c41bf25dc5843c0ceb95820dc83b930321f9
SHA-256 db5b998f0d36708205a4b8edc0db1501deb0246a81b52e9cb036cfd58b7570d3

SMDIP-4_W7.62mm.kicad_mod
Git blob f45a9a53110c40e6dfdcdae40d07a29856841be2
SHA-256 23f55da451d042a66c22a94cf3e622a242f6e5c4c7ed22909a564699350bf30d
```

The project-local committed files are the Gate-B footprint authority. Moving upstream branches and ambient workstation libraries are not accepted evidence.

## Fault timing and driver gate

```text
healthy MUTE_GATE estimate          = -10.545 V
worst J113 cutoff boundary          = -3.0 V
calculated crossing time            = 12.57 ms
schematic target                    = less than 20 ms
PMV20XNE conservative gate estimate = 2.604 V
guaranteed RDS(on) test point       = 2.5 V
```

## Validation evidence

Committed head `8d0187bf2ed4bc3caceb9cc4844b2d50bef65b6a` passed dedicated workflow run `29347852152`:

```text
Q70 CASE 318-08 independent validator      PASS
Q71 TO-236AB independent validator         PASS
U70 option-7 SMD-4 validator               PASS
immutable source revision and hashes       PASS
U70 25 C authority validator               PASS
exact symbol / physical-pin validator      PASS
shared U32 / hierarchy validator           PASS
KiCad 10 hierarchical ERC                  PASS — 0 errors / 0 warnings
promotion                                  NO COMMITTED-FILE DIFF
```

The complete schematic workflow chain passed on the same head.

## Unchanged boundaries

- sheet 07 exports no hierarchy net;
- `U32` remains one physical OPA1679 split across sheets 03 and 07;
- the output jack remains a separate exact-part and mechanical gate;
- full-temperature U70 release behaviour remains Gate C;
- measured mute depth, pop energy, rail sequencing, load drive and endurance remain Gate C;
- PCB placement, routing, fabrication and purchasing remain blocked.

## Gate decision

```text
Gate A — schematic architecture               REMAINS ACCEPTED
Gate B — Q70/Q71/U70 exact parts/footprints   PASS, SUBJECT TO NEW PR REVIEW
Gate C — measured mute/fault behaviour        NOT STARTED
Gate D — PCB / production                     BLOCKED
```

PR #46 remains unmerged and must return to draft for deliberate approval or rejection.
