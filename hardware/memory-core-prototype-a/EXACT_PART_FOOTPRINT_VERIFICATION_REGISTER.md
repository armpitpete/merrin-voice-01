# Exact-Part and Footprint Verification Register

## Authority

This register begins Gate B after the deliberate squash merge of PR #45.

```text
Gate A — schematic acceptance       PASS / MERGED
Gate B — exact parts / footprints   ACTIVE
Gate C — bench acceptance           NOT STARTED
Gate D — PCB / production           BLOCKED
```

Gate B may return an assumption to schematic correction. It does not authorise PCB placement, routing, fabrication, purchasing or a production claim.

## Verification rule

An active device or connector is accepted only when all of the following are fixed and independently checked:

1. exact manufacturer and orderable part number;
2. manufacturer datasheet and revision;
3. package designation and physical dimensions;
4. physical pin numbering and schematic-symbol mapping;
5. electrical limits at the actual circuit bias and fault states;
6. one reviewed KiCad footprint mapped to the physical package;
7. any package-specific thermal, clearance or assembly constraint;
8. an explicit status of `ACCEPTED`, `BLOCKED` or `RETURN TO SCHEMATIC`.

A generic class name, typical graph, assumed current-transfer ratio or visually similar footprint is not acceptance evidence.

## Lane 01 — output mute and fault-control path

Detailed review:

- `OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md`

Current result:

```text
Q70 output-mute JFET          RETURN TO SCHEMATIC
Q71 fault inverter NPN        RETURN TO SCHEMATIC
U70 fault optocoupler         BLOCKED
OUTPUT FAULT-RAIL BEHAVIOUR   RETURN TO SCHEMATIC
FOOTPRINTS ASSIGNED           NONE
```

### Candidate register

| Ref | Current class | Exact candidate reviewed | Package | Current decision | Blocking reason |
|---|---|---|---|---|---|
| Q70 | J113-class N-channel JFET | onsemi `MMBFJ113` | SOT-23 / TO-236 | RETURN TO SCHEMATIC | Gate is physical pin 3, but the accepted logical symbol places gate on pin 2. Maximum 100 ohm on-resistance also gives only about 40.1 dB ideal shunt attenuation through R703 = 10 kOhm. |
| Q71 | MMBT3904-class NPN | onsemi `MMBT3904LT1G` | SOT-23 / TO-236 | RETURN TO SCHEMATIC | Physical pins are 1 base, 2 emitter, 3 collector; the accepted `Q_NPN_BCE` symbol uses 1 base, 2 collector, 3 emitter. Guaranteed saturation is also not established at the realised base drive. |
| U70 | LTV-817S-class phototransistor optocoupler | exact suffix not fixed | SO-4 class | BLOCKED | The current timing calculation assumes 50% CTR at about 1.96 mA LED current. No exact ordering suffix or guaranteed low-current CTR has been accepted. |

## Required correction order

1. Define the minimum acceptable measured mute depth and the maximum allowed pop energy.
2. Correct Q70 and Q71 physical pin maps before any footprint is attached.
3. Correct the output fault path so loss of the positive rail cannot release the mute while the negative rail remains present.
4. Select an exact optocoupler suffix or revise the bias so minimum CTR is guaranteed at the design current and temperature range.
5. Recalculate Q71 base drive using the actual open-drain `HARDWARE_FAULT_N` source impedance.
6. Regenerate sheet 07, rerun the existing validators and KiCad ERC, and review the schematic diff.
7. Only then verify and assign the three physical footprints.

## Remaining Gate-B lanes

After this lane closes:

1. input and output jacks;
2. SSI2164 package and control-law assumptions;
3. OPA1679 package and decoupling requirements;
4. Return limiter and clamp diodes;
5. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.