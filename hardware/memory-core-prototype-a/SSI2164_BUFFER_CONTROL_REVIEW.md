# SSI2164 buffered-control review

## Decision

```text
CONTROL-PORT LOADING DEFECT       CORRECTED
BUFFER                            OPA4196 PW / TSSOP-14 TARGET
SHARED REFERENCE                  U63
UNITS 1/2/4                       SHEET 05
UNITS 3/5                         SHEET 06
NOMINAL 3.3 V ATTENUATION         99.8 dB
LOW RAIL / 9 kΩ CALCULATION       98.1 dB
SSI2164 PACKAGE                   PSL16 / JEDEC MS-012-AC
SSI2164 FOOTPRINT                 BLANK
OPA4196 FOOTPRINT                 BLANK
PCB / PANEL / PURCHASING          BLOCKED
```

## Primary-source basis

The SSI2164 manufacturer specifies a nominal 10 kΩ control-port impedance with a 9–11 kΩ range, a -33 mV/dB control constant and 3.3 V for approximately -100 dB attenuation. The SSI2164 orderable package is `SSI2164S-TU` or `SSI2164S-RT`, package ID `PSL16`, compliant with JEDEC MS-012-AC.

Texas Instruments specifies the OPA4196 for 4.5–36 V operation, rail-to-rail input/output, 140 µA typical quiescent current per channel, unity-gain capacitive-load operation and PW TSSOP-14 availability. TI recommends 0.1 µF local supply bypass and 10–20 Ω output isolation for capacitive loads.

## Remaining gates

- exact SSI2164 and OPA4196 land-pattern review;
- exact post-buffer clamp-diode selection;
- regulator-reference tolerance in the complete attenuation bound;
- bench measurement of unity, attenuation, startup and fault behaviour.
