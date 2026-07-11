# 06_RETURN_BREAK_LIMITER — Validation Record

## Status

```text
GENERATED ARTIFACT: PASS
SYMBOL / PIN CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PASS
COMMITTED-FILE RERUN: PASS
PCB / FOOTPRINT / MECHANICAL AUTHORITY: NOT GRANTED
```

## Corrected design evidence

The accepted Return sheet was regenerated after rejecting an earlier stale artifact.

Corrections made before acceptance:

1. **Official SSI2164 channel mapping**

   ```text
   channel 3 input   = pin 15 — IIN3
   channel 3 control = pin 14 — VC3
   channel 3 output  = pin 13 — IOUT3
   ```

   Pins `10/11/12` are channel 4 and are reserved for the later wet-master circuit on sheet 05.

2. **Post-codec Return normalisation**

   Sheet 03 produces the Return output at approximately `0.747` gain. Sheet 06 applies a `20 kΩ / 10 kΩ` divider before the SSI2164:

   ```text
   0.747 × 1/3 ≈ 0.249
   ```

   This reconciles the codec receiver with the accepted Return gain contract.

3. **Unique schematic references**

   The second accidental uses of `C610` and `C611` were renamed:

   ```text
   Break bandwidth capacitor  = C640
   Return bandwidth capacitor = C641
   ```

   Values, nets and topology did not change.

4. **Staged multi-unit SSI2164 handling**

   KiCad ERC requires every unit of the physical multi-unit device to be placed. U60 units 1, 2 and 4 are therefore shown visibly as explicit no-connect reservations for sheet 05. They use the same `U60` reference and do not represent duplicate chips.

   Sheet 05 must remove those reservations and connect the real Memory, Ghost and wet-master channels.

## Locked sheet boundary

Only these signals may leave sheet 06:

```text
RETURN_LIMITED
RETURN_FEED
ABSENCE_INFLUENCE
```

The following remain local:

```text
raw RETURN_DAC conditioning
SSI2164 current nodes
BREAK output
analogue Return nonlinear output
clamp node
±2.5 V limiter references
```

## Generated-artifact gate result

The dedicated Return workflow passed:

- Return safety hierarchy amendment;
- official SSI2164 symbol/pin contract;
- unique-reference check;
- all-five-unit staged placement check;
- fixed `27.4 kΩ / 40.2 kΩ` Return-feed contract;
- native KiCad 10 parsing;
- full hierarchical ERC with zero errors;
- strict captured-sheet warning policy.

## Committed-file rerun result

The second Return workflow run detected the committed stage and therefore skipped:

```text
Return safety-interface amendment
generation
multi-unit repair
promotion
```

It then passed:

- the symbol/pin and staged-unit contract against the committed native file;
- the unique-reference check;
- KiCad 10 hierarchical ERC;
- the strict captured-sheet warning policy.

`06_RETURN_BREAK_LIMITER` is closed at schematic-capture level. Physical footprint review, integrated Return safety review, measured loop gain, limiter threshold/recovery measurements, and the 30-minute worst-setting endurance test remain later gates.
