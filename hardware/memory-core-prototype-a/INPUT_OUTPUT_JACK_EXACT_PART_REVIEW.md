# Input and Output Jack Exact-Part Review

## Final decision

```text
J40 INPUT CONTACT CONTRACT                 PASS
J70 OUTPUT CONTACT CONTRACT                PASS
WQP518MA EXACT ORDERABLE JACK               PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE     PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT             PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT             PASS — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                     PASS
PANEL NOMINAL THICKNESS                     1.60 MM
PANEL MATERIAL / SUPPLIER                   PROVISIONAL
HEX NUT PRODUCT VARIANT                     SELECTED
WASHER                                      NONE
CORRECT NUT-ONLY PHYSICAL FIT               APPROVED
INDEPENDENT MECHANICAL REVIEW               PASS
J40 FOOTPRINT FIELD                         ASSIGNED
J70 FOOTPRINT FIELD                         ASSIGNED
PROJECT SYMBOL DEFAULT                      BLANK
POST-ASSIGNMENT VALIDATION                  PASS
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     READY FOR MERGE REVIEW
```

The current authoritative stack is:

```text
1.60 mm nominal panel + selected Thonk hex nut + no washer
```

The former `2.00 mm aluminium panel + washer + nut` result is withdrawn and is not used as evidence.

## Supplier-controlled equivalence

Selected orderable jack:

```text
Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
```

Thonk states that WQP518MA, PJ301M-12 and PJ398SM are functionally identical and interchangeable, and that the WQP518MA footprint is unchanged.

That equivalence is accepted for contact arrangement, switched-normal behaviour, terminal geometry and PCB footprint equivalence. It is not proof of final panel fabrication dimensions.

## Schematic contracts

### J40 input

```text
pin 1 TIP         → INPUT_TIP
pin 2 TIP_NORMAL  → GND
pin 3 SLEEVE      → GND
```

Contacts 1 and 2 are closed with no plug inserted. Inserting a plug opens the normal contact and leaves contact 1 connected to the plug tip.

### J70 output

```text
pin 1 TIP         → OUTPUT_TIP
pin 2 TIP_NORMAL  → no-connect
pin 3 SLEEVE      → GND
```

The output normal contact is deliberately unused.

## Footprint authority

```text
repository  KiCad/kicad-footprints
commit      7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
path        Connector_Audio.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod
Git blob    6c9440c957bf566ae79058cdab7afabfb86955d8
SHA-256     8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
```

Project-local footprint:

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
1 = T  = TIP
2 = TN = TIP_NORMAL
3 = S  = SLEEVE
3.00 mm NPTH at the published jack-barrel centre
SHA-256 e9e095c63fa39dfd306a45755b6e8e9048e795b8592a6eeba3bf6ab734ed3685
```

The electrical pad centres, sizes and drills match the pinned official KiCad source geometry. J40 and J70 now use this numeric footprint. The project symbol default remains blank so the decision is instance-specific.

## Corrected panel and hardware stack

```text
panel nominal thickness      1.60 mm
panel material               provisional FR-4 PCB panel
panel supplier               not locked; JLCPCB only a possibility
nut                          selected Thonk hex nut
washer                       none
threaded bushing length      4.50 mm supplier nominal
available above panel        2.90 mm nominal
panel-to-PCB seating         8.30 mm supplier nominal; not measured
```

The project owner attested that the corrected stack passes clean insertion, clean nut start, clamping before bottoming, secure retention, no rotation or wobble, no housing distortion, no jack lift or tilt, no solder-terminal loading, no PCB bow, no forced alignment, 3.00 mm barrel-relief clearance and unobstructed terminal holes.

## Independent review and assignment history

The corrected physical-fit record was reviewed at:

```text
2d1e58e61b1a04653b17cd666dda2160808079cf
```

The review found:

```text
corrected stack identity                 PASS
qualitative retention and stress checks  PASS
barrel-relief and terminal clearance      PASS
evidence limitations                      ACCEPTED WITH EXPLICIT TRANSFER
```

That review authorised assignment as a later bounded action. At the review point only, the footprint fields were blank. This is superseded pre-assignment history, not the current state.

Assignment was applied in:

```text
f34eea95c216cd31df4d4e3f1498adc4b9014ec9
```

Current assignment state:

```text
J40 footprint field               ASSIGNED
J70 footprint field               ASSIGNED
project symbol default            BLANK
controlled generators             UPDATED
post-assignment validation        PASS
```

## Validation authority

Two distinct validation stages are retained without conflation:

```text
assignment-state validation head  bbc54c59152fdab8ac42ad0035a163e2e383c92b
restored-workflow validation head  5e07b4657436c19db32ea9651ee68e510df402eb
```

The first validated the assigned engineering state and recorded the assignment evidence. The second restored the normal read-only workflow and passed the complete untouched chain. A fresh chain is required on the repository-authority synchronisation head before merge review.

## Deferred mechanical-release evidence

The following remain deliberately unclaimed:

- final panel material and supplier;
- actual finished panel thickness or controlled supplier tolerance;
- exact assembled PCB-to-panel distance;
- finished panel-hole diameter and manufacturing tolerance;
- any resulting axis-offset correction.

Nut thickness, thread pitch and photographs remain optional unless the final stack no longer reproduces the accepted fit.

These omissions do not invalidate the schematic footprint assignment. They continue to block PCB creation, placement, routing, standoff selection, panel CAD, panel fabrication and purchasing.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PASS
corrected panel stack                  INDEPENDENTLY APPROVED
bounded J40/J70 footprint assignment  COMPLETE
project symbol default                BLANK
PCB creation / placement / routing    BLOCKED
panel CAD / fabrication               BLOCKED
purchasing / production               BLOCKED
PR #47 merge                          AWAITING REVIEW
```

PR #47 remains draft and unmerged.