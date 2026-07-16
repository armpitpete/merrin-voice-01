# Exact-Part and Footprint Verification Register

## Authority

```text
Gate A — schematic acceptance       PASS / MERGED
Gate B — exact parts / footprints   ACTIVE
Gate C — bench acceptance           NOT STARTED
Gate D — PCB / production           BLOCKED
```

Gate B may verify parts and assign reviewed schematic footprints. It does not authorise PCB creation, placement, routing, panel CAD, fabrication, purchasing or production.

## Verification rule

An active device or connector is accepted only when all of these are traceable:

1. exact orderable identity;
2. manufacturer or controlled-supplier evidence;
3. mechanical designation and envelope;
4. physical contact numbering and symbol mapping;
5. switching behaviour in the actual circuit use;
6. immutable upstream revision and SHA-256-locked project-local footprint bytes;
7. reviewed package or connector geometry;
8. panel and mounting-stack constraints where applicable;
9. explicit transfer of unresolved physical and measured gates.

A generic class name, supplier nickname, moving library branch or footprint-name match is not acceptance evidence by itself.

## Lane 01 — output mute and fault-control path

```text
STATUS                                  APPROVED AND MERGED
PR                                      #46
APPROVED HEAD                           c5b6551bbd6b577057bad571a9f051e8a39966c7
MAIN SQUASH COMMIT                      651d594e3c9993b2fdc6ca527328887458a7d849
Q70 MMBFJ113 / CASE 318-08              APPROVED
Q71 PMV20XNE / TO-236AB                 APPROVED
U70 VO617A-3X007T / OPTION-7 SMD-4      APPROVED
KICAD 10 HIERARCHICAL ERC               PASS — 0 / 0
MEASURED / FULL-TEMPERATURE BEHAVIOUR   GATE C
PCB / ROUTING / FAB / PURCHASING        BLOCKED
```

Detailed records:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`
- `07_OUTPUT_MUTE_PROTECTION_VALIDATION.md`
- `OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json`

## Lane 02 — input and output jacks

Detailed records:

- `JACK_EXACT_PART_EDIT_CONTRACT.md`
- `INPUT_OUTPUT_JACK_AUDIT.json`
- `INPUT_OUTPUT_JACK_EXACT_PART_REVIEW.md`
- `WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md`
- `WQP518MA_PANEL_STACK_INDEPENDENT_REVIEW.md`
- `jack-footprint-audits/KiCad_Official_Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod`
- `MerrinLab_PrototypeA.pretty/Jack_3.5mm_Thonkiconn_WQP518MA_Numeric.kicad_mod`

### Current authoritative state

```text
STATUS                                      APPROVED AND MERGED
PR                                          #47
REVIEWED HEAD                               ebaf7fbc50f5c07443d329519de0a38622f231b1
MAIN SQUASH COMMIT                          dd306209e9874dd6e9064c33973d99ecf9282690
J40 INPUT CONTACT CONTRACT                  PASS
J70 OUTPUT CONTACT CONTRACT                 PASS
WQP518MA ORDERABLE JACK                      PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE      PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT              PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT              PASS — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                      PASS
CORRECT 1.60 MM NUT-ONLY PHYSICAL FIT        PASS
INDEPENDENT MECHANICAL REVIEW                PASS
J40 FOOTPRINT FIELD                          ASSIGNED
J70 FOOTPRINT FIELD                          ASSIGNED
PROJECT SYMBOL DEFAULT FOOTPRINT             BLANK
CONTROLLED GENERATORS                        UPDATED
POST-ASSIGNMENT VALIDATION                   PASS
PCB / PANEL FAB / PURCHASING                 BLOCKED
```

Assigned footprint:

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
1 = TIP
2 = TIP_NORMAL
3 = SLEEVE
3.00 mm NPTH barrel relief
```

Assignment commit:

```text
f34eea95c216cd31df4d4e3f1498adc4b9014ec9
```

### Contact contracts

| Ref | Role | Contact 1 | Contact 2 | Contact 3 | Required switching behaviour |
|---|---|---|---|---|---|
| J40 | input | `TIP → INPUT_TIP` | `TIP_NORMAL → GND` | `SLEEVE → GND` | contacts 1–2 closed with no plug; open on insertion |
| J70 | output | `TIP → OUTPUT_TIP` | no-connect | `SLEEVE → GND` | normal contact deliberately unused |

### Controlled footprint authority

```text
orderable jack        Thonkiconn WQP518MA
controlled drawing    PJ398SM
accepted scope         contacts, switching and PCB terminal geometry
excluded scope         final panel construction and fabrication dimensions

source repository      KiCad/kicad-footprints
source commit          7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
source blob            6c9440c957bf566ae79058cdab7afabfb86955d8
source SHA-256          8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
numeric SHA-256         e9e095c63fa39dfd306a45755b6e8e9048e795b8592a6eeba3bf6ab734ed3685
```

### Corrected mechanical stack

```text
panel nominal thickness      1.60 mm
panel construction           provisional FR-4 PCB panel
panel supplier               not locked; JLCPCB only a possibility
nut                          selected Thonk hex nut
washer                       none
threaded bushing             4.50 mm supplier nominal
available thread             2.90 mm nominal before nut engagement
panel-to-PCB seating         8.30 mm supplier nominal; not measured
```

### Superseded history

The independent mechanical review at `2d1e58e61b1a04653b17cd666dda2160808079cf` authorised footprint assignment as a later bounded gate. At that historical review point only, J40 and J70 remained blank.

Before merge, PR #47 was reviewed at exact head `ebaf7fbc50f5c07443d329519de0a38622f231b1` while still open and unmerged. That pre-merge state was superseded by squash commit `dd306209e9874dd6e9064c33973d99ecf9282690` and is not current authority.

The earlier `2.00 mm aluminium + washer + nut` fit statement is withdrawn because it described the wrong stack.

### Deferred mechanical-release gate

Before PCB placement, standoff selection, panel CAD, fabrication or purchasing, lock or measure:

1. final panel material and supplier;
2. actual finished panel thickness or controlled supplier tolerance;
3. actual assembled PCB-to-panel seating distance;
4. finished panel-hole diameter and manufacturing tolerance;
5. any resulting axis-offset correction.

### Current stop boundary

```text
Lane 02 exact-part authority            APPROVED AND MERGED
J40 / J70 footprint assignment          COMPLETE
project symbol default                  BLANK
PCB creation / placement / routing      BLOCKED
panel CAD / fabrication                 BLOCKED
purchasing / production                 BLOCKED
SSI2164 lane                            NOT STARTED
```

## Remaining Gate-B lanes

Proceed one lane at a time after this post-merge authority closure is reviewed and merged:

1. SSI2164 package and control-law assumptions;
2. OPA1679 package and decoupling requirements;
3. Return limiter and clamp diodes;
4. service connector and test-point access.

PCB creation, placement, routing, panel CAD, fabrication, purchasing and production remain blocked.
