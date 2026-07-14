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
- `jack-footprint-audits/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical.kicad_mod`

Current result:

```text
STATUS                                      ACTIVE — INITIAL EVIDENCE GATE
J40 INPUT CONTACT CONTRACT                  PASS
J70 OUTPUT CONTACT CONTRACT                 PASS
WQP518MA ORDERABLE CANDIDATE                 RETAIN
WQP518MA ↔ PJ398SM DRAWING EQUIVALENCE       NOT YET ACCEPTED
CURRENT NUMERIC SYMBOL PINS 1 / 2 / 3        PASS FOR SCHEMATIC USE
PINNED SOURCE FOOTPRINT T / TN / S           GEOMETRY RECORDED
DIRECT FOOTPRINT ASSIGNMENT                  FAIL — IDENTIFIERS DO NOT MATCH
PANEL HOLE                                   CANDIDATE ONLY
PANEL-TO-PCB SEATING                         BLOCKED
EXACT NUT / WASHER / PANEL STACK             BLOCKED
J40 / J70 FOOTPRINT FIELDS                   BLANK
PCB / PANEL FAB / PURCHASING                 BLOCKED
```

### Existing contact contracts

| Ref | Role | Contact 1 | Contact 2 | Contact 3 | Required switching behaviour |
|---|---|---|---|---|---|
| J40 | input | `TIP → INPUT_TIP` | `TIP_NORMAL → GND` | `SLEEVE → GND` | contacts 1–2 closed with no plug; open on insertion |
| J70 | output | `TIP → OUTPUT_TIP` | no-connect | `SLEEVE → GND` | normal contact deliberately unused |

### Retained candidate

```text
orderable candidate   Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
drawing model label   PJ398SM
connector             switched 3.5 mm mono TS, vertical PCB mount
physical contacts     1 TIP / 2 TIP_NORMAL / 3 SLEEVE
```

Thonk's interchangeability statement is recorded as supplier evidence. The lane does not yet treat a PJ398SM-labelled drawing as a manufacturer-controlled WQP518MA drawing.

### Pinned candidate footprint

```text
repository  clacktronics/AudioJacks
commit      14a88866e93b8ce4a31ad376b0c6eb85cd4d2cf3
path        AudioJacks.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical.kicad_mod
Git blob    1ebfa641294a0fd38f9c0e2c5c8b85dbc71ccaf6
SHA-256     9f54f81d8f0152e77082746b47158c297c84154dd6fbe0b459ef147a86b10678
upstream testing status  UNTESTED
```

The terminal centres match the supplier drawing, but the footprint uses semantic pads `T`, `TN`, `S`. The current project symbol uses numeric identifiers `1`, `2`, `3`. Direct assignment is prohibited.

### Current panel and mounting status

```text
bushing diameter shown       6.0 mm
candidate panel clearance    6.5 mm — not accepted
exact thread                  unknown
exact nut                     not selected
exact washer                  not selected
maximum panel thickness       unknown
panel-to-PCB seating          not accepted
barrel relief / keepout       required
```

### Required bounded repair

1. Establish controlled WQP518MA-to-PJ398SM dimensional equivalence.
2. Select exact nut and washer hardware.
3. Establish panel-hole, panel-thickness and panel-to-PCB tolerances.
4. Create an independently reviewed numeric project-local footprint with `1=T`, `2=TN`, `3=S` and barrel keepout.
5. Only after those checks pass, amend J40 and J70 and assign the footprint.
6. Rerun jack validators and KiCad hierarchical ERC.
7. Return the lane for deliberate approval or rejection.

## Remaining Gate-B lanes

Proceed one lane at a time after Lane 02 is deliberately resolved:

1. SSI2164 package and control-law assumptions;
2. OPA1679 package and decoupling requirements;
3. Return limiter and clamp diodes;
4. service connector and test-point access.

PCB placement, routing, panel fabrication, purchasing and production remain blocked.
