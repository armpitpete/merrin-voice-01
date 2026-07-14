# Input and Output Jack Exact-Part Review

## Decision after bounded repair

```text
J40 INPUT CONTACT CONTRACT                 PASS
J70 OUTPUT CONTACT CONTRACT                PASS
WQP518MA EXACT ORDERABLE JACK               PASS FOR CONTACT / PCB GEOMETRY
WQP518MA ↔ PJ398SM SUPPLIER EQUIVALENCE     PASS FOR CONTACT / PCB GEOMETRY
OFFICIAL KICAD SOURCE FOOTPRINT             PINNED AND VERIFIED
NUMERIC PROJECT-LOCAL FOOTPRINT             CREATED — 1 / 2 / 3
3 MM BARREL RELIEF NPTH                     INCLUDED
PANEL HOLE TARGET                           6.50 +0.10 / -0.00 MM — DERIVED
HEX NUT PRODUCT VARIANT                     SELECTED
WASHER PRODUCT VARIANT                      SELECTED
THREAD / NUT / WASHER DIMENSIONS            NOT PUBLISHED
2 MM PANEL STACK                            NOT YET FIT-PROVEN
PHYSICAL SAMPLE                             REQUIRED
FOOTPRINTS ASSIGNED                         NONE
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     HUMAN MEASUREMENT REQUIRED
```

This repair closes the electrical-contact, supplier-equivalence, pin-map and PCB-footprint geometry defects. It does not close the panel stack. Product photographs and generic thread assumptions are not accepted as dimensional evidence.

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

It is not treated as evidence for unpublished nut, washer or thread-stack dimensions.

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

The new footprint authority is the official KiCad WQP/PJ398SM footprint at immutable revision:

```text
repository  KiCad/kicad-footprints
commit      7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
path        Connector_Audio.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod
Git blob    6c9440c957bf566ae79058cdab7afabfb86955d8
SHA-256     8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc
```

The earlier untested `clacktronics/AudioJacks` snapshot remains historical comparison evidence only. It is not the accepted source geometry.

## Numeric project-local footprint

Created footprint:

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
nominal panel-to-PCB seating   8.30 mm, pending sample confirmation
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

The drawing leaves `2.50 mm` of shown threaded length above a `2.00 mm` panel before accounting for washer thickness, nut thickness and required engagement. That stack cannot be accepted without measurements.

## Required physical sample evidence

Complete `WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md` using one actual WQP518MA, the selected Thonk hex nut, the selected Thonk washer and a 2.00 mm panel coupon.

The required checks include:

1. thread pitch and major diameter;
2. usable threaded length;
3. nut and washer dimensions;
4. secure engagement through the 2 mm panel;
5. measured PCB-to-panel seating distance;
6. confirmation that panel tightening does not lift the jack or load its solder joints;
7. confirmation that the 3 mm barrel relief clears the physical part.

## Assignment decision

The project-local footprint is ready for independent geometry validation, but **no footprint assignment before the panel stack passes**.

J40 and J70 therefore retain blank footprint fields. The project symbol also retains a blank default footprint.

## Current boundary

```text
contact and switching contract        PASS
supplier-controlled equivalence       PASS FOR CONTACT / PCB GEOMETRY
official source footprint provenance  PASS
numeric footprint geometry            PENDING CURRENT-HEAD CI
panel-hole target                      RECORDED, NOT FABRICATION AUTHORITY
nut and washer products               SELECTED
dimensional panel stack               BLOCKED
schematic footprint assignment        BLOCKED
```

PCB placement, routing, panel fabrication and purchasing remain blocked.
