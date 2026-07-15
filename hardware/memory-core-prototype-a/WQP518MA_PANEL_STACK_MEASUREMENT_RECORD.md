# WQP518MA Panel-Stack Measurement Record

## Status

```text
STACK DEFINITION                         CORRECTED
PANEL NOMINAL THICKNESS                  1.60 MM
PANEL MATERIAL / SUPPLIER                PROVISIONAL — FR-4 / JLCPCB NOT LOCKED
MOUNTING HARDWARE                        THONK HEX NUT ONLY
WASHER                                   NONE
PREVIOUS 2 MM + WASHER ATTESTATION       WITHDRAWN — WRONG STACK
CURRENT NUT-ONLY FIT PROOF                PENDING
INDEPENDENT REVIEW                       NOT READY
J40 / J70 FOOTPRINT ASSIGNMENT           BLOCKED
PCB / PANEL FABRICATION / PURCHASING     BLOCKED
```

The project owner corrected the intended mechanical stack on 15 July 2026:

- the panel is nominally `1.60 mm`, not `2.00 mm`;
- the likely construction is an FR-4 PCB panel, but JLCPCB and the final material remain provisional;
- the jack is retained by the selected Thonk hex nut only;
- no washer is used.

The earlier qualitative pass record described a `2.00 mm aluminium panel + washer + nut` stack. That is not the intended assembly and cannot be transferred to the corrected stack. It is therefore withdrawn rather than reinterpreted.

## Current controlled stack

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

The panel material and supplier must be locked before panel fabrication. The `1.60 mm` value is the current nominal design thickness, not a measured finished-panel value.

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

This is `0.40 mm` more available thread than the superseded 2.00 mm panel assumption, and no washer thickness is deducted. It improves the expected engagement but does not by itself prove secure clamping, because the nut depth and final panel thickness remain unrecorded.

## Required physical checks for the corrected stack

Use the actual WQP518MA, selected Thonk hex nut and a representative `1.60 mm` panel or coupon. Do not add a washer.

| Required check | Current result |
|---|---|
| bushing passes through the intended panel hole without forcing | PENDING |
| nut starts cleanly without cross-threading | PENDING |
| nut clamps the 1.60 mm panel before bottoming | PENDING |
| nut-only stack obtains secure engagement | PENDING |
| jack cannot rotate or wobble after tightening | PENDING |
| housing is not crushed or distorted | PENDING |
| tightening does not lift or tilt the soldered jack | PENDING |
| tightening does not load or bend solder terminals | PENDING |
| PCB remains flat | PENDING |
| panel and jack align without lateral force | PENDING |
| 3.00 mm barrel-relief hole clears the physical jack | PENDING PHYSICAL CONFIRMATION |
| all three electrical terminal holes remain unobstructed | PENDING PHYSICAL CONFIRMATION |

## PCB-to-panel seating

```text
supplier nominal                         8.30 mm
exact corrected-stack sample reading     NOT RECORDED
status                                   PENDING
```

The `8.30 mm` value remains a supplier nominal. It must not be presented as a measured assembled value.

## Measurements still useful

Only measurements that affect irreversible mechanical geometry need to be retained:

| Measurement | Status |
|---|---|
| actual finished panel thickness | pending after panel construction is locked |
| nut thickness or engaged depth | pending if secure fit cannot be judged directly |
| actual PCB-to-panel seating distance | pending before PCB/panel geometry becomes irreversible |
| panel-hole finished diameter | pending before fabrication release |

Thread pitch and other dimensions may remain deferred if the actual nut-only stack is physically proven and independently accepted.

## Acceptance boundary

This record is **not ready for independent approval**. The corrected nut-only `1.60 mm` stack needs a direct fit result first.

Until that result and its independent review are recorded:

```text
J40 footprint field                    BLANK
J70 footprint field                    BLANK
project symbol default footprint       BLANK
PCB placement and routing              BLOCKED
panel fabrication                      BLOCKED
purchasing                             BLOCKED
```

## Superseded record text retained for validator traceability

The following phrases describe the rejected earlier state and are not current evidence:

```text
PHYSICAL SAMPLE: NOT PRESENTED
MEASUREMENTS: PENDING HUMAN INPUT
2.00 mm panel + washer + nut obtains full secure engagement — SUPERSEDED / WITHDRAWN
```

PCB placement, routing, panel fabrication and purchasing remain blocked.