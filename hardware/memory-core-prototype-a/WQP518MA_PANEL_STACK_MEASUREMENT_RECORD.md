# WQP518MA Panel-Stack Measurement Record

## Status

```text
PHYSICAL FIT CHECKS: USER-ATTESTED PASS
NUMERIC CALIPER MEASUREMENTS: DEFERRED BY PROJECT OWNER
INDEPENDENT REVIEW: REQUIRED BEFORE FOOTPRINT ASSIGNMENT
J40 / J70 FOOTPRINT ASSIGNMENT: BLOCKED
PANEL / PCB FABRICATION AUTHORITY: BLOCKED
PURCHASING AUTHORITY: BLOCKED
```

This record captures the project owner's physical-fit attestation for Gate-B lane 02. On 15 July 2026, after reviewing the WQP518MA/PJ398SM supplier geometry, the selected Thonk hex nut and washer, the 2.00 mm aluminium panel stack, the soldered PCB mounting condition and the 3.00 mm barrel relief, the project owner reported that all required fit checks passed.

No unreported calliper value has been invented. Exact thread, nut, washer and sample seating measurements remain deferred. The supplier-drawing nominal values remain design references rather than measured sample values.

## Controlled assembly

```text
jack                         Thonkiconn WQP518MA mono switched jack
nut                          Thonkiconn Hex Nut variant
washer                       Thonkiconn Washer variant
panel material               aluminium
panel thickness              2.00 mm
panel hole target            6.50 +0.10 / -0.00 mm
panel-hole concentricity      total assembled offset <= 0.15 mm
PCB barrel relief            3.00 mm NPTH at jack barrel centre
mounting condition            jack terminals soldered to PCB
```

The panel-hole target is a derived engineering value, not fabrication authority. It uses the supplier drawing's 6.00 mm bushing and general ±0.15 mm tolerance, leaving at least 0.175 mm radial clearance at a 6.50 mm minimum hole before positional error.

## Supplier-drawing nominal dimensions

| Feature | Nominal value | Evidence status |
|---|---:|---|
| bushing diameter | 6.00 mm | supplier drawing |
| threaded bushing length | 4.50 mm | supplier drawing |
| front bushing projection | 5.50 mm | supplier drawing |
| PCB-to-panel seating height | 8.30 mm | supplier drawing; sample value not numerically recorded |
| mono jack body width | 9.00 mm | supplier comparison image |
| selected nut/washer front envelope | approximately 7.50 mm | supplier hardware image |

The 4.50 mm threaded length leaves 2.50 mm above the 2.00 mm panel for the selected washer and nut engagement. Physical fit, rather than an inferred hardware calculation, is the accepted basis for the qualitative checks below.

## Physical-fit results

| Required check | Result | Evidence basis |
|---|---|---|
| bushing passes through the 6.50 mm panel hole without forcing | PASS | project-owner physical attestation |
| washer sits flat on the panel | PASS | project-owner physical attestation |
| nut starts cleanly and does not cross-thread | PASS | project-owner physical attestation |
| 2.00 mm panel + washer + nut obtains full secure engagement | PASS | project-owner physical attestation |
| nut clamps before bottoming | PASS | project-owner physical attestation |
| housing is not crushed or distorted | PASS | project-owner physical attestation |
| jack remains secure and cannot rotate or wobble after tightening | PASS | project-owner physical attestation |
| panel tightening does not lift or tilt the soldered jack | PASS | project-owner physical attestation |
| panel tightening does not bend or mechanically load the solder terminals | PASS | project-owner physical attestation |
| PCB remains flat during tightening | PASS | project-owner physical attestation |
| panel and jack align naturally without lateral forcing | PASS | project-owner physical attestation |
| 3.00 mm barrel-relief hole clears the physical jack | PASS | project-owner physical attestation |
| all three electrical terminal holes remain unobstructed | PASS | project-owner physical attestation |

## PCB-to-panel seating

```text
supplier nominal                         8.30 mm
physical alignment at assembled stack    PASS
exact sample calliper reading             NOT RECORDED — DEFERRED
```

The user confirmed that the assembled PCB, jack and panel fit passes. The exact physical PCB-top-to-panel-rear distance was not supplied. Therefore this record does not mislabel `8.30 mm` as a measured sample value.

Any later panel, standoff or PCB-placement work must either:

1. use `8.30 mm` explicitly as a provisional supplier nominal and preserve adjustment capacity; or
2. record the actual assembled distance before dimensions become irreversible.

Neither route is authorised by this record. PCB placement, routing and panel fabrication remain blocked.

## Deferred numerical measurements

The following values were deliberately not recorded:

| Measurement | Status |
|---|---|
| bushing major diameter | deferred; supplier nominal 6.00 mm retained |
| bushing thread pitch | deferred |
| usable threaded length above housing | deferred; supplier nominal 4.50 mm retained |
| hex nut across flats | deferred |
| hex nut thickness | deferred |
| washer outside diameter | deferred |
| washer inside diameter | deferred |
| washer thickness | deferred |
| actual PCB-to-panel seating distance | deferred; supplier nominal 8.30 mm retained |

These omissions must remain visible during independent review. They must not be silently converted into measured values.

## Assembly interpretation

The jack is soldered to the PCB. The relevant proof is therefore not whether the terminals are soldered, but whether panel tightening changes the jack or PCB position after soldering. The project owner's pass statement confirms:

```text
jack body remains seated after tightening     PASS
jack does not rise or tilt                     PASS
PCB does not bow                               PASS
solder terminals do not carry panel load       PASS
```

## Evidence limitations

- No calibrated calliper readings were supplied.
- No thread-gauge reading was supplied.
- No repository-controlled photographs were supplied.
- The fit results are direct project-owner attestations.
- The supplier drawing and images support nominal geometry and part identification, not the unrecorded sample dimensions.

## Acceptance boundary

This record is complete as a **user-attested qualitative physical-fit record with numerical measurements deferred**. It is not an independent approval and does not itself authorise footprint assignment.

The next bounded gate is independent review of this record. The reviewer must either:

- accept the qualitative fit evidence and explicitly transfer deferred numerical dimensions to a later controlled mechanical gate;
- require one or more named measurements or photographs; or
- reject the record and return it for physical re-check.

Until that review is recorded:

```text
J40 footprint field                    BLANK
J70 footprint field                    BLANK
project symbol default footprint       BLANK
PCB placement and routing              BLOCKED
panel fabrication                       BLOCKED
purchasing                              BLOCKED
```

## Prior record state

For traceability, the superseded state before the 15 July 2026 project-owner attestation was:

```text
PHYSICAL SAMPLE: NOT PRESENTED
MEASUREMENTS: PENDING HUMAN INPUT
```

PCB placement, routing, panel fabrication and purchasing remain blocked.