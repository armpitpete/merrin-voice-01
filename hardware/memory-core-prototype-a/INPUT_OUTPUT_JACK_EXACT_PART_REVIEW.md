# Input and Output Jack Exact-Part Review

## Decision after independent mechanical review

```text
J40 INPUT CONTACT CONTRACT                 PASS
J70 OUTPUT CONTACT CONTRACT                PASS
WQP518MA EXACT ORDERABLE JACK               PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE     PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT             PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT             PASS — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                     PASS
PANEL HOLE TARGET                           6.50 +0.10 / -0.00 MM — DERIVED
HEX NUT PRODUCT VARIANT                     SELECTED
WASHER                                      NONE
PANEL NOMINAL THICKNESS                     1.60 MM
PANEL MATERIAL / SUPPLIER                   PROVISIONAL
AVAILABLE THREAD BEFORE NUT                 2.90 MM NOMINAL
CORRECT NUT-ONLY PHYSICAL FIT               APPROVED
INDEPENDENT MECHANICAL REVIEW               PASS
FOOTPRINTS ASSIGNED                         NONE
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     READY FOR BOUNDED FOOTPRINT ASSIGNMENT
```

The electrical-contact, supplier-equivalence, pin-map and PCB-footprint geometry work remains valid. The corrected mechanical stack is:

```text
1.60 mm nominal panel + selected Thonk hex nut + no washer
```

The former `2.00 mm aluminium panel + washer + nut` result remains withdrawn and is not used as evidence.

## Supplier-controlled equivalence

The selected orderable jack remains:

```text
Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
```

Thonk states that WQP518MA, PJ301M-12 and PJ398SM are functionally identical and interchangeable, and that the WQP518MA footprint is unchanged.

That equivalence is accepted for contact arrangement, switched-normal behaviour, terminal geometry and PCB footprint equivalence. It is not treated as proof of final panel fabrication dimensions.

## Existing schematic contracts

### J40 input

```text
pin 1 TIP         → INPUT_TIP
pin 2 TIP_NORMAL  → GND
pin 3 SLEEVE      → GND
```

Contacts 1 and 2 must be closed with no plug inserted. Inserting a plug opens the normal contact and leaves contact 1 connected to the plug tip.

### J70 output

```text
pin 1 TIP         → OUTPUT_TIP
pin 2 TIP_NORMAL  → no-connect
pin 3 SLEEVE      → GND
```

The output normal contact is deliberately unused.

## Official source geometry

```text
repository  KiCad/kicad-footprints
commit      7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
path        Connector_Audio.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod
Git blob    6c9440c957bf566ae79058cdab7afabfb86955d8
SHA-256     8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
```

## Numeric project-local footprint

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
1 = T  = TIP
2 = TN = TIP_NORMAL
3 = S  = SLEEVE
3.00 mm NPTH at published jack-barrel centre
```

The electrical pad centres, sizes and drills match the pinned official KiCad source geometry exactly. The footprint remains unassigned.

## Corrected panel and hardware stack

```text
panel nominal thickness      1.60 mm
panel material               provisional FR-4 PCB panel
panel supplier               not locked; JLCPCB only a possibility
nut                          selected Thonk hex nut
washer                       none
threaded bushing length      4.50 mm supplier nominal
available above panel        4.50 - 1.60 = 2.90 mm nominal
panel-to-PCB seating         8.30 mm supplier nominal
```

The project owner directly attested that the corrected stack passes the complete qualitative fit set: clean insertion, clean nut start, clamping before bottoming, secure retention, no rotation or wobble, no housing distortion, no jack lift or tilt, no solder-terminal loading, no PCB bow, no forced alignment, physical clearance through the 3.00 mm barrel relief and unobstructed terminal holes.

## Independent review

`WQP518MA_PANEL_STACK_INDEPENDENT_REVIEW.md` independently reviewed the corrected record at head:

```text
2d1e58e61b1a04653b17cd666dda2160808079cf
```

Findings:

```text
corrected stack identity                 PASS
qualitative retention and stress checks  PASS
barrel-relief and terminal clearance      PASS
evidence limitations                      ACCEPTED WITH EXPLICIT TRANSFER
```

Decision:

```text
corrected physical fit                   APPROVED
next bounded footprint-assignment gate   AUTHORISED
footprint assignment by this review      NOT PERFORMED
```

## Deferred mechanical-release evidence

The following remain deliberately unclaimed and transferred to a later mechanical-release gate:

- final panel material and supplier;
- actual finished panel thickness or controlled supplier tolerance;
- exact assembled PCB-to-panel distance;
- finished panel-hole diameter and manufacturing tolerance;
- any resulting axis-offset correction.

Nut thickness, thread pitch and photographs remain optional unless the final physical stack no longer reproduces the accepted fit.

These omissions do not block assignment of the already validated footprint. They continue to block PCB placement, standoff selection, panel fabrication and purchasing.

## Assignment decision

The next bounded gate may assign:

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
```

to J40 and J70, regenerate the controlled schematic sources, rerun KiCad hierarchical ERC and update the lane evidence.

This review does not perform that assignment.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PASS
corrected panel stack                  INDEPENDENTLY APPROVED
schematic footprint assignment        NOT YET PERFORMED
panel material / supplier lock        BLOCKED
actual seating measurement            BLOCKED
PCB placement / panel fab / purchase  BLOCKED
PR #47 merge                           NOT REVIEWED
```

PCB placement, routing, panel fabrication and purchasing remain blocked.