# Output Mute and Fault-Control Exact-Part Review

## Decision

```text
OUTPUT-MUTE / FAULT-CONTROL EXACT-PART GATE: NOT PASSED
Q70 DIRECT FOOTPRINT ASSIGNMENT: REJECTED
Q71 DIRECT FOOTPRINT ASSIGNMENT: REJECTED
U70 EXACT PART / FOOTPRINT: BLOCKED
SHEET 07 SCHEMATIC CORRECTION: REQUIRED
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
```

This review does not invalidate the Gate-A schematic architecture. It identifies physical-part facts that must return to sheet 07 before Gate B can accept parts or footprints.

## Reviewed circuit

Current fault-control path:

```text
RAIL_3V3 -- R10 10k -- HARDWARE_FAULT_N -- R711 10k -- Q71 base
                                                |
                                             R712 100k
                                                |
                                               GND

RAIL_P12 -- R713 2.2k -- MUTE_FAULT_HIGH -- R714 3.3k -- U70 LED -- GND
                              |
                           Q71 collector
Q71 emitter ----------------- GND

RAIL_N12 -- R715 100k -- MUTE_GATE -- R716 1M -- GND
                              |
                            C710 1uF
                              |
                             GND

U70 phototransistor: collector at GND, emitter at MUTE_GATE
Q70 JFET shunt: MUTE_NODE to GND, controlled by MUTE_GATE
```

The accepted capture uses blank active-device footprints and explicitly transfers mute depth, fault timing, rail sequencing and exact package selection to this gate.

## Q70 — output-mute JFET

### Exact candidate reviewed

```text
Manufacturer: onsemi
Part:         MMBFJ113
Function:     N-channel analog-switch JFET
Package:      SOT-23 / TO-236, case 318
Datasheet:    MMBFJ113/D, Rev. 5, March 2023
Source:       https://www.onsemi.com/pdf/datasheet/mmbfj113-d.pdf
```

Manufacturer facts relevant to this circuit:

```text
physical pin 1 = drain
physical pin 2 = source
physical pin 3 = gate
source and drain are interchangeable
VGS(off), J113 = -0.5 V to -3.0 V
rDS(on), J113 = 100 ohm maximum at VGS = 0 V
```

### Pin-map result

Current accepted logical mapping:

```text
Q70 pin 1 = MUTE_NODE
Q70 pin 2 = MUTE_GATE
Q70 pin 3 = GND
```

Required `MMBFJ113` physical mapping:

```text
Q70 pin 1 = MUTE_NODE    (drain)
Q70 pin 2 = GND          (source)
Q70 pin 3 = MUTE_GATE    (gate)
```

The current symbol places the gate on physical pin 2. Source/drain interchangeability does not cure a gate-pin error. A SOT-23 footprint must not be attached to the current symbol.

### Electrical result

The nominal healthy gate calculation remains about `-10.91 V`. Against the worst specified J113 cutoff magnitude of `3.0 V`, the nominal off-state margin is about `7.91 V`.

The mute-on resistance is not sufficient to claim silence:

```text
R703 series isolation = 10,000 ohm
MMBFJ113 worst rDS(on) = 100 ohm
ideal static ratio     = 100 / (10,000 + 100)
                       = 0.009901
ideal attenuation      = about -40.1 dB
```

This ignores signal dependence, temperature, JFET spread, op-amp behaviour, leakage and board parasitics. `MMBFJ113` is therefore an electrically plausible prototype candidate, but it is not accepted until a minimum mute-depth target is defined and the measured gate is planned.

### Q70 decision

```text
PART CANDIDATE: RETAIN FOR COMPARISON
SYMBOL PIN MAP: FAIL
FOOTPRINT: NOT ACCEPTED
MUTE-DEPTH CLAIM: NOT ACCEPTED
STATUS: RETURN TO SCHEMATIC
```

## Q71 — fault inverter NPN

### Exact candidate reviewed

```text
Manufacturer: onsemi
Part:         MMBT3904LT1G
Function:     general-purpose NPN transistor
Package:      SOT-23 / TO-236, case 318
Datasheet:    MMBT3904LT1/D, Rev. 14, August 2021
Source:       https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf
```

Manufacturer pin map:

```text
physical pin 1 = base
physical pin 2 = emitter
physical pin 3 = collector
```

### Pin-map result

The accepted sheet uses KiCad `Q_NPN_BCE`:

```text
logical pin 1 = base
logical pin 2 = collector
logical pin 3 = emitter
```

The current net assignment is consequently:

```text
Q71 pin 1 = FAULT_INV_BASE
Q71 pin 2 = MUTE_FAULT_HIGH
Q71 pin 3 = GND
```

The exact `MMBT3904LT1G` requires:

```text
Q71 pin 1 = FAULT_INV_BASE
Q71 pin 2 = GND
Q71 pin 3 = MUTE_FAULT_HIGH
```

A standard SOT-23 footprint attached to the present `Q_NPN_BCE` symbol would swap collector and emitter.

### Base-drive result

`HARDWARE_FAULT_N` is not a zero-ohm 3.3 V source. It is an open-drain shared fault net pulled to `RAIL_3V3` by `R10 = 10 kOhm` on sheet 01. Q71 then adds `R711 = 10 kOhm` in series and `R712 = 100 kOhm` from base to ground.

Using a first-pass `VBE = 0.7 V`:

```text
current through R10 + R711 = (3.3 - 0.7) / 20k = 0.130 mA
R712 current at 0.7 V      = 0.007 mA
estimated Q71 base current = 0.123 mA
```

When healthy, Q71 must sink approximately the `R713` pull-up current:

```text
about (12 V - VCE) / 2.2k = about 5.4 mA
forced beta                = about 44
```

The onsemi guaranteed saturation point is specified at `IC = 10 mA, IB = 1 mA`, a forced beta of 10. The current design does not operate at that guaranteed test ratio. Typical behaviour may be adequate, but exact-part acceptance cannot be based on typical gain.

The base load also pulls the shared `HARDWARE_FAULT_N` healthy level below its unloaded 3.3 V value. That interaction must be included in the fault-net review.

### Q71 decision

```text
PART CANDIDATE: ELECTRICALLY PLAUSIBLE
SYMBOL PIN MAP: FAIL
GUARANTEED SATURATION: NOT ESTABLISHED
FOOTPRINT: NOT ACCEPTED
STATUS: RETURN TO SCHEMATIC
```

## U70 — isolated fault clamp

### Current candidate state

The accepted capture names an `LTV-817S-class` SO-4 phototransistor optocoupler and uses the conventional logical pin map:

```text
pin 1 = LED anode
pin 2 = LED cathode
pin 3 = emitter
pin 4 = collector
```

The circuit calculates about `1.96 mA` LED current during a fault and estimates clamp time using an assumed `50% CTR`.

### Exact-part result

No exact manufacturer ordering suffix or CTR rank is fixed. The current review has not established a guaranteed minimum CTR at approximately `1.96 mA` over the intended temperature range.

To move the `1 uF` gate capacitor from about `-10.91 V` to 0 V within 20 ms while overcoming the `100 kOhm` negative pull requires roughly:

```text
capacitor current = 10.91 V * 1uF / 20 ms = 0.546 mA
negative-pull current near 0 V            = 0.120 mA
required average collector current        = about 0.666 mA
required CTR at 1.96 mA LED current        = about 34%
```

That is a circuit requirement, not a verified part guarantee. The exact optocoupler must provide margin beyond it at minimum CTR, temperature and ageing, or the LED bias and timing network must be revised.

### U70 decision

```text
EXACT ORDERING CODE: NOT FIXED
LOW-CURRENT CTR GUARANTEE: NOT ESTABLISHED
TIMING GUARANTEE: NOT ESTABLISHED
FOOTPRINT: NOT ACCEPTED
STATUS: BLOCKED
```

## Rail-loss fault behaviour

The current path is asymmetric:

- loss of `RAIL_N12` removes the negative release pull and lets `R716` move `MUTE_GATE` toward ground, which tends to mute;
- loss of `RAIL_P12` also removes the source of `RAIL_3V3`, the `HARDWARE_FAULT_N` pull-up and the optocoupler LED current;
- if `RAIL_N12` remains present during that condition, `R715` pulls `MUTE_GATE` negative and releases Q70 instead of enforcing mute.

Therefore the present circuit does not establish fail-muted behaviour for positive-rail loss or asymmetric rail sequencing. Exact part selection cannot repair this topology by itself.

```text
RAIL-LOSS FAIL-MUTE CLAIM: REJECTED
STATUS: RETURN TO SCHEMATIC
```

## Required schematic correction

The next bounded engineering patch must:

1. replace or correct the Q70 symbol so physical pin 3 is the gate;
2. replace Q71 with a physical `B-E-C` pin-map symbol and reconnect collector/emitter nets;
3. define the required mute depth before deciding whether `MMBFJ113` is sufficient;
4. redesign or formally constrain the fault path so positive-rail loss cannot release the mute;
5. select an exact optocoupler ordering code and prove minimum CTR at the realised LED current;
6. prove Q71 saturation using the actual `R10 + R711` source impedance, or revise the drive network;
7. regenerate sheet 07 and rerun all committed-file validators plus KiCad ERC.

Only after that schematic patch is reviewed may the SOT-23 and SO-4 footprints be independently verified and assigned.

## Gate status after this review

```text
Gate A — schematic architecture     REMAINS ACCEPTED
Gate B — output mute/fault parts    RETURNED TO SCHEMATIC
Gate C — measured mute/fault tests  NOT STARTED
Gate D — PCB / production           BLOCKED
```