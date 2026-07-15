# Input and Output Jack Exact-Part Review

## Decision after bounded repair

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
WASHER PRODUCT VARIANT                      SELECTED
2 MM PANEL STACK                            USER-ATTESTED PASS
NO JACK LIFT / TERMINAL LOADING             USER-ATTESTED PASS
PHYSICAL 3 MM BARREL CLEARANCE              USER-ATTESTED PASS
PCB-TO-PANEL ALIGNMENT                      USER-ATTESTED PASS
EXACT SAMPLE SEATING VALUE                  DEFERRED
THREAD / NUT / WASHER DIMENSIONS            DEFERRED
INDEPENDENT MECHANICAL REVIEW               REQUIRED
FOOTPRINTS ASSIGNED                         NONE
KICAD 10 HIERARCHICAL ERC                   PASS — 0 ERRORS / 0 WARNINGS
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     READY FOR INDEPENDENT REVIEW
```

This repair closes the electrical-contact, supplier-equivalence, pin-map and PCB-footprint geometry defects. The project owner has now attested that the physical fit checks pass. Exact sample dimensions were deliberately not supplied and remain visible as deferred evidence.

## Supplier-controlled equivalence

The selected orderable jack remains:

```text
Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
```

Thonk's controlled product page explicitly states that WQP518MA, PJ301M-12 and PJ398SM are functionally identical and interchangeable. It separately states that WQP518MA is the improved version and that its footprint is unchanged.

That supplier statement is accepted for:

- contact arrangement;
- switched-normal behaviour;
- terminal geometry;
- PCB footprint equivalence.

It is not treated as evidence for unpublished nut, washer or thread dimensions.

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

The footprint authority is the official KiCad WQP/PJ398SM footprint at immutable revision:

```text
repository  KiCad/kicad-footprints
commit      7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
path        Connector_Audio.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod
Git blob    6c9440c957bf566ae79058cdab7afabfb86955d8
SHA-256     8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
```

The earlier untested `clacktronics/AudioJacks` snapshot remains historical comparison evidence only. It is not the accepted source geometry.

## Numeric project-local footprint

Validated footprint:

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
```

Physical mapping:

```text
1 = T  = TIP
2 = TN = TIP_NORMAL
3 = S  = SLEEVE
```

The electrical pad centres, sizes and drills match the pinned official KiCad geometry exactly. The project-local footprint adds one deliberate mechanical feature:

```text
3.00 mm NPTH at the published jack-barrel centre
```

This implements the supplier drawing's advised barrel relief rather than relying only on a text keepout.

## Panel target and tolerance calculation

The supplier drawing shows:

```text
bushing diameter nominal       6.00 mm
general drawing tolerance      ±0.15 mm
threaded bushing length shown  4.50 mm
body height shown              8.30 mm
```

Recorded project targets:

```text
panel material                 aluminium
panel thickness                2.00 mm
panel hole                     6.50 +0.10 / -0.00 mm
maximum total axis offset      0.15 mm
nominal panel-to-PCB seating   8.30 mm supplier nominal
```

At the maximum drawn bushing diameter of `6.15 mm` and minimum panel hole of `6.50 mm`, the minimum radial clearance before positional error is `0.175 mm`. The `0.15 mm` total axis-offset target therefore remains inside the derived clearance.

These are controlled design targets, not panel-fabrication authority.

## Mounting hardware selection

Selected supplier-compatible products from the same WQP518MA product page:

```text
nut      Thonkiconn Hex Nuts product variant
washer   Thonkiconn Washers product variant
```

The supplier page proves that these are sold for the Thonkiconn family. It does not publish:

- bushing thread pitch;
- nut thickness;
- washer thickness;
- washer inside and outside diameters;
- minimum secure thread engagement;
- maximum permitted panel thickness.

The drawing leaves `2.50 mm` of shown threaded length above a `2.00 mm` panel before accounting for washer thickness, nut thickness and required engagement. The project owner has physically attested that the selected stack clamps securely despite those unpublished dimensions.

## Physical sample record

`WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md` now records project-owner pass statements for:

1. secure engagement through the 2.00 mm panel;
2. correct nut start and clamping before bottoming;
3. no housing distortion;
4. no jack rotation or wobble after tightening;
5. no lift or tilt of the soldered jack;
6. no mechanical loading of the solder terminals;
7. natural PCB-to-panel alignment;
8. physical clearance through the 3.00 mm barrel relief;
9. unobstructed terminal holes.

The record does **not** claim that unprovided dimensions were measured. The exact PCB-to-panel sample distance remains unrecorded; `8.30 mm` remains the supplier nominal. Thread pitch, nut thickness and washer dimensions are also deferred.

## Validation evidence

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

The validator independently compared the numeric `1/2/3` pad geometry with the pinned official `T/TN/S` source geometry and verified the 3 mm NPTH barrel relief.

## Assignment decision

The project-local footprint has passed geometry validation, but **no footprint assignment before the panel stack passes** and receives independent review.

The physical-fit record is now ready for that review. J40 and J70 retain blank footprint fields. The project symbol also retains a blank default footprint.

The independent reviewer must explicitly choose one outcome:

1. approve the qualitative physical-fit evidence and transfer the deferred numerical dimensions to a later controlled mechanical gate;
2. require named measurements or photographs; or
3. return the record for revision.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PASS
panel-hole target                      RECORDED, NOT FABRICATION AUTHORITY
nut and washer products               SELECTED
physical-fit checks                    USER-ATTESTED PASS
exact sample dimensions                DEFERRED
independent review                     REQUIRED
schematic footprint assignment        BLOCKED
```

PCB placement, routing, panel fabrication and purchasing remain blocked.