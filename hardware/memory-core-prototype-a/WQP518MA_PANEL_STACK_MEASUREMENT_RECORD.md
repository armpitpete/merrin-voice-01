# WQP518MA Panel-Stack Measurement Record

## Status

```text
STACK DEFINITION                         CORRECTED
PANEL NOMINAL THICKNESS                  1.60 MM
PANEL MATERIAL / SUPPLIER                PROVISIONAL — FR-4 / JLCPCB NOT LOCKED
MOUNTING HARDWARE                        THONK HEX NUT ONLY
WASHER                                   NONE
CORRECT NUT-ONLY PHYSICAL FIT            USER-ATTESTED PASS
INDEPENDENT REVIEW                       APPROVED FOR FOOTPRINT-ASSIGNMENT GATE
EXACT PCB-TO-PANEL SAMPLE READING        NOT RECORDED
J40 / J70 FOOTPRINT ASSIGNMENT           NOT YET PERFORMED
PCB / PANEL FABRICATION / PURCHASING     BLOCKED
```

The project owner corrected the intended mechanical stack and reported that all required physical checks passed on 15 July 2026:

- the panel is nominally `1.60 mm`;
- the likely construction is an FR-4 PCB panel, but JLCPCB and the final material remain provisional;
- the jack is retained by the selected Thonk hex nut only;
- no washer is used.

The earlier qualitative pass record described a `2.00 mm aluminium panel + washer + nut` stack. That was the wrong assembly and remains withdrawn. The pass results below apply only to the corrected `1.60 mm panel + nut + no washer` stack.

Independent review is recorded in `WQP518MA_PANEL_STACK_INDEPENDENT_REVIEW.md`. That review approves the qualitative fit for the next bounded footprint-assignment gate only. It does not authorise PCB placement, panel fabrication, purchasing or production.

## Controlled stack

```text
jack                         Thonkiconn WQP518MA mono switched jack
nut                          Thonkiconn Hex Nut variant
washer                       none
panel material               provisional FR-4 PCB panel; supplier not locked
panel nominal thickness      1.60 mm
panel hole target            6.50 +0.10 / -0.00 mm
panel-hole concentricity      total assembled offset <= 0.15 mm
PCB barrel relief            3.00 mm NPTH at jack barrel centre
mounting condition           jack terminals soldered to PCB
```

The panel material and supplier must be locked before panel fabrication. The `1.60 mm` value is the current nominal design thickness, not a recorded finished-panel measurement.

## Supplier-drawing nominal dimensions

| Feature | Nominal value | Evidence status |
|---|---:|---|
| bushing diameter | 6.00 mm | supplier drawing |
| threaded bushing length | 4.50 mm | supplier drawing |
| front bushing projection | 5.50 mm | supplier drawing |
| PCB-to-panel seating height | 8.30 mm | supplier drawing; sample value not recorded |
| mono jack body width | 9.00 mm | supplier comparison image |

## Nut-only thread calculation

```text
threaded bushing length       4.50 mm
minus nominal panel           1.60 mm
minus washer                  0.00 mm
available for nut engagement  2.90 mm nominal
```

The direct secure-fit attestation, rather than the nominal calculation alone, is the accepted basis for the qualitative stack pass.

## Corrected physical-fit results

| Required check | Result | Evidence basis |
|---|---|---|
| bushing passes through the intended panel hole without forcing | PASS | project-owner direct attestation |
| nut starts cleanly without cross-threading | PASS | project-owner direct attestation |
| nut clamps the nominal 1.60 mm panel before bottoming | PASS | project-owner direct attestation |
| nut-only stack obtains secure engagement | PASS | project-owner direct attestation |
| jack cannot rotate or wobble after tightening | PASS | project-owner direct attestation |
| housing is not crushed or distorted | PASS | project-owner direct attestation |
| tightening does not lift or tilt the soldered jack | PASS | project-owner direct attestation |
| tightening does not load or bend solder terminals | PASS | project-owner direct attestation |
| PCB remains flat | PASS | project-owner direct attestation |
| panel and jack align without lateral force | PASS | project-owner direct attestation |
| 3.00 mm barrel-relief hole clears the physical jack | PASS | project-owner direct attestation |
| all three electrical terminal holes remain unobstructed | PASS | project-owner direct attestation |

## Independent-review outcome

```text
corrected stack identity                 PASS
qualitative retention and stress checks  PASS
3.00 mm barrel-relief clearance          PASS
terminal-hole clearance                  PASS
evidence limitations                     ACCEPTED WITH EXPLICIT TRANSFER
```

Decision:

```text
corrected physical fit                   APPROVED
next bounded footprint-assignment gate   AUTHORISED
footprint assignment in this record      NOT PERFORMED
```

## PCB-to-panel seating

```text
supplier nominal                         8.30 mm
physical alignment                       PASS
exact corrected-stack sample reading     NOT RECORDED
```

The `8.30 mm` value remains a supplier nominal. It is not represented as an actual assembled measurement.

The exact PCB-to-panel seating distance must be recorded before PCB placement, standoff selection or panel geometry becomes irreversible.

## Deferred mechanical-release evidence

| Measurement or decision | Status |
|---|---|
| final panel material and supplier | required before fabrication release |
| actual finished panel thickness or controlled supplier tolerance | required before fabrication release |
| actual PCB-to-panel seating distance | required before irreversible PCB/panel geometry |
| finished panel-hole diameter and tolerance | required before fabrication release |
| nut thickness or engaged depth | deferred unless the accepted fit cannot be reproduced |
| thread pitch | deferred unless the accepted fit cannot be reproduced |
| repository-controlled photographs | optional unless later review requires them |

## Acceptance boundary

This record is approved for the narrow purpose of allowing the already validated project-local footprint to be assigned to J40 and J70 in a later bounded patch.

This review does not itself assign the footprint. Until the next bounded gate is deliberately applied:

```text
J40 footprint field                    BLANK
J70 footprint field                    BLANK
project symbol default footprint       BLANK
PCB placement and routing              BLOCKED
panel fabrication                      BLOCKED
purchasing                             BLOCKED
```

## Superseded record state

```text
2.00 mm aluminium panel + washer + nut
status: WITHDRAWN — WRONG STACK
```

PCB placement, routing, panel fabrication and purchasing remain blocked.

## Post-review footprint assignment

```text
J40 footprint field                    ASSIGNED
J70 footprint field                    ASSIGNED
project symbol default footprint       BLANK
assignment commit                      f34eea95c216cd31df4d4e3f1498adc4b9014ec9
PCB placement, routing, panel fabrication and purchasing remain blocked
```
