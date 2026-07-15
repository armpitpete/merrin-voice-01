# WQP518MA Panel-Stack Measurement Record

## Status

```text
STACK DEFINITION                         CORRECTED
PANEL NOMINAL THICKNESS                  1.60 MM
PANEL MATERIAL / SUPPLIER                PROVISIONAL — FR-4 / JLCPCB NOT LOCKED
MOUNTING HARDWARE                        THONK HEX NUT ONLY
WASHER                                   NONE
CORRECT NUT-ONLY PHYSICAL FIT            USER-ATTESTED PASS
EXACT PCB-TO-PANEL SAMPLE READING        NOT RECORDED
INDEPENDENT REVIEW                       REQUIRED BEFORE FOOTPRINT ASSIGNMENT
J40 / J70 FOOTPRINT ASSIGNMENT           BLOCKED
PCB / PANEL FABRICATION / PURCHASING     BLOCKED
```

The project owner corrected the intended mechanical stack and then reported that all required physical checks passed on 15 July 2026:

- the panel is nominally `1.60 mm`;
- the likely construction is an FR-4 PCB panel, but JLCPCB and the final material remain provisional;
- the jack is retained by the selected Thonk hex nut only;
- no washer is used.

The earlier qualitative pass record described a `2.00 mm aluminium panel + washer + nut` stack. That was the wrong assembly and remains withdrawn. The pass results below apply only to the corrected `1.60 mm panel + nut + no washer` stack.

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

This is `0.40 mm` more available thread than the superseded 2.00 mm panel assumption, and no washer thickness is deducted. The physical fit result below, rather than the calculation alone, is the basis for the qualitative stack pass.

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

## PCB-to-panel seating

```text
supplier nominal                         8.30 mm
physical alignment                       PASS
exact corrected-stack sample reading     NOT RECORDED
```

The `8.30 mm` value remains a supplier nominal. It is not represented as an actual assembled measurement.

The physical fit is sufficient to return this record for independent review, but the actual PCB-to-panel seating distance must be recorded before PCB placement, standoff selection or panel geometry becomes irreversible.

## Measurements retained for later mechanical release

| Measurement | Status |
|---|---|
| actual finished panel thickness | required after panel construction and supplier are locked |
| actual PCB-to-panel seating distance | required before irreversible PCB/panel geometry |
| finished panel-hole diameter | required before fabrication release |
| nut thickness or engaged depth | deferred unless independent review requires it |
| thread pitch | deferred unless independent review requires it |

## Evidence limitations

- No calibrated calliper readings were supplied.
- No exact assembled PCB-to-panel distance was supplied.
- No repository-controlled photographs were supplied.
- Panel construction and supplier remain provisional.
- The fit results are direct project-owner attestations.

## Acceptance boundary

This record is complete as a **user-attested corrected-stack physical-fit record**. It is now ready for independent review. It is not itself independent approval and does not authorise footprint assignment.

The reviewer must explicitly:

1. approve the corrected nut-only qualitative fit evidence and transfer the named dimensional checks to the later mechanical-release gate;
2. require named measurements or photographs; or
3. return the record for revision.

Until independent review is recorded:

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