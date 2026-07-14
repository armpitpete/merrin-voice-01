# Output Mute and Fault-Control Exact-Part Review

## Decision after schematic correction

```text
OUTPUT-MUTE / FAULT-CONTROL EXACT-PART GATE: PASS FOR Q70 / Q71 / U70
Q70 EXACT PART / PIN MAP / PACKAGE: ACCEPTED
Q71 EXACT PART / PIN MAP / PACKAGE: ACCEPTED
U70 EXACT PART / CTR BIN / PACKAGE: ACCEPTED
POSITIVE-RAIL-LOSS FAIL-MUTE TOPOLOGY: ACCEPTED AT CALCULATED SCHEMATIC LEVEL
CALCULATED STATIC MUTE TARGET: >60 dB
MEASURED MUTE DEPTH / POP / RAIL-SEQUENCING: TRANSFERRED TO GATE C
PCB PLACEMENT / ROUTING / FABRICATION / PURCHASING: BLOCKED
```

This review closes the first Gate-B exact-part lane. It accepts three exact active parts, their physical pin maps and their package-to-footprint mappings. It does not accept measured behaviour or physical PCB implementation.

## Corrected topology

The provisional fault-powered clamp was replaced by a powered healthy-release path:

```text
RAIL_3V3 -- R10 10k -- HARDWARE_FAULT_N -- R711 10k -- Q71 gate
                                                |
                                             R712 100k
                                                |
                                               GND

RAIL_P12 -- R713 820R -- MUTE_LED_SUPPLY -- R714 1k -- U70 LED anode
U70 LED cathode -- MUTE_LED_K -- Q71 drain
Q71 source ---------------------------------------------- GND

RAIL_N12 -- R715 10k -- RELEASE_SINK -- U70 emitter
U70 collector ----------------------------- MUTE_GATE
                                              |
                                      R716 100k to GND
                                      C710 100nF to GND
                                              |
                                      Q70 physical gate

OUT_PREMUTE -- R703 120k -- MUTE_NODE -- Q70 drain
                                      Q70 source -- GND
```

Healthy `HARDWARE_FAULT_N` turns Q71 and U70 on, connecting the negative release path. A fault, undefined fault signal or loss of `RAIL_P12` removes the release drive, allowing `R716` to return `MUTE_GATE` toward ground and turn the shunt JFET on.

## Q70 — output mute JFET

```text
Manufacturer: onsemi
Exact part:   MMBFJ113
Package:      SOT-23 / TO-236
Datasheet:    https://www.onsemi.com/pdf/datasheet/mmbfj113-d.pdf
KiCad:        Package_TO_SOT_SMD:SOT-23
```

Physical pin contract:

```text
pin 1 drain  -> MUTE_NODE
pin 2 source -> GND
pin 3 gate   -> MUTE_GATE
```

Guaranteed limits used by this gate:

```text
J113 VGS(off): -0.5 V to -3.0 V
rDS(on):       100 ohm maximum at VGS = 0 V
```

### Minimum mute-depth requirement

```text
calculated worst-case static attenuation: greater than 60 dB
measured Gate-C output attenuation:       at least 60 dB
```

With `R703 = 120 kOhm ±1%` and maximum `100 ohm` JFET on-resistance:

```text
R703 minimum = 118.8 kOhm
ratio        = 100 / (118800 + 100)
attenuation  = 61.50 dB
```

This is a static bound. Signal dependence, leakage, distortion, op-amp behaviour, parasitic coupling and audible pop energy remain measured Gate-C tests.

### Q70 decision

```text
EXACT PART: ACCEPTED
PHYSICAL PIN MAP: ACCEPTED
SOT-23 FOOTPRINT MAPPING: ACCEPTED
CALCULATED STATIC TARGET: PASS — 61.50 dB
MEASURED MUTE CLAIM: NOT YET ACCEPTED
```

## Q71 — healthy-release driver

The under-proven provisional NPN was replaced rather than forced into acceptance.

```text
Manufacturer: Nexperia
Exact part:   PMV20XNE
Function:     30 V N-channel MOSFET
Package:      SOT-23 / TO-236AB
Datasheet:    https://assets.nexperia.com/documents/data-sheet/PMV20XNE.pdf
KiCad:        Package_TO_SOT_SMD:SOT-23
```

Physical pin contract:

```text
pin 1 gate   -> FAULT_GATE
pin 2 source -> GND
pin 3 drain  -> MUTE_LED_K
```

The manufacturer specifies maximum `RDS(on) = 30 mOhm` at `VGS = 2.5 V`. The realised gate drive includes sheet-01 `R10 = 10 kOhm`, sheet-07 `R711 = 10 kOhm` and `R712 = 100 kOhm` to ground.

Using `3.3 V -5%` and 1% resistor extremes:

```text
VGS minimum estimate = 2.604 V
```

This remains above the manufacturer’s 2.5 V guaranteed resistance test point. The BJT saturation problem is removed; the fault net now drives a high-impedance MOSFET gate.

### Q71 decision

```text
EXACT PART: ACCEPTED
PHYSICAL PIN MAP: ACCEPTED
2.5 V DRIVE CONTRACT: PASS — 2.604 V conservative estimate
SOT-23 FOOTPRINT MAPPING: ACCEPTED
```

## U70 — isolated healthy-release optocoupler

```text
Manufacturer: Vishay
Exact order:  VO617A-3X007T
CTR class:    group 3
Package:      option-7 SMD-4, 7.62 mm row spacing
Datasheet:    https://www.vishay.com/docs/83430/vo617a.pdf
KiCad:        Package_DIP:SMDIP-4_W7.62mm
```

Physical pin contract:

```text
pin 1 LED anode   -> MUTE_LED_A
pin 2 LED cathode -> MUTE_LED_K
pin 3 emitter     -> RELEASE_SINK
pin 4 collector   -> MUTE_GATE
```

The selected group guarantees:

```text
CTR at IF = 5 mA, VCE = 5 V: 100% minimum, 200% maximum
VCE(sat):                     0.4 V maximum at IF = 5 mA, IC = 1 mA
```

The split LED resistance is `820 ohm + 1.0 kOhm`. Using `RAIL_P12 = 12 V -5%`, both resistors at +1%, and a conservative `1.65 V` LED drop:

```text
minimum estimated LED current = 5.304 mA
minimum guaranteed collector capability at 100% CTR = 5.304 mA
```

The release path needs approximately `1.055 mA` at the start of release through `R715 = 10 kOhm`, and much less at steady state. The selected CTR class therefore provides more than 5:1 current margin against the calculated transient requirement.

### U70 decision

```text
EXACT ORDERING CODE: ACCEPTED
MINIMUM CTR CONDITION: PASS
OPTION-7 SMD-4 PIN MAP: ACCEPTED
SMDIP-4_W7.62mm FOOTPRINT MAPPING: ACCEPTED
```

## Rail-loss and fault timing

Using maximum `0.4 V` optocoupler saturation voltage, `R715 = 10 kOhm` and `R716 = 100 kOhm`:

```text
healthy MUTE_GATE estimate = -10.545 V
worst J113 cutoff magnitude = 3.0 V
healthy off-state margin    = 7.545 V
```

When `HARDWARE_FAULT_N` goes low or `RAIL_P12` disappears, U70 opens. `R716 = 100 kOhm` and `C710 = 100 nF` return the gate toward ground:

```text
t = 100k x 100nF x ln(10.545 / 3.0)
  = 12.57 ms
```

This is below the declared 20 ms schematic target. Loss of `RAIL_N12` also removes the negative release source and therefore tends toward mute rather than release.

Real rail ramps, capacitor tolerance, optocoupler storage, JFET spread and pop energy remain Gate C.

## Footprint verification boundary

| Ref | Exact part | Manufacturer package | KiCad footprint | Decision |
|---|---|---|---|---|
| Q70 | onsemi MMBFJ113 | SOT-23 / TO-236 | `Package_TO_SOT_SMD:SOT-23` | ACCEPTED |
| Q71 | Nexperia PMV20XNE | SOT-23 / TO-236AB | `Package_TO_SOT_SMD:SOT-23` | ACCEPTED |
| U70 | Vishay VO617A-3X007T | option-7 SMD-4 | `Package_DIP:SMDIP-4_W7.62mm` | ACCEPTED |

Acceptance covers pad numbering, package family and nominal package geometry. It does not authorise placement, courtyard interaction, creepage strategy, assembly process, panel mechanics or purchasing.

## Validation required for closure

The amended sheet must pass:

- deterministic amendment idempotence;
- exact symbol and instance pin-map validators;
- exact footprint mapping validation;
- shared `U32` allocation validation;
- hierarchy/no-export validation;
- KiCad 10 hierarchical ERC with zero errors and zero warnings.

## Gate status

```text
Gate A — schematic architecture               REMAINS ACCEPTED
Gate B — Q70/Q71/U70 exact parts/footprints   PASS, SUBJECT TO PR REVIEW
Gate C — measured mute/fault behaviour        NOT STARTED
Gate D — PCB / production                     BLOCKED
```

The next Gate-B lane remains blocked until this correction is reviewed. PCB placement, routing, fabrication and purchasing remain blocked.
