# Input and Output Jack Exact-Part Lane — Edit Contract

## Goal

Verify the exact input and output jack models used by `J40` and `J70`, including:

- switched-contact behaviour;
- physical contact numbering;
- controlled WQP518MA/PJ398SM equivalence;
- mechanical envelope;
- PCB hole pattern and barrel relief;
- panel-hole and panel-to-PCB geometry;
- exact nut, washer and panel stack;
- immutable KiCad footprint provenance;
- symbol-to-footprint pad mapping.

## Allowed files

- `hardware/memory-core-prototype-a/04_INPUT_PRESSURE_ABSENCE.kicad_sch`
- `hardware/memory-core-prototype-a/07_OUTPUT_MUTE_PROTECTION.kicad_sch`
- `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.kicad_sym`
- `hardware/memory-core-prototype-a/fp-lib-table`
- jack-specific Gate-B records under `hardware/memory-core-prototype-a/`
- immutable source snapshots under `hardware/memory-core-prototype-a/jack-footprint-audits/`
- the numeric project footprint under `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.pretty/`
- jack-specific validators under `tools/`
- jack-specific GitHub Actions workflow changes
- `EXACT_PART_FOOTPRINT_VERIFICATION_REGISTER.md`

## Forbidden changes

- no PCB creation, placement or routing;
- no panel CAD or fabrication drawing release;
- no purchasing authorisation;
- no changes to Q70, Q71 or U70;
- no changes to audio gain, protection, mute or Return topology;
- no unrelated exact-part decisions;
- no silent substitution between `WQP518MA`, `PJ398SM` and `PJ301M-12`;
- no direct assignment of a footprint whose pad identifiers do not match the schematic symbol;
- no footprint assignment before the panel stack passes physical or controlled-document review.

## Expected diff

This bounded repair may:

1. accept Thonk's supplier-controlled WQP518MA/PJ398SM contact and footprint equivalence;
2. pin an official KiCad WQP/PJ398SM footprint snapshot to an immutable commit;
3. create a project-local numeric footprint with `1=TIP`, `2=TIP_NORMAL`, `3=SLEEVE`;
4. add a real `3.00 mm` NPTH barrel relief at the published barrel centre;
5. select the supplier's compatible hex-nut and washer product variants;
6. record derived panel-hole and seating targets;
7. create a physical-sample measurement record for dimensions the supplier does not publish;
8. keep both schematic footprint fields blank until the hardware stack is proven.

A later bounded patch may assign the reviewed project-local footprint to J40 and J70 only after the sample record or a controlled hardware drawing proves the thread, nut, washer and 2 mm panel stack.

## Check command

```text
python tools/validate_jack_exact_part_lane.py
```

The complete KiCad 10 hierarchical ERC policy must remain at zero errors and zero warnings.

## Stop rule

Stop for human measurement rather than assign the footprint if any of these remains unknown:

- bushing thread pitch;
- nut thickness;
- washer thickness;
- secure engagement through the 2.00 mm panel;
- actual panel-to-PCB seating distance;
- whether panel clamping loads the solder joints or lifts the jack from the PCB.

The current stop is therefore deliberate: the supplier-controlled electrical and PCB geometry may pass while mechanical stack acceptance remains blocked.

PCB placement, routing, panel fabrication, purchasing and production remain blocked throughout this lane.
