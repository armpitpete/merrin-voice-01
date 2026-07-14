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
6. immutable upstream revision and SHA-256-locked project-local footprint bytes;
7. independent dimensional comparison for every exact package;
8. explicit temperature scope for datasheet-bound electrical claims;
9. transfer of remaining physical and measured gates.

A generic class name, typical graph, assumed CTR, moving library branch or footprint-name match is not acceptance evidence.

## Lane 01 — output mute and fault-control path

Detailed records:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`
- `07_OUTPUT_MUTE_PROTECTION_VALIDATION.md`
- `OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json`

Current result:

```text
Q70 MMBFJ113 exact part / pin map                RETAINED
Q71 PMV20XNE exact part / pin map                 RETAINED
U70 VO617A-3X007T exact part / pin map            RETAINED
POWERED HEALTHY-RELEASE TOPOLOGY                  PASS AT CALCULATED LEVEL
Q70 CASE 318-08 INDEPENDENT DIMENSIONAL AUDIT     PASS, PENDING CURRENT-HEAD CI
Q71 TO-236AB INDEPENDENT DIMENSIONAL AUDIT        PASS, PENDING CURRENT-HEAD CI
U70 OPTION-7 SMD-4 DIMENSIONAL AUDIT              PASS, PENDING CURRENT-HEAD CI
U70 25 C DATASHEET-BOUND SATURATION PROOF         PASS — 8.93:1
Q70 25 C DATASHEET-BOUND ATTENUATION              PASS — 61.50 dB
IMMUTABLE KICAD FOOTPRINT PROVENANCE              PASS, PENDING CURRENT-HEAD CI
MEASURED MUTE / POP / RAIL SEQUENCING             GATE C
PCB / ROUTING / FABRICATION / PURCHASING          BLOCKED
```

### Candidate register

| Ref | Exact part | Manufacturer package | Physical pins | Assigned KiCad footprint |
|---|---|---|---|---|
| Q70 | onsemi `MMBFJ113` | SOT-23 / TO-236, CASE 318-08 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia `PMV20XNE` | TO-236AB / SOT23 | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay `VO617A-3X007T` | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

### Electrical evidence

```text
minimum estimated VO617A LED current = 5.304 mA
25 C saturated condition = IF 5 mA, IC 1 mA, VCE(sat) <= 0.4 V
actual worst load at VCE = 0.4 V = 0.112 mA
25 C saturation-current margin = 8.93:1
full-temperature release behaviour = Gate C

Q70 25 C datasheet-bound attenuation = 61.50 dB
full-temperature and measured >=60 dB acceptance = Gate C

healthy MUTE_GATE estimate = -10.545 V
fault / +12 V loss crossing of -3 V = 12.57 ms
```

### Q70 independent dimensional evidence

Q70's CASE 318-08 package is independently recorded and checked:

```text
body length maximum       3.04 mm
body width maximum        1.40 mm
overall lead span maximum 2.64 mm
outer lead pitch range    1.78 to 2.04 mm
lead width maximum        0.50 mm
lead length maximum       0.69 mm
```

It no longer inherits the Q71 package decision.

### Immutable footprint authority

The accepted project-local footprint bytes originate from the official `KiCad/kicad-footprints` repository at:

```text
commit 7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
```

```text
SOT-23
Git blob 50a8c41bf25dc5843c0ceb95820dc83b930321f9
SHA-256 db5b998f0d36708205a4b8edc0db1501deb0246a81b52e9cb036cfd58b7570d3

SMDIP-4_W7.62mm
Git blob f45a9a53110c40e6dfdcdae40d07a29856841be2
SHA-256 23f55da451d042a66c22a94cf3e622a242f6e5c4c7ed22909a564699350bf30d
```

The validator checks each package independently against these immutable files. Placement, neighbouring clearances, creepage strategy and assembly acceptance remain blocked.

### Required closure

The current PR head must pass the independent package validators, immutable provenance checks, temperature-scope checks, exact electrical validators, KiCad ERC and a committed-file no-diff rerun.

Lane 01 remains subject to another PR #46 approval review. It is not merged.

## Remaining Gate-B lanes

Proceed only after Lane 01 is deliberately merged:

1. input and output jacks;
2. SSI2164 package and control-law assumptions;
3. OPA1679 package and decoupling requirements;
4. Return limiter and clamp diodes;
5. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.
