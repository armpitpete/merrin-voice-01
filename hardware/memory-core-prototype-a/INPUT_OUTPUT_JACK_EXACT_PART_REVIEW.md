# Input and Output Jack Exact-Part Review

## Initial Gate-B decision

```text
J40 INPUT CONTACT CONTRACT                 PASS
J70 OUTPUT CONTACT CONTRACT                PASS
WQP518MA EXACT CANDIDATE                    RETAIN
WQP518MA ↔ PJ398SM DRAWING EQUIVALENCE      NOT YET ACCEPTED
CURRENT NUMERIC SYMBOL PIN MAP              PASS FOR SCHEMATIC USE
SOURCE FOOTPRINT PAD IDENTIFIERS            INCOMPATIBLE WITH CURRENT SYMBOL
PANEL HOLE                                  CANDIDATE ONLY
PANEL-TO-PCB GEOMETRY                       BLOCKED
NUT / WASHER / PANEL STACK                  BLOCKED
FOOTPRINTS ASSIGNED                         NONE
PCB / PANEL FAB / PURCHASING                BLOCKED
OVERALL                                     RETURN FOR BOUNDED REPAIR
```

This lane does not reject the Thonkiconn form factor. It prevents an attractive but unsafe shortcut: assigning a footprint called “Thonkiconn” without proving the exact orderable jack, pad mapping and panel stack.

## Existing schematic intent

Both jacks currently use `MerrinLab_PrototypeA:WQP518MA_APPLICATION` with blank footprint fields.

### J40 input

```text
pin 1 TIP         → INPUT_TIP
pin 2 TIP_NORMAL  → GND
pin 3 SLEEVE      → GND
```

The input depends on the normally closed contact. With no plug inserted, contacts 1 and 2 must be closed so `INPUT_TIP` is grounded. Plug insertion must open the 1–2 path while retaining contact 1 as the signal tip.

### J70 output

```text
pin 1 TIP         → OUTPUT_TIP
pin 2 TIP_NORMAL  → no-connect
pin 3 SLEEVE      → GND
```

The output does not use the normal contact. Leaving pin 2 unconnected is deliberate.

## Exact candidate

The retained orderable candidate is:

```text
Thonkiconn Mono 3.5 mm Audio Jack — WQP518MA
```

Thonk states that `WQP518MA`, `PJ398SM` and `PJ301M-12` are functionally identical and interchangeable. The same supplier page calls the WQP518MA an improved version and says its footprint is unchanged.

The available dimensional drawing is labelled `PJ398SM`, not `WQP518MA`. That supplier-declared equivalence is useful evidence, but it is not yet treated as a manufacturer-controlled WQP518MA drawing.

## Contact and electrical evidence

The drawing identifies a three-contact switched mono socket:

```text
1 = TIP
2 = TIP_NORMAL
3 = SLEEVE
```

Published limits on the drawing are:

```text
rating                         30 V DC, 0.5 A
contact resistance             ≤ 0.03 ohm
insulation resistance          ≥ 100 Mohm at 250 V DC
withstand voltage              500 V AC
insertion / extraction force   3–25 N
life                           5,000 cycles
```

These limits are adequate for the current low-voltage audio use. Contact life and real switching reliability remain physical-sample and endurance matters rather than schematic claims.

## Mechanical and PCB drawing evidence

The supplier drawing shows:

```text
body width                     9.0 mm
body depth shown               9.0 mm
body height shown              8.3 mm
front projection shown         5.5 mm
rear contact projection shown  3.5 mm
bushing diameter               6.0 mm

TIP centre                     y = -4.92 mm
TIP_NORMAL centre              y = +3.38 mm
SLEEVE centre                  y = +6.48 mm

TIP / TIP_NORMAL holes         0.6 × 1.5 mm
SLEEVE hole                    0.6 × 1.3 mm
```

The drawing also advises either a `3 mm` PCB relief hole directly below the jack barrel or an equivalent void in the ground plane with no traces routed through that region.

## Pinned footprint candidate

The strongest available candidate footprint is pinned from:

```text
repository  clacktronics/AudioJacks
commit      14a88866e93b8ce4a31ad376b0c6eb85cd4d2cf3
path        AudioJacks.pretty/Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical.kicad_mod
Git blob    1ebfa641294a0fd38f9c0e2c5c8b85dbc71ccaf6
SHA-256     9f54f81d8f0152e77082746b47158c297c84154dd6fbe0b459ef147a86b10678
```

Its terminal centres match the drawing:

```text
T   (0, -4.92 mm)
TN  (0, +3.38 mm)
S   (0, +6.48 mm)
```

The footprint uses `1.6 × 0.6 mm` oval drills for all three terminals. This gives 0.1 mm length clearance over the drawing’s 1.5 mm TIP/TN tabs and 0.3 mm over the 1.3 mm sleeve tab.

The upstream library labels its own testing status as `Untested`. The footprint is therefore evidence and a starting geometry, not an accepted authority by reputation alone.

## Blocking pin-map defect

The current schematic symbol uses numeric physical pins:

```text
1 = TIP
2 = TIP_NORMAL
3 = SLEEVE
```

The source footprint uses semantic pad identifiers:

```text
T
TN
S
```

KiCad connects symbols to footprints by matching identifiers. A direct assignment would not connect numeric symbol pins to semantic footprint pads.

Required bounded repair:

- create a project-local numeric footprint with `1=T`, `2=TN`, `3=S`; or
- deliberately change the project symbol and every dependent validator to semantic identifiers.

The numeric project-local footprint is the lower-risk option because the schematic already expresses the physical contact numbers clearly.

## Panel and mounting status

The intended mounting method is:

```text
vertical PCB solder mounting
+
front-panel bushing through a clearance hole
+
front-panel nut and washer retention
```

The drawing shows a `6.0 mm` bushing. A `6.5 mm` panel hole is recorded only as a candidate clearance, not an accepted production dimension.

Acceptance remains blocked because the current evidence does not fix:

- the exact bushing thread;
- exact nut type;
- exact washer type;
- maximum compatible panel thickness;
- accepted panel-to-PCB seating distance;
- tolerance between the PCB jack origin and the panel-hole centre.

These must be established by a manufacturer/supplier mechanical record or by a controlled physical sample measurement before panel CAD or PCB placement.

## Next bounded repair

1. Obtain or create controlled evidence that the orderable WQP518MA uses the PJ398SM drawing geometry.
2. Select the exact nut and washer arrangement.
3. Establish panel hole, panel thickness and panel-to-PCB seating tolerances.
4. Create a numeric project-local footprint with `1=T`, `2=TN`, `3=S` and the required barrel keepout.
5. Validate the footprint independently against the drawing and the selected physical sample or controlled source.
6. Amend J40 and J70 only after those checks pass.
7. Rerun jack validators and KiCad hierarchical ERC.
8. Return the lane for an explicit approval-or-rejection review.

PCB placement, routing, panel fabrication and purchasing remain blocked.
