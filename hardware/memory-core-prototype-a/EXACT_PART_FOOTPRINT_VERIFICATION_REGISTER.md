# Exact-Part and Footprint Verification Register

## Authority

```text
Gate A — schematic acceptance       PASS / MERGED
Gate B — exact parts / footprints   ACTIVE
Gate C — bench acceptance           NOT STARTED
Gate D — PCB / production           BLOCKED
```

Gate B may correct schematic assumptions and accept individually reviewed package mappings. It does not authorise PCB placement, routing, fabrication, purchasing or production claims.

## Verification rule

An active device or connector is accepted only when all of these are traceable:

1. exact manufacturer and orderable part number;
2. manufacturer datasheet;
3. package designation and dimensional envelope;
4. physical pin numbering and symbol mapping;
5. electrical limits at the actual circuit bias and fault states;
6. actual KiCad footprint geometry from the pinned toolchain;
7. dimensional comparison of pads, pitch, orientation and courtyard;
8. explicit transfer of remaining physical and measured gates.

A generic class name, typical graph, assumed CTR or footprint-name match is not acceptance evidence.

## Lane 01 — output mute and fault-control path

Detailed records:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`
- `07_OUTPUT_MUTE_PROTECTION_VALIDATION.md`
- `OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json`

Current result:

```text
Q70 MMBFJ113 physical part and pin map          RETAIN
Q71 PMV20XNE physical part and pin map           RETAIN
U70 VO617A-3X007T physical part and pin map       RETAIN
POWERED HEALTHY-RELEASE TOPOLOGY                 RETAIN
U70 ACTUAL-BIAS SATURATION PROOF                  PASS
Q70 25 C DATASHEET-BOUND ATTENUATION              61.50 dB
DIMENSIONAL FOOTPRINT AUDIT                       PENDING CURRENT PR RERUN
MEASURED MUTE / POP / RAIL SEQUENCING             GATE C
PCB / ROUTING / FABRICATION / PURCHASING          BLOCKED
```

### Candidate register

| Ref | Exact part | Manufacturer package | Physical pins | KiCad footprint |
|---|---|---|---|---|
| Q70 | onsemi `MMBFJ113` | SOT-23 / TO-236, case 318-08 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia `PMV20XNE` | TO-236AB / SOT23 | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay `VO617A-3X007T` | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

### Corrected electrical evidence

```text
minimum estimated VO617A LED current = 5.304 mA
guaranteed saturated condition = IF 5 mA, IC 1 mA, VCE(sat) <= 0.4 V
actual worst load at VCE = 0.4 V = 0.112 mA
saturation-current margin = 8.93:1

Q70 25 C datasheet-bound attenuation = 61.50 dB
full-temperature and measured >=60 dB acceptance = Gate C

healthy MUTE_GATE estimate = -10.545 V
fault / +12 V loss crossing of -3 V = 12.57 ms
```

### Dimensional evidence

The validator uses the actual footprints copied from the pinned KiCad image rather than trusting the library identifiers:

```text
Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod
Package_DIP.pretty/SMDIP-4_W7.62mm.kicad_mod
```

It checks pad centres, pad dimensions, package pitch, pin orientation and courtyard coverage against `OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json`.

Lane 01 is not approved until the current committed head passes those checks and PR #46 receives a new review.

## Remaining Gate-B lanes

Proceed only after Lane 01 is deliberately merged:

1. input and output jacks;
2. SSI2164 package and control-law assumptions;
3. OPA1679 package and decoupling requirements;
4. Return limiter and clamp diodes;
5. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.
