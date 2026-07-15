# Input and Output Jack Exact-Part Review

## Decision after corrected mechanical definition

```text
J40 INPUT CONTACT CONTRACT                 PASS
J70 OUTPUT CONTACT CONTRACT                PASS
WQP518MA EXACT ORDERABLE JACK               PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE     PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT             PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT             PASS — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                     PASS AS FOOTPRINT GEOMETRY
PANEL HOLE TARGET                           6.50 +0.10 / -0.00 MM — DERIVED
HEX NUT PRODUCT VARIANT                     SELECTED
WASHER                                      NONE
PANEL NOMINAL THICKNESS                     1.60 MM
PANEL MATERIAL / SUPPLIER                   PROVISIONAL
AVAILABLE THREAD BEFORE NUT                 2.90 MM NOMINAL
CORRECT NUT-ONLY PHYSICAL FIT               PENDING
PREVIOUS 2 MM + WASHER ATTESTATION          WITHDRAWN
FOOTPRINTS ASSIGNED                         NONE
KICAD 10 HIERARCHICAL ERC                   PASS — 0 ERRORS / 0 WARNINGS
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     STOPPED FOR CORRECT-STACK FIT
```

The electrical-contact, supplier-equivalence, pin-map and PCB-footprint geometry work remains valid. The mechanical record was corrected after the project owner clarified that the intended stack uses a nominal `1.60 mm` panel and the selected Thonk hex nut, with no washer.

The former user-attested pass described a `2.00 mm aluminium panel + washer + nut` stack. Because that is not the intended assembly, the pass is withdrawn and cannot support footprint assignment.

## Supplier-controlled equivalence

The selected orderable jack remains:

```text
Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
```

Thonk states that WQP518MA, PJ301M-12 and PJ398SM are functionally identical and interchangeable, and that the WQP518MA footprint is unchanged.

That supplier-controlled equivalence is accepted for:

- contact arrangement;
- switched-normal behaviour;
- terminal geometry;
- PCB footprint equivalence.

It is not treated as proof of the final panel stack.

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

The corrected stack has `0.40 mm` more nominal thread than the rejected 2.00 mm panel assumption, and no washer thickness is deducted. This makes secure engagement more likely but does not prove it.

## Required physical sample evidence

The physical sample must use the actual WQP518MA, the selected nut, no washer and a representative nominal `1.60 mm` panel or coupon.

It must confirm:

1. the nut starts cleanly;
2. the nut clamps before bottoming;
3. the nut-only stack is secure;
4. the jack cannot rotate or wobble;
5. tightening does not lift or tilt the soldered jack;
6. tightening does not load its solder terminals;
7. the PCB remains flat;
8. the panel and jack align without lateral force;
9. the 3.00 mm barrel relief clears the physical jack;
10. the electrical terminal holes remain unobstructed.

The actual PCB-to-panel distance must be recorded before PCB and panel geometry becomes irreversible. The panel material, supplier and finished thickness must be locked before fabrication release.

## Assignment decision

There is **no footprint assignment before the panel stack passes** physical confirmation and independent review.

J40 and J70 retain blank footprint fields. The project symbol retains a blank default footprint.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PASS
corrected panel stack                  DEFINED, NOT FIT-PROVEN
physical sample                        REQUIRED
independent review                     NOT READY
schematic footprint assignment        BLOCKED
pcb / panel fab / purchasing           blocked
```

PCB placement, routing, panel fabrication and purchasing remain blocked.