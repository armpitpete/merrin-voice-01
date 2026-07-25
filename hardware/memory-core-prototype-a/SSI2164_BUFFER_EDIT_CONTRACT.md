# SSI2164 buffered-control edit contract

## Goal

Correct the SSI2164 control-voltage loading error by inserting one dedicated OPA4196 quad unity-gain buffer between the TMUX1574 filtered control nodes and the four SSI2164 control inputs.

The implemented control law must preserve:

```text
0.00 V at SSI VC  = unity
3.30 V at SSI VC  = approximately -100 dB attenuation
negative SSI VC   = forbidden
```

## Base authority

```text
main commit                  8df52377de753c8c910d67fc31405782d52a1be8
Lane 02 jack authority       CLOSED
PCB / panel / purchasing     BLOCKED
```

## Selected architecture

```text
buffer                         OPA4196 quad operational amplifier
supply                         protected +/-12 V
configuration                  four unity-gain followers
ownership                      one shared five-unit U63 across sheets 05 and 06
package target                 PW / TSSOP-14
footprint assignment           BLOCKED pending exact footprint review
local supply bypass            100 nF from each supply pin to ground
pre-buffer filtering           existing 1 kΩ / capacitor networks
post-buffer isolation          20 ohm per channel
post-buffer clamps             0 V and +3.3 V boundaries
```

Sheet 05 owns OPA4196 units 1, 2 and 4 for Memory, Ghost and wet master. Sheet 06 owns unit 3 for Return and unit 5 for common power. Sheet 08 remains the TMUX1574 safe-selector and first-filter stage.

The OPA4196 is separate from the seven-package OPA1679 audio allocation.

## Final authority files

- `docs/v5.2-ssi2164-mcp4728-fail-safe-control.md`
- `docs/v5.2-power-current-and-thermal-budget.md`
- `docs/v5.2-return-limiter-and-opamp-allocation.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_EDIT_CONTRACT.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_CONTROL_REVIEW.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_AUDIT.json`
- `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.kicad_sym`
- `hardware/memory-core-prototype-a/05_MEMORY_GHOST_WET.kicad_sch`
- `hardware/memory-core-prototype-a/06_RETURN_BREAK_LIMITER.kicad_sch`
- `hardware/memory-core-prototype-a/05_MEMORY_GHOST_WET_VALIDATION.md`
- `hardware/memory-core-prototype-a/06_RETURN_BREAK_LIMITER_VALIDATION.md`
- `tools/capture_memory_ghost_wet_sheet.py`
- `tools/capture_memory_ghost_wet_sheet_v2.py`
- `tools/capture_return_break_limiter_sheet.py`
- `tools/capture_return_break_limiter_sheet_v3.py`
- `tools/repair_ssi2164_buffer_opa4196_units.py`
- `tools/validate_memory_ghost_wet_capture.py`
- `tools/validate_ssi2164_buffer_lane.py`
- `.github/workflows/kicad-return-sheet-erc.yml` only to permit both shared multi-unit references U60 and U63
- `.github/workflows/ssi2164-buffered-control-authority.yml` as the final read-only lane authority

Implementation-only patch scripts and the write-enabled temporary workflow are absent from the final review state.

## Forbidden changes

- no SSI2164 footprint assignment;
- no OPA4196 footprint assignment;
- no OPA1679 package or decoupling changes;
- no Return limiter/clamp-diode exact-part selection;
- no top-level hierarchy or sheet-08 engineering changes;
- no PCB creation, placement or routing;
- no panel CAD or fabrication;
- no purchasing or production authority;
- no unrelated schematic changes;
- no merge without independent exact-head review.

## Expected electrical diff

1. Retain TMUX1574 safe selection and sheet-08 filtering unchanged.
2. Add one shared OPA4196 U63 across sheets 05 and 06.
3. Buffer the four local filtered control nodes at unity gain.
4. Add 20 Ω post-buffer isolation per channel.
5. Place 0 V / +3.3 V clamps after each buffer.
6. Preserve all four SSI2164 control-pin and channel assignments.
7. Add 100 nF local decoupling from each U63 supply pin to ground.
8. Update only the duplicate-reference validators so U60 and U63 are both recognised as intentional shared devices.
9. Repair only the mirrored native coordinates of U63 input, feedback, output and power labels after generation.
10. Make both authoritative wrappers invoke the same fail-closed U63 repair so regeneration is reproducible.
11. Accept exactly two serialised labels only at the proven coincident Memory and Ghost buffer-input junctions; all other exact-coordinate assertions remain unique.
12. Emit the project symbol library without tab-only or trailing-whitespace lines.

## Checks

```text
python tools/validate_ssi2164_buffer_lane.py
python tools/validate_memory_ghost_wet_capture.py
python tools/validate_current_schematic_stage.py
capture UUID-normalized committed sheets 05 and 06
regenerate sheets 05 and 06 from committed generators
git diff --check
prove every changed line is a KiCad UUID replacement
prove UUID-normalized regenerated content is exactly identical
rerun all three validators
KiCad 10 hierarchical ERC
```

The pinned schematic generator assigns fresh KiCad object UUIDs during full sheet regeneration. UUID values are therefore treated as serialization metadata, not semantic circuit content. Regeneration is accepted only when every non-UUID byte remains identical, UUID structure remains valid and unique, all validators pass, and hierarchical ERC remains at zero errors and zero warnings.

The lane validator must assert every U63 label at its exact physical pin coordinate on sheets 05 and 06, including explicit multiplicity for intentional coincident same-net labels.

## Stop rule

Stop immediately if:

- the exact SSI2164 VC voltage cannot be proven within the accepted range;
- the OPA4196 symbol or package identity is ambiguous;
- a U63 coordinate cannot be derived uniquely from the locked symbol geometry;
- the controlled generators, repair tool and generated sheets disagree;
- ERC or any existing validation fails;
- regeneration changes any UUID-normalized schematic content;
- regeneration produces a non-UUID diff line or duplicate UUID;
- an unlisted file must change;
- PCB, panel, purchasing or production authority would be required.
