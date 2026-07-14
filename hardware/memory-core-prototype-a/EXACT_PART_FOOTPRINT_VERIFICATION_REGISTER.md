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
6. SHA-256-locked KiCad footprint geometry from an authoritative source;
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
Q70 MMBFJ113 exact part / pin map / package      PASS, SUBJECT TO PR REVIEW
Q71 PMV20XNE exact part / pin map / package       PASS, SUBJECT TO PR REVIEW
U70 VO617A-3X007T exact part / pin map / package  PASS, SUBJECT TO PR REVIEW
POWERED HEALTHY-RELEASE TOPOLOGY                  PASS AT CALCULATED LEVEL
U70 ACTUAL-BIAS SATURATION PROOF                   PASS — 8.93:1 MARGIN
Q70 25 C DATASHEET-BOUND ATTENUATION               PASS — 61.50 dB
HASH-LOCKED DIMENSIONAL FOOTPRINT AUDIT             PASS
KICAD 10 HIERARCHICAL ERC                           PASS — 0 / 0
COMMITTED-FILE NO-DIFF RERUN                        PASS
MEASURED MUTE / POP / RAIL SEQUENCING               GATE C
PCB / ROUTING / FABRICATION / PURCHASING            BLOCKED
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

The validator parses committed, SHA-256-locked snapshots from KiCad's official footprint library:

```text
SOT-23 snapshot hash:
f8fd6dd6411c47f6547df13b1efe33867682117b7fb6f2ea829d1d726d565887

SMDIP-4_W7.62mm snapshot hash:
5d9faa2287c41ae0b7930be347813bde5098acb8688513fff275fde904b532a0
```

It verifies pad centres, pad dimensions, package pitch, pin orientation and courtyard coverage. Placement, neighbour interaction and assembly acceptance remain blocked.

### Closure evidence

Committed head `59b96b78891bc95c6c025fad70b9137c6c4241f4` passed dedicated run `29339271573`, including exact electrical validation, snapshot hashes, dimensional footprint validation, KiCad ERC and a no-diff promotion step.

Lane 01 remains subject to a new PR #46 approval review. It is not merged.

## Remaining Gate-B lanes

Proceed only after Lane 01 is deliberately merged:

1. input and output jacks;
2. SSI2164 package and control-law assumptions;
3. OPA1679 package and decoupling requirements;
4. Return limiter and clamp diodes;
5. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.
