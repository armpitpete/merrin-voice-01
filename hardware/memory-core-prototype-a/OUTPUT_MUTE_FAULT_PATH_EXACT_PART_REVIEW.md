# Output Mute and Fault-Control Exact-Part Review

## Decision after evidence repair

```text
Q70 / Q71 / U70 CANDIDATE DEVICES: RETAIN
PHYSICAL PIN MAPS: PASS
POWERED HEALTHY-RELEASE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
U70 ACTUAL-BIAS SATURATION PROOF: PASS
Q70 25 C DATASHEET-BOUND MUTE CALCULATION: PASS — 61.50 dB
DIMENSIONAL FOOTPRINT AUDIT: PENDING CURRENT PR RERUN
MEASURED BEHAVIOUR: GATE C
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
PR ACCEPTANCE: PENDING NEW REVIEW
```

The former non-saturated CTR argument and name-only footprint check are withdrawn.

## Corrected topology

```text
RAIL_3V3 -- R10 10k -- HARDWARE_FAULT_N -- R711 10k -- Q71 gate
                                                |
                                             R712 100k
                                                |
                                               GND

RAIL_P12 -- R713 820R -- R714 1k -- U70 LED -- Q71 drain
Q71 source ------------------------------------------------ GND

RAIL_N12 -- R715 10k -- U70 emitter
U70 collector ------------------ MUTE_GATE
                                  |
                         R716 100k to GND
                         C710 100nF to GND
                                  |
                         Q70 physical gate
```

Healthy operation powers the isolated negative release. Fault, undefined fault state or loss of `RAIL_P12` removes that release and lets `R716` return the gate toward mute.

## Exact parts and pins

| Ref | Exact part | Package | Pin contract |
|---|---|---|---|
| Q70 | onsemi MMBFJ113 | SOT-23 / TO-236, case 318-08 | 1 D, 2 S, 3 G |
| Q71 | Nexperia PMV20XNE | TO-236AB / SOT23 | 1 G, 2 S, 3 D |
| U70 | Vishay VO617A-3X007T | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C |

## U70 actual-bias proof

Vishay specifies `VCE(sat) <= 0.4 V` at `IF = 5 mA` and `IC = 1 mA`.

The conservative LED calculation remains:

```text
RAIL_P12 = 11.4 V
VF = 1.65 V
R713 + R714 at +1% = 1.8382 kOhm
IF minimum estimate = 5.304 mA
```

The actual release-path load line at the guaranteed saturation voltage is:

```text
RAIL_N12 magnitude at +5% = 12.6 V
R715 + R716 at -1% = 108.9 kOhm
VCE = 0.4 V
required collector current = (12.6 - 0.4) / 108.9k
                           = 0.112 mA
```

The guaranteed saturated test current is `1.0 mA`, giving `8.93:1` margin over the actual worst calculated load. This replaces the invalid use of the `VCE = 5 V` CTR guarantee.

## Q70 mute-depth boundary

The calculation is now explicitly limited to the datasheet condition:

```text
TJ = 25 C
VGS = 0 V
VDS <= 0.1 V
MMBFJ113 rDS(on) maximum = 100 ohm
R703 minimum = 118.8 kOhm
calculated static attenuation = 61.50 dB
```

It is not described as a full-temperature or production worst case. Gate C must prove at least `60 dB` on assembled hardware over the declared operating range and device spread.

## Dimensional footprint audit

The assigned footprint names remain:

```text
Q70 / Q71: Package_TO_SOT_SMD:SOT-23
U70:       Package_DIP:SMDIP-4_W7.62mm
```

Acceptance now requires geometry extracted from the pinned KiCad `10.0.4` image.

The audit checks:

- SOT-23 pin-1/2 pitch, opposite-side pin-3 orientation, pad size and courtyard;
- option-7 SMD-4 `7.62 mm` row spacing, `2.54 mm` pitch, pin-1 orientation, pad size and courtyard;
- manufacturer body and lead-span maxima;
- positive courtyard containment.

This audit does not authorise placement, courtyard interaction with neighbouring parts, assembly process, creepage strategy or purchasing.

## Remaining measured gates

Gate C retains:

- mute depth across temperature and part spread;
- audible pop and transient energy;
- real rail ramp and sequencing behaviour;
- load drive and output impedance;
- sustained fault and endurance testing.

## Closure condition

PR #46 returns for approval only after the current committed head passes:

- actual-bias saturation validation;
- dimensional footprint validation from pinned KiCad files;
- exact pin and hierarchy validation;
- KiCad ERC at zero errors and zero warnings;
- a no-diff committed-file rerun.
