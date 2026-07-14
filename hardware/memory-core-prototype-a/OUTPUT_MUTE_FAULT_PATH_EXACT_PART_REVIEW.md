# Output Mute and Fault-Control Exact-Part Review

## Decision after evidence repair

```text
Q70 MMBFJ113 EXACT PART / PIN MAP / PACKAGE: ACCEPTED FOR GATE B
Q71 PMV20XNE EXACT PART / PIN MAP / PACKAGE: ACCEPTED FOR GATE B
U70 VO617A-3X007T EXACT PART / PIN MAP / PACKAGE: ACCEPTED FOR GATE B
POWERED HEALTHY-RELEASE TOPOLOGY: ACCEPTED AT CALCULATED SCHEMATIC LEVEL
U70 ACTUAL-BIAS SATURATION PROOF: PASS
Q70 25 C DATASHEET-BOUND MUTE CALCULATION: PASS — 61.50 dB
HASH-LOCKED DIMENSIONAL FOOTPRINT AUDIT: PASS
MEASURED BEHAVIOUR: TRANSFERRED TO GATE C
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
PR ACCEPTANCE: SUBJECT TO NEW HUMAN REVIEW
```

The former non-saturated CTR argument and name-only footprint check are withdrawn and replaced by the evidence below.

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

| Ref | Exact part | Package | Physical pins | KiCad footprint |
|---|---|---|---|---|
| Q70 | onsemi MMBFJ113 | SOT-23 / TO-236, case 318-08 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia PMV20XNE | TO-236AB / SOT23 | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay VO617A-3X007T | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

## U70 actual-bias saturation proof

Vishay guarantees:

```text
IF = 5 mA
IC = 1.0 mA
VCE(sat) <= 0.4 V
```

The conservative LED path produces at least `5.304 mA`. The actual release-path load at the guaranteed saturation voltage is:

```text
RAIL_N12 magnitude at +5% = 12.6 V
R715 + R716 at -1% = 108.9 kOhm
VCE = 0.4 V
required collector current = 0.112 mA
```

The guaranteed saturated test current is `1.0 mA`, giving `8.93:1` margin. This proof follows the realised resistor load line and does not use the `VCE = 5 V` CTR condition.

## Q70 mute-depth boundary

```text
TJ = 25 C
VGS = 0 V
VDS <= 0.1 V
MMBFJ113 rDS(on) maximum = 100 ohm
R703 minimum = 118.8 kOhm
calculated static attenuation = 61.50 dB
```

This is explicitly a 25 C datasheet-bound calculation, not a full-temperature or production guarantee. Gate C must prove at least `60 dB` on assembled hardware across the declared temperature, device spread and signal conditions.

## Dimensional footprint evidence

The audit parses SHA-256-locked snapshots from KiCad's official footprint library:

```text
SOT-23.kicad_mod
sha256 f8fd6dd6411c47f6547df13b1efe33867682117b7fb6f2ea829d1d726d565887

SMDIP-4_W7.62mm.kicad_mod
sha256 5d9faa2287c41ae0b7930be347813bde5098acb8688513fff275fde904b532a0
```

Verified geometry:

```text
SOT-23 pads:       1.475 x 0.600 mm
SOT-23 pin-1/2:    1.900 mm pitch
SOT-23 courtyard:  3.860 x 3.400 mm

SMDIP-4 pads:      2.000 x 1.780 mm
SMDIP-4 rows:      7.620 mm
SMDIP-4 pin pitch: 2.540 mm
SMDIP-4 courtyard: 10.140 x 5.580 mm
```

Pad centres, pin-one orientation, package pitch and courtyard coverage were compared with the manufacturer package records. This does not authorise placement, neighbour clearances, assembly process, creepage strategy or purchasing.

## Validation evidence

Committed head `59b96b78891bc95c6c025fad70b9137c6c4241f4` passed workflow run `29339271573`:

```text
first-generation capture                SKIPPED
sheet qualification                     CURRENT
actual-bias electrical validator        PASS
exact symbol / physical-pin validator   PASS
hash-locked dimensional footprint audit PASS
shared U32 / hierarchy validator        PASS
KiCad 10 hierarchical ERC               PASS — 0 errors / 0 warnings
promotion                               NO DIFF
```

## Remaining measured gates

Gate C retains mute depth across temperature and part spread, audible pop and transient energy, real rail ramps and sequencing, load drive, output impedance and endurance.

PCB placement, routing, fabrication and purchasing remain blocked. PR #46 must receive a new deliberate approval review before merge.
