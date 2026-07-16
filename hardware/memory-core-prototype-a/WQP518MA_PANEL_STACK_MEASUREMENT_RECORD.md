# WQP518MA Panel-Stack Measurement Record

## Current status

```text
STACK DEFINITION                         CORRECTED
PANEL NOMINAL THICKNESS                  1.60 MM
PANEL MATERIAL / SUPPLIER                PROVISIONAL — FR-4 / JLCPCB NOT LOCKED
MOUNTING HARDWARE                        THONK HEX NUT ONLY
WASHER                                   NONE
CORRECT NUT-ONLY PHYSICAL FIT            USER-ATTESTED PASS
INDEPENDENT REVIEW                       PASS
EXACT PCB-TO-PANEL SAMPLE READING        NOT RECORDED
J40 FOOTPRINT FIELD                      ASSIGNED
J70 FOOTPRINT FIELD                      ASSIGNED
PROJECT SYMBOL DEFAULT                   BLANK
PR #47                                   APPROVED AND MERGED
MAIN SQUASH COMMIT                       dd306209e9874dd6e9064c33973d99ecf9282690
PCB / PANEL FABRICATION / PURCHASING     BLOCKED
```

The project owner corrected the intended mechanical stack and reported that all required physical checks passed on 15 July 2026:

- panel nominal thickness `1.60 mm`;
- likely FR-4 PCB-panel construction, with final material and supplier still provisional;
- selected Thonk hex nut only;
- no washer.

The earlier qualitative pass described a `2.00 mm aluminium panel + washer + nut` stack. That was the wrong assembly and is withdrawn. The pass results below apply only to the corrected `1.60 mm panel + nut + no washer` stack.

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

The panel material and supplier must be locked before panel fabrication. The `1.60 mm` value is a nominal design thickness, not a recorded finished-panel measurement.

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
corrected physical fit                   APPROVED
```

The independent review authorised the later footprint-assignment gate. That assignment was performed, validated, approved and merged through PR #47.

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

## Current assignment and merge boundary

```text
J40 footprint field                    ASSIGNED
J70 footprint field                    ASSIGNED
project symbol default footprint       BLANK
assignment commit                      f34eea95c216cd31df4d4e3f1498adc4b9014ec9
reviewed PR head                       ebaf7fbc50f5c07443d329519de0a38622f231b1
main squash commit                     dd306209e9874dd6e9064c33973d99ecf9282690
post-assignment validation             PASS
PCB creation / placement / routing     BLOCKED
panel CAD / fabrication                BLOCKED
purchasing / production                BLOCKED
SSI2164 lane                           NOT STARTED
```

## Superseded history

### Wrong physical stack

```text
2.00 mm aluminium panel + washer + nut
status: WITHDRAWN — WRONG STACK
```

### Pre-assignment review point

At the independent-review head, J40 and J70 were deliberately blank because that review only authorised a later assignment patch. That historical blank state was superseded by assignment commit `f34eea95c216cd31df4d4e3f1498adc4b9014ec9`.

### Pre-merge review point

PR #47 was reviewed at exact head `ebaf7fbc50f5c07443d329519de0a38622f231b1` while open and unmerged. That historical state was superseded by squash commit `dd306209e9874dd6e9064c33973d99ecf9282690`.

PCB creation, placement, routing, panel CAD, fabrication, purchasing and production remain blocked.
