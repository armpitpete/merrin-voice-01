# Input and Output Jack Exact-Part Lane — Edit Contract

## Goal

Verify the exact input and output jack models used by `J40` and `J70`, including:

- switched-contact behaviour;
- physical contact numbering;
- controlled WQP518MA/PJ398SM equivalence;
- mechanical envelope;
- PCB hole pattern and barrel relief;
- panel-hole and panel-to-PCB geometry;
- exact nut-only panel stack;
- immutable KiCad footprint provenance;
- symbol-to-footprint pad mapping.

## Corrected mechanical authority

```text
panel nominal thickness      1.60 mm
panel construction           provisional FR-4 PCB panel
panel supplier               not locked; JLCPCB only a current possibility
retaining hardware           selected Thonk hex nut
washer                       none
thread above nominal panel   2.90 mm before nut engagement
physical fit                 user-attested pass
independent review           approved for next bounded assignment gate
```

The former `2.00 mm aluminium + washer + nut` stack is rejected. No fit result from that superseded stack may be used to approve the corrected assembly.

No footprint assignment before the panel stack passes physical or controlled-document review was permitted. That prerequisite is now satisfied for the next bounded footprint-assignment patch only.

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
- no PCB placement or panel release merely because the footprint-assignment gate is authorised.

## Completed evidence

This lane has:

1. accepted Thonk's supplier-controlled WQP518MA/PJ398SM contact and footprint equivalence;
2. pinned an official KiCad WQP/PJ398SM footprint snapshot to an immutable commit;
3. created a project-local numeric footprint with `1=TIP`, `2=TIP_NORMAL`, `3=SLEEVE`;
4. added a real `3.00 mm` NPTH barrel relief at the published barrel centre;
5. selected the supplier's compatible hex-nut product variant;
6. recorded that no washer is used;
7. recorded the provisional `1.60 mm` panel target and derived seating targets;
8. recorded the project owner's corrected-stack physical-fit attestation;
9. independently approved the corrected physical-fit record;
10. kept both schematic footprint fields blank during the review-only gate.

## Next bounded patch

The next patch may only:

1. assign `MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric` to J40 and J70;
2. update the controlled schematic generators and generated sheets consistently;
3. leave the project symbol default footprint blank unless separately justified;
4. rerun the complete KiCad 10 hierarchical ERC and lane validator;
5. record the exact assignment head and validation results;
6. stop before PCB placement, routing, panel CAD, fabrication or purchasing.

## Check command

```text
python tools/validate_jack_exact_part_lane.py
```

The complete KiCad 10 hierarchical ERC policy must remain at zero errors and zero warnings.

## Deferred mechanical-release gate

Before PCB placement, standoff selection, panel fabrication or purchasing, a later controlled gate must lock or measure:

- final panel material and supplier;
- actual finished panel thickness or controlled supplier tolerance;
- actual panel-to-PCB seating distance;
- finished panel-hole diameter and manufacturing tolerance;
- any resulting axis-offset or clearance correction.

## Stop rule

This independent-review gate stops with:

```text
corrected physical fit                 APPROVED
next footprint-assignment gate         AUTHORISED
J40 / J70 footprint fields             BLANK
PCB placement and routing              BLOCKED
panel fabrication                      BLOCKED
purchasing                             BLOCKED
```

PCB placement, routing, panel fabrication, purchasing and production remain blocked throughout this lane.