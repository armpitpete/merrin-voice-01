# Exact-Part and Footprint Verification Register

## Authority

```text
Gate A — schematic acceptance       PASS / MERGED
Gate B — exact parts / footprints   ACTIVE
Gate C — bench acceptance           NOT STARTED
Gate D — PCB / production           BLOCKED
```

Gate B may correct schematic assumptions and accept individually reviewed package mappings. It does not authorise PCB placement, routing, panel fabrication, purchasing or production claims.

## Verification rule

An active device or connector is accepted only when all of these are traceable:

1. exact manufacturer and orderable part number;
2. manufacturer or controlled supplier datasheet;
3. package or mechanical designation and dimensional envelope;
4. physical pin/contact numbering and symbol mapping;
5. electrical and switching behaviour in the actual circuit use;
6. immutable upstream revision and SHA-256-locked project-local footprint bytes;
7. independent dimensional comparison for every exact package or connector;
8. panel geometry and mounting-stack requirements where applicable;
9. explicit transfer of remaining physical and measured gates.

A generic class name, supplier nickname, claimed interchangeability, moving library branch or footprint-name match is not acceptance evidence by itself.

## Lane 01 — output mute and fault-control path

```text
STATUS                                  APPROVED AND MERGED
PR                                      #46
APPROVED HEAD                           c5b6551bbd6b577057bad571a9f051e8a39966c7
MAIN SQUASH COMMIT                      651d594e3c9993b2fdc6ca527328887458a7d849
Q70 MMBFJ113 / CASE 318-08              APPROVED
Q71 PMV20XNE / TO-236AB                 APPROVED
U70 VO617A-3X007T / OPTION-7 SMD-4      APPROVED
POWERED HEALTHY-RELEASE TOPOLOGY        APPROVED AT CALCULATED LEVEL
KICAD 10 HIERARCHICAL ERC               PASS — 0 / 0
MEASURED / FULL-TEMPERATURE BEHAVIOUR   GATE C
PCB / ROUTING / FAB / PURCHASING        BLOCKED
```

Detailed records:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`
- `07_OUTPUT_MUTE_PROTECTION_VALIDATION.md`
- `OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json`

Lane 01 is canonical on `main`. Gate C retains measured mute depth, full-temperature optocoupler release, pop energy, real rail sequencing, output loading and endurance.

## Lane 02 — input and output jacks

Detailed records:

- `JACK_EXACT_PART_EDIT_CONTRACT.md`
- `INPUT_OUTPUT_JACK_AUDIT.json`
- `INPUT_OUTPUT_JACK_EXACT_PART_REVIEW.md`
- `WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md`
- `jack-footprint-audits/KiCad_Official_Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod`
- `MerrinLab_PrototypeA.pretty/Jack_3.5mm_Thonkiconn_WQP518MA_Numeric.kicad_mod`

Current result:

```text
STATUS                                      ACTIVE — INDEPENDENT REVIEW GATE
J40 INPUT CONTACT CONTRACT                  PASS
J70 OUTPUT CONTACT CONTRACT                 PASS
WQP518MA ORDERABLE JACK                      PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE      PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT              PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT              PASS — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                      PASS
PANEL HOLE TARGET                            6.50 +0.10 / -0.00 MM — DERIVED
HEX NUT PRODUCT VARIANT                      SELECTED
WASHER PRODUCT VARIANT                       SELECTED
2 MM PANEL STACK                             USER-ATTESTED PASS
NO JACK LIFT / TERMINAL LOADING              USER-ATTESTED PASS
3 MM PHYSICAL BARREL CLEARANCE               USER-ATTESTED PASS
PCB-TO-PANEL ALIGNMENT                       USER-ATTESTED PASS
EXACT SAMPLE SEATING VALUE                   DEFERRED — 8.30 MM SUPPLIER NOMINAL
THREAD / NUT / WASHER DIMENSIONS             DEFERRED
INDEPENDENT MECHANICAL REVIEW                REQUIRED
J40 / J70 FOOTPRINT FIELDS                   BLANK
KICAD 10 HIERARCHICAL ERC                    PASS — 0 / 0
PCB / PANEL FAB / PURCHASING                 BLOCKED
```

### Existing contact contracts

| Ref | Role | Contact 1 | Contact 2 | Contact 3 | Required switching behaviour |
|---|---|---|---|---|---|
| J40 | input | `TIP → INPUT_TIP` | `TIP_NORMAL → GND` | `SLEEVE → GND` | contacts 1–2 closed with no plug; open on insertion |
| J70 | output | `TIP → OUTPUT_TIP` | no-connect | `SLEEVE → GND` | normal contact deliberately unused |

### Accepted supplier-equivalence scope

```text
orderable jack        Thonkiconn WQP518MA
controlled drawing    PJ398SM
accepted scope         contacts, switching and PCB footprint geometry
excluded scope         unpublished numerical thread, nut and washer dimensions
```

Thonk explicitly states that WQP518MA, PJ398SM and PJ301M-12 are functionally identical and interchangeable and that the WQP518MA footprint is unchanged. That controlled supplier statement is accepted for the limited scope above.

### Official footprint authority

```text
repository  KiCad/kicad-footprints
commit      7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
path        Connector_Audio.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod
Git blob    6c9440c957bf566ae79058cdab7afabfb86955d8
SHA-256     8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
```

### Numeric project footprint

```text
library id  MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
1           TIP
2           TIP_NORMAL
3           SLEEVE
barrel       3.00 mm NPTH at published centre
SHA-256      e9e095c63fa39dfd306a45755b6e8e9048e795b8592a6eeba3bf6ab734ed3685
```

The numeric footprint copies the official electrical pad geometry exactly and resolves the earlier `1/2/3` versus `T/TN/S` mismatch. It remains unassigned.

### Validation evidence

Measurement-record head:

```text
e64365a017abe0e35df6024dc0721837e1a15426
```

```text
KiCad jack exact-part verification  run 29405232875  PASS
KiCad schematic ERC                 run 29405232999  PASS
Current schematic stage authority   run 29405232860  PASS
Hierarchical ERC                     0 errors / 0 warnings
Footprint assignment                 remained blank
```

### Mechanical record outcome

The project owner reported on 15 July 2026 that all required functional fit checks passed for:

1. secure Thonk hex-nut and washer engagement through the 2.00 mm aluminium panel;
2. no lifting or tilting of the soldered jack during tightening;
3. no mechanical loading of its solder terminals;
4. natural PCB-to-panel alignment;
5. clearance of the physical jack through the 3.00 mm NPTH barrel relief;
6. unobstructed electrical terminal holes.

The exact sample calliper reading for PCB-to-panel seating was not recorded. The `8.30 mm` value remains the supplier-drawing nominal, not a measured sample value. Exact thread, nut and washer dimensions were also deliberately deferred.

This is a user-attested qualitative fit result. It now requires independent review. That review must explicitly accept the deferral, name required corrections, or return the mechanical record for revision.

### Current boundary

```text
physical-fit attestation              RECORDED
independent mechanical review         REQUIRED
schematic footprint assignment        BLOCKED
PCB placement and routing             BLOCKED
panel fabrication                     BLOCKED
purchasing                            BLOCKED
```

Only after independent approval may the project-local footprint be assigned to J40 and J70 and KiCad ERC rerun.

## Remaining Gate-B lanes

Proceed one lane at a time after Lane 02 is deliberately resolved:

1. SSI2164 package and control-law assumptions;
2. OPA1679 package and decoupling requirements;
3. Return limiter and clamp diodes;
4. service connector and test-point access.

PCB placement, routing, panel fabrication, purchasing and production remain blocked.