# Input and Output Jack Exact-Part Lane — Edit Contract

## Goal

Verify the exact input and output jack models used by `J40` and `J70`, including:

- switched-contact behaviour;
- physical contact numbering;
- schematic use of the normal contact;
- mechanical envelope;
- PCB hole pattern;
- panel-hole and panel-to-PCB geometry;
- panel-retention method;
- immutable KiCad footprint provenance;
- symbol-to-footprint pad mapping.

## Allowed files

- `hardware/memory-core-prototype-a/04_INPUT_PRESSURE_ABSENCE.kicad_sch`
- `hardware/memory-core-prototype-a/07_OUTPUT_MUTE_PROTECTION.kicad_sch`
- `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.kicad_sym`
- jack-specific Gate-B records under `hardware/memory-core-prototype-a/`
- jack-specific project-local footprint snapshots under `hardware/memory-core-prototype-a/jack-footprint-audits/`
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
- no direct assignment of a footprint whose pad identifiers do not match the schematic symbol.

## Expected diff

The initial gate is evidence-first:

1. record the current `J40` and `J70` electrical contracts;
2. retain `WQP518MA` as the exact candidate, not an accepted part;
3. pin and inspect the strongest available PJ398SM/WQP518MA footprint source;
4. identify any symbol, footprint, panel or mounting mismatch;
5. keep both schematic footprints blank until all acceptance conditions pass.

A later bounded patch may correct the symbol and assign one reviewed project-local footprint to both jacks. That change must be independently validated before acceptance.

## Check command

```text
python tools/validate_jack_exact_part_lane.py
```

After any native schematic amendment, also run the complete KiCad 10 hierarchical ERC policy.

## Stop rule

Stop and return the lane for review if any of these remains unknown or contradictory:

- exact orderable jack identity;
- normally closed contact behaviour;
- physical contact numbering;
- symbol-to-footprint pad correspondence;
- panel-hole diameter;
- panel-to-PCB seating geometry;
- exact nut/washer retention arrangement;
- immutable footprint source;
- manufacturer or supplier dimensional equivalence.

PCB placement, routing, panel fabrication, purchasing and production remain blocked throughout this lane.
