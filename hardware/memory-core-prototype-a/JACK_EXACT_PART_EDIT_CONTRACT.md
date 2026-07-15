# Input and Output Jack Exact-Part Lane — Edit Contract

## Goal

Verify and assign the exact input and output jack footprints used by `J40` and `J70`, including:

- switched-contact behaviour;
- physical contact numbering;
- controlled WQP518MA/PJ398SM equivalence;
- mechanical envelope;
- PCB hole pattern and barrel relief;
- corrected nut-only panel stack;
- immutable KiCad footprint provenance;
- symbol-to-footprint pad mapping;
- bounded instance-specific footprint assignment;
- post-assignment validation.

## Current mechanical authority

```text
panel nominal thickness      1.60 mm
panel construction           provisional FR-4 PCB panel
panel supplier               not locked; JLCPCB only a possibility
retaining hardware           selected Thonk hex nut
washer                       none
thread above nominal panel   2.90 mm before nut engagement
physical fit                 user-attested pass
independent review           pass
```

The former `2.00 mm aluminium + washer + nut` stack is rejected and retained only as superseded history.

## Allowed files for the completed lane

- `hardware/memory-core-prototype-a/04_INPUT_PRESSURE_ABSENCE.kicad_sch`
- `hardware/memory-core-prototype-a/07_OUTPUT_MUTE_PROTECTION.kicad_sch`
- `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.kicad_sym`
- `hardware/memory-core-prototype-a/fp-lib-table`
- jack-specific Gate-B records under `hardware/memory-core-prototype-a/`
- immutable source snapshots under `hardware/memory-core-prototype-a/jack-footprint-audits/`
- the numeric project footprint under `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.pretty/`
- `tools/capture_input_pressure_absence_sheet.py`
- `tools/capture_output_mute_protection_sheet.py`
- `tools/validate_jack_exact_part_lane.py`
- `.github/workflows/kicad-jack-exact-parts.yml`
- `EXACT_PART_FOOTPRINT_VERIFICATION_REGISTER.md`

## Forbidden changes

- no PCB creation, placement or routing;
- no panel CAD or fabrication drawing release;
- no purchasing authorisation;
- no changes to Q70, Q71 or U70;
- no changes to audio gain, protection, mute or Return topology;
- no unrelated exact-part decisions;
- no silent substitution between `WQP518MA`, `PJ398SM` and `PJ301M-12`;
- no project-symbol default footprint assignment without a separate decision;
- no PCB or panel release merely because the schematic footprint assignment passed.

## Completed evidence and implementation

This lane has:

1. accepted Thonk's supplier-controlled WQP518MA/PJ398SM contact and PCB-terminal equivalence;
2. pinned an official KiCad WQP/PJ398SM footprint snapshot to an immutable commit;
3. created a project-local numeric footprint with `1=TIP`, `2=TIP_NORMAL`, `3=SLEEVE`;
4. added a `3.00 mm` NPTH barrel relief at the published barrel centre;
5. selected the compatible Thonk hex nut;
6. recorded that no washer is used;
7. recorded the provisional `1.60 mm` panel target;
8. recorded the project owner's corrected-stack physical-fit attestation;
9. independently approved the corrected physical-fit record;
10. assigned the numeric footprint to J40 and J70 only;
11. kept the project symbol default footprint blank;
12. updated both controlled generators and generated sheets;
13. passed the lane validator and complete KiCad hierarchical ERC chain.

Assigned footprint:

```text
MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric
```

Assignment commit:

```text
f34eea95c216cd31df4d4e3f1498adc4b9014ec9
```

## Superseded pre-assignment gate

The independent-review stage authorised assignment while deliberately leaving J40 and J70 blank. That state was correct for that historical review point but was superseded when the bounded assignment patch was applied. It is not current authority.

## Check command

```text
python tools/validate_jack_exact_part_lane.py
```

The complete KiCad 10 hierarchical ERC policy must remain at zero errors and zero warnings.

## Deferred mechanical-release gate

Before PCB placement, standoff selection, panel CAD, panel fabrication or purchasing, a later controlled gate must lock or measure:

- final panel material and supplier;
- actual finished panel thickness or controlled supplier tolerance;
- actual panel-to-PCB seating distance;
- finished panel-hole diameter and manufacturing tolerance;
- any resulting axis-offset or clearance correction.

## Current stop rule

```text
corrected physical fit                 APPROVED
independent mechanical review          PASS
J40 footprint field                    ASSIGNED
J70 footprint field                    ASSIGNED
project symbol default                 BLANK
post-assignment validation             PASS
PCB creation / placement / routing     BLOCKED
panel CAD / fabrication                BLOCKED
purchasing / production                BLOCKED
PR #47                                 DRAFT / UNMERGED
```

The next permitted action is merge review of PR #47 after a fresh untouched validation chain passes on the repository-authority synchronisation head.

PCB creation, placement, routing, panel CAD, fabrication, purchasing and production remain blocked.