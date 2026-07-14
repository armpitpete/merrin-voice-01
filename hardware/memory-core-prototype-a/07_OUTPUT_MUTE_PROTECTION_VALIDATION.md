# 07_OUTPUT_MUTE_PROTECTION — Validation Record

## Current status

```text
SCHEMATIC-CAPTURE CONTRACT: PASS
EXACT Q70 / Q71 / U70 PIN-MAP CONTRACT: PASS
EXACT Q70 / Q71 / U70 FOOTPRINT MAPPING: PASS
HEALTHY-RELEASE FAIL-MUTE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
CALCULATED STATIC MUTE ATTENUATION: 61.50 dB
CALCULATED FAULT / +12 V LOSS CROSSING: 12.57 ms
SHARED U32 CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PENDING CURRENT PR RERUN
MEASURED MUTE / POP / RAIL SEQUENCING: NOT ACCEPTED
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
```

## Corrected exact parts

| Ref | Exact part | Pin map | Footprint |
|---|---|---|---|
| Q70 | onsemi MMBFJ113 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia PMV20XNE | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay VO617A-3X007T | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

The exact symbols are embedded in sheet 07 and stored in the project symbol library with manufacturer datasheets and reviewed package mappings.

## Corrected fail-mute path

Healthy operation powers the isolated negative release path. Fault or positive-rail loss removes that release path. This reverses the former unsafe dependency in which loss of the positive rail could leave the negative rail releasing the mute.

```text
healthy fault signal
  -> PMV20XNE on
  -> VO617A-3 LED on
  -> phototransistor connects RAIL_N12 release path
  -> MUTE_GATE approximately -10.545 V
  -> MMBFJ113 off

fault / undefined signal / RAIL_P12 loss
  -> PMV20XNE or VO617A off
  -> negative release path opens
  -> 100 kOhm / 100 nF returns MUTE_GATE toward 0 V
  -> MMBFJ113 turns on
  -> output shunted through Q70 after 120 kOhm isolation
```

## Calculated contracts

### Static mute target

```text
R703 minimum at -1% = 118.8 kOhm
MMBFJ113 maximum rDS(on) = 100 ohm
calculated attenuation = 61.50 dB
required schematic minimum = greater than 60 dB
required later measured minimum = at least 60 dB
```

### Fault timing

```text
healthy gate estimate using VO617A VCE(sat) max = -10.545 V
worst J113 cutoff boundary = -3.0 V
R716 x C710 time constant = 10 ms
calculated crossing time = 12.57 ms
schematic target = less than 20 ms
```

### Release-driver gate

```text
R10 + R711 source path = 20 kOhm nominal
R712 gate pull-down = 100 kOhm
conservative PMV20XNE gate estimate = 2.604 V
PMV20XNE guaranteed RDS(on) test point = 2.5 V
```

### Optocoupler CTR

```text
R713 + R714 = 1.82 kOhm nominal
conservative LED-current estimate = 5.304 mA
VO617A-3 minimum CTR = 100% at 5 mA
minimum guaranteed collector capability = 5.304 mA
maximum calculated initial release-path current = 1.055 mA
```

## Unchanged boundaries

- sheet 07 still exports no hierarchy net;
- `U32` remains one physical OPA1679 split across sheets 03 and 07;
- the output jack remains a separate exact-part/mechanical gate;
- no PCB placement or routing is authorised;
- measured mute depth, pop energy, rail sequencing, load drive and endurance remain Gate C.

## Required current-PR verification

The dedicated output workflow must:

1. run the amendment script idempotently;
2. validate exact symbols, pins, values and footprints;
3. validate the corrected net topology and calculations;
4. validate unchanged shared-U32 and hierarchy boundaries;
5. run KiCad 10 hierarchical ERC;
6. enforce zero errors and zero warnings.

This record becomes closed only when those checks pass on the committed PR head.
