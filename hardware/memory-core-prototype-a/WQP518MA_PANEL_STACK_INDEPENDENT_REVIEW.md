# WQP518MA Corrected Panel-Stack Independent Review

## Review scope

This review covers only the corrected mechanical fit record for the input and output jack stack:

```text
jack                         Thonkiconn WQP518MA mono switched jack
retaining hardware           selected Thonk hex nut
washer                       none
panel nominal thickness      1.60 mm
panel material / supplier    provisional; not locked
PCB barrel relief            3.00 mm NPTH at jack barrel centre
```

It does not review or authorise footprint assignment, PCB placement, routing, standoff selection, panel fabrication, purchasing or production.

## Reviewed authority

```text
PR                           #47
reviewed head                2d1e58e61b1a04653b17cd666dda2160808079cf
measurement record           WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md
machine audit                INPUT_OUTPUT_JACK_AUDIT.json
exact-part review            INPUT_OUTPUT_JACK_EXACT_PART_REVIEW.md
```

## Evidence reviewed

The corrected record explicitly withdraws the earlier `2.00 mm aluminium + washer + nut` result and applies the current pass statements only to the `1.60 mm nominal panel + Thonk hex nut + no washer` stack.

The project owner directly attested that:

1. the bushing enters the intended panel hole without forcing;
2. the nut starts cleanly without cross-threading;
3. the nut clamps before bottoming;
4. the nut-only stack obtains secure engagement;
5. the jack cannot rotate or wobble after tightening;
6. the housing is not crushed or distorted;
7. tightening does not lift or tilt the soldered jack;
8. tightening does not load or bend the solder terminals;
9. the PCB remains flat;
10. the panel and jack align without lateral force;
11. the 3.00 mm barrel-relief hole clears the physical jack;
12. all three electrical terminal holes remain unobstructed.

The supplier drawing shows a nominal `4.50 mm` threaded bushing. Against the nominal `1.60 mm` panel and no washer, the record derives `2.90 mm` available thread before nut engagement. The direct secure-fit attestation is accepted as stronger evidence than the nominal calculation alone.

## Independent findings

### F01 — corrected stack identity

```text
PASS
```

The current record is unambiguous about the selected nut-only stack. The superseded washer stack is visibly withdrawn and cannot be mistaken for current evidence.

### F02 — qualitative retention and stress behaviour

```text
PASS
```

The attested checks cover the required functional risks: inadequate engagement, nut bottoming, rotation, wobble, housing distortion, jack lift, terminal loading, PCB bow and forced alignment.

### F03 — PCB footprint mechanical clearance

```text
PASS
```

The record directly attests that the physical jack clears the 3.00 mm NPTH barrel relief and that all electrical terminal holes remain unobstructed. This is sufficient for the later bounded footprint-assignment gate.

### F04 — evidence limitations

```text
ACCEPTED WITH EXPLICIT TRANSFER
```

No calibrated calliper readings, repository-controlled photographs or exact assembled seating measurement were supplied. Final panel material, supplier, finished thickness and finished panel-hole diameter remain unlocked.

These limitations do not invalidate the qualitative fit result or the validated pad geometry. They do prevent release of irreversible mechanical geometry and fabrication authority.

## Decision

```text
CORRECTED 1.60 MM NUT-ONLY PHYSICAL FIT     APPROVED
FOOTPRINT ASSIGNMENT GATE                    AUTHORISED AS NEXT BOUNDED GATE
J40 / J70 FOOTPRINTS                         NOT ASSIGNED BY THIS REVIEW
PCB PLACEMENT / ROUTING                      BLOCKED
STANDOFF / PANEL GEOMETRY                    BLOCKED
PANEL FABRICATION                            BLOCKED
PURCHASING                                   BLOCKED
PR #47 MERGE                                 NOT REVIEWED
```

The corrected qualitative physical-fit record is approved for the narrow purpose of allowing a later bounded patch to assign the already validated project-local footprint to J40 and J70.

## Deferred mechanical-release gate

Before PCB placement, standoff selection, panel fabrication or purchasing, a later controlled record must lock or measure:

1. final panel material and supplier;
2. actual finished panel thickness or controlled supplier tolerance;
3. actual assembled PCB-to-panel seating distance;
4. finished panel-hole diameter and manufacturing tolerance;
5. any resulting axis-offset or clearance correction.

Nut thickness, thread pitch and photographs remain optional unless the final physical stack no longer reproduces the accepted fit.

## Stop boundary

This review records approval only. It deliberately leaves:

```text
J40 footprint field                    BLANK
J70 footprint field                    BLANK
project symbol default footprint       BLANK
PCB placement and routing              BLOCKED
panel fabrication                      BLOCKED
purchasing                             BLOCKED
```

The next bounded gate is footprint assignment to J40 and J70, followed by regeneration and KiCad validation. No such work is performed in this review.