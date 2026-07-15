# Input and Output Jack Exact-Part Review

## Decision after corrected mechanical fit

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
CORRECT NUT-ONLY PHYSICAL FIT               USER-ATTESTED PASS
EXACT SAMPLE SEATING VALUE                  NOT RECORDED
INDEPENDENT MECHANICAL REVIEW               REQUIRED
FOOTPRINTS ASSIGNED                         NONE
KICAD 10 HIERARCHICAL ERC                   PASS — 0 ERRORS / 0 WARNINGS
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     READY FOR INDEPENDENT REVIEW
```

The electrical-contact, supplier-equivalence, pin-map and PCB-footprint geometry work remains valid. The intended mechanical stack is now correctly defined and physically attested:

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

That supplier-controlled equivalence is accepted for:

- contact arrangement;
- switched-normal behaviour;
- terminal geometry;
- PCB footprint equivalence.

It is not treated as proof of final panel fabrication dimensions.

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

The project owner directly attested that the corrected stack passes all required qualitative checks:

1. the bushing enters the intended panel hole without forcing;
2. the nut starts cleanly without cross-threading;
3. the nut clamps before bottoming;
4. the nut-only stack is secure;
5. the jack cannot rotate or wobble;
6. the housing is not crushed or distorted;
7. tightening does not lift or tilt the soldered jack;
8. tightening does not load the solder terminals;
9. the PCB remains flat;
10. the panel and jack align without lateral force;
11. the 3.00 mm barrel relief clears the physical jack;
12. all electrical terminal holes remain unobstructed.

## Deferred mechanical-release evidence

The following values remain deliberately unclaimed:

- actual finished panel thickness;
- exact assembled PCB-to-panel distance;
- finished panel-hole diameter;
- final panel material and supplier;
- nut thickness and thread pitch unless later required.

The `8.30 mm` seating figure remains a supplier nominal, not a sample measurement. These omissions do not erase the qualitative fit pass, but they keep PCB placement, standoff selection, panel fabrication and purchasing blocked.

## Assignment decision

There is **no footprint assignment before independent review of the corrected panel-stack record**.

J40 and J70 retain blank footprint fields. The project symbol retains a blank default footprint.

The independent reviewer must explicitly:

1. approve the corrected nut-only qualitative fit and transfer the deferred dimensional evidence to the later mechanical-release gate;
2. require named measurements or photographs; or
3. return the record for revision.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PASS
corrected panel stack                  USER-ATTESTED PASS
independent review                     REQUIRED
schematic footprint assignment        BLOCKED
panel material / supplier lock        BLOCKED
actual seating measurement            BLOCKED
pcb / panel fab / purchasing           BLOCKED
```

PCB placement, routing, panel fabrication and purchasing remain blocked.