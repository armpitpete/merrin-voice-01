# WQP518MA Panel-Stack Measurement Record

## Status

```text
PHYSICAL SAMPLE: NOT PRESENTED
MEASUREMENTS: PENDING HUMAN INPUT
PANEL / PCB FABRICATION AUTHORITY: BLOCKED
PURCHASING AUTHORITY: BLOCKED
```

This record is the required closure evidence for the mechanical part of Gate-B lane 02. The controlled Thonk supplier page proves that WQP518MA and PJ398SM are interchangeable and use the same footprint, but it does not publish the nut, washer and thread-stack dimensions needed to approve the panel assembly.

## Controlled design choices awaiting fit proof

```text
jack                         Thonkiconn WQP518MA
nut                          Thonkiconn Hex Nut variant
washer                       Thonkiconn Washer variant
panel material               aluminium
panel thickness target       2.00 mm
panel hole target            6.50 +0.10 / -0.00 mm
panel-hole concentricity      total assembled offset <= 0.15 mm
PCB barrel relief            3.00 mm NPTH at jack barrel centre
```

The panel-hole target is a derived engineering value, not fabrication authority. It uses the supplier drawing's 6.00 mm bushing and general ±0.15 mm tolerance, leaving at least 0.175 mm radial clearance at a 6.50 mm minimum hole before positional error.

## Required sample measurements

Measure one actual WQP518MA jack, one selected Thonk hex nut and one selected Thonk washer using calibrated callipers or a thread gauge.

| Measurement | Required value | Result |
|---|---:|---|
| bushing major diameter | mm | PENDING |
| bushing thread pitch | mm | PENDING |
| usable threaded length above housing | mm | PENDING |
| hex nut across flats | mm | PENDING |
| hex nut thickness | mm | PENDING |
| washer outside diameter | mm | PENDING |
| washer inside diameter | mm | PENDING |
| washer thickness | mm | PENDING |
| jack body height from PCB seating plane to panel seating plane | mm | PENDING |
| terminal shoulder-to-PCB seating behaviour | description | PENDING |
| 2.00 mm panel + washer + nut obtains full secure engagement | pass/fail | PENDING |
| panel rear face can seat without stressing solder joints | pass/fail | PENDING |

## Required fit checks

1. Insert the bushing through a `6.50 mm` gauge hole in a `2.00 mm` test coupon.
2. Install the selected washer and hex nut.
3. Confirm secure thread engagement without bottoming the nut or crushing the housing.
4. Confirm the panel can seat at the measured PCB-to-panel distance without lifting the jack from the PCB.
5. Confirm the 3 mm barrel-relief hole clears the barrel and leaves all three terminal holes unobstructed.
6. Record photographs of the assembled stack and the calliper readings.

## Acceptance rule

J40 and J70 may receive the project-local footprint only after this record is completed and independently reviewed. A verbal estimate, product photograph or generic M6/M7 hardware assumption is not sufficient.

PCB placement, routing, panel fabrication and purchasing remain blocked.
