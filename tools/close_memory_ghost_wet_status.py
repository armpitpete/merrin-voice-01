#!/usr/bin/env python3
"""Apply the accepted sheet-05 schematic-gate status to hardware documentation."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
README = ROOT / "README.md"
RETURN_VALIDATION = ROOT / "06_RETURN_BREAK_LIMITER_VALIDATION.md"
WET_VALIDATION = ROOT / "05_MEMORY_GHOST_WET_VALIDATION.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label} block, found {count}")
    return text.replace(old, new, 1)


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "05_MEMORY_GHOST_WET NEXT\nPCB WORK BLOCKED",
        "05_MEMORY_GHOST_WET COMPLETE / ERC VALIDATED\n"
        "07_OUTPUT_MUTE_PROTECTION NEXT\n"
        "PCB WORK BLOCKED",
        "current-status sheet-05 marker",
    )
    text = replace_once(
        text,
        "├── 05_MEMORY_GHOST_WET.kicad_sch       NEXT CAPTURE\n"
        "├── 06_RETURN_BREAK_LIMITER.kicad_sch   CAPTURED / ERC VALIDATED\n"
        "├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD",
        "├── 05_MEMORY_GHOST_WET.kicad_sch       CAPTURED / ERC VALIDATED\n"
        "├── 06_RETURN_BREAK_LIMITER.kicad_sch   CAPTURED / ERC VALIDATED\n"
        "├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch NEXT CAPTURE",
        "native-hierarchy sheet order",
    )
    text = replace_once(
        text,
        "- Sheet 06 may export only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`.\n",
        "- Sheet 06 may export only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`.\n"
        "- Sheet 05 consumes only the accepted Memory/Ghost DAC and SSI2164 control signals and exports only `WET_MIX`.\n"
        "- U60 is one physical SSI2164: units 1/2/4 are on sheet 05; units 3/5 are on sheet 06.\n",
        "locked-interface insertion point",
    )
    text = replace_once(
        text,
        "- measured SSI2164 control range after sheets 05 and 06 are integrated.",
        "- measured SSI2164 control range across the integrated sheet-05 and sheet-06 channels.",
        "controls open-item wording",
    )
    text = replace_once(
        text,
        "all five SSI2164 schematic units present",
        "single U60 device split across sheet 05 units 1/2/4 and sheet 06 units 3/5",
        "Return shared-device validation line",
    )
    text = replace_once(
        text,
        "- 30-minute worst-setting endurance test;\n"
        "- replacement of reserved SSI2164 units when sheet 05 is captured.",
        "- 30-minute worst-setting endurance test.",
        "obsolete Return reservation item",
    )

    wet_section = """## Captured sheet 05 — Memory / Ghost / Wet

Captured signal route:

```text
MEMORY_DAC → SSI2164 channel 1 → OPA1679 I/V ┐
                                               ├→ equal half-sum
GHOST_DAC  → SSI2164 channel 2 → OPA1679 I/V ┘
                                               ↓
                                    SSI2164 channel 4 wet master
                                               ↓
                                            WET_MIX
```

Locked shared-device ownership:

```text
U60 unit 1 = Memory channel 1   pins 2 IIN1, 3 VC1, 4 IOUT1
U60 unit 2 = Ghost channel 2    pins 7 IIN2, 6 VC2, 5 IOUT2
U60 unit 3 = Return channel 3   pins 15 IIN3, 14 VC3, 13 IOUT3   sheet 06
U60 unit 4 = wet-master channel pins 10 IIN4, 11 VC4, 12 IOUT4
U60 unit 5 = common power       sheet 06
```

Locked wet-sum relationship:

```text
Memory input resistor = 40.2 kΩ
Ghost input resistor  = 40.2 kΩ
feedback resistor     = 20.0 kΩ

branch magnitude = 20.0 / 40.2 ≈ 0.4975
two equal full-scale branches ≈ 0.995 total
```

Validation:

```text
native generation passed
hierarchy and WET_MIX-only export contract passed
SSI2164 symbol and official physical-pin contract passed
single-device five-unit U60 ownership contract passed
no duplicate SSI2164 physical device created
KiCad 10 hierarchical ERC passed
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
integrated Return workflow rerun passed with generation skipped
```

Still open:

- exact SSI2164 SOP-16 footprint and independent package-pin review;
- exact OPA1679 TSSOP-14 footprint review;
- exact coupling, stability and decoupling capacitor selections;
- measured Memory and Ghost VCA control laws;
- measured Memory/Ghost branch gain and wet-sum headroom;
- measured wet-master attenuation range, noise, distortion and recovery;
- integrated analogue loop gain and safety review;
- PCB placement, routing and all physical implementation gates.

"""
    text = replace_once(
        text,
        "## Captured sheet 04 — Input / Pressure / Absence\n",
        wet_section + "## Captured sheet 04 — Input / Pressure / Absence\n",
        "sheet-05 documentation insertion point",
    )
    text = replace_once(
        text,
        "captured sheets may not retain temporary interface-harness warnings\n```\n\n"
        "Remaining scaffold warnings are temporary and are not accepted permanent exceptions.",
        "captured sheets may not retain temporary interface-harness warnings\n```\n\n"
        "The integrated sheet-05 gate currently reports `0 errors, 0 warnings`. "
        "Temporary scaffold warnings are not accepted permanent exceptions.",
        "ERC current-stage statement",
    )
    text = replace_once(
        text,
        "[ ] 05_MEMORY_GHOST_WET        NEXT\n"
        "[ ] 07_OUTPUT_MUTE_PROTECTION",
        "[x] 05_MEMORY_GHOST_WET\n"
        "[ ] 07_OUTPUT_MUTE_PROTECTION  NEXT",
        "active capture order",
    )
    text = replace_once(
        text,
        "Sheet 05 must capture the Memory, Ghost and wet analogue paths, consume `MEMORY_DAC`, `GHOST_DAC`, and the three accepted SSI2164 control signals, replace the reserved SSI2164 channel placeholders currently held on sheet 06, and export only `WET_MIX`.",
        "Sheet 07 is the next bounded capture. It must consume `DIRECT_PRESENT`, `WET_MIX`, `HARDWARE_FAULT_N`, and the accepted ±12 V rails; implement the output summing, deterministic mute and output-protection path; and keep physical jack, footprint and panel decisions outside this schematic gate.",
        "next-sheet authority paragraph",
    )

    README.write_text(text, encoding="utf-8")


def update_return_validation() -> None:
    text = RETURN_VALIDATION.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "Pins `10/11/12` are channel 4 and are reserved for the later wet-master circuit on sheet 05.",
        "Pins `10/11/12` are channel 4 and are now used by the wet-master circuit on sheet 05.",
        "Return channel-4 status",
    )
    text = replace_once(
        text,
        "4. **Staged multi-unit SSI2164 handling**\n\n"
        "   KiCad ERC requires every unit of the physical multi-unit device to be placed. U60 units 1, 2 and 4 are therefore shown visibly as explicit no-connect reservations for sheet 05. They use the same `U60` reference and do not represent duplicate chips.\n\n"
        "   Sheet 05 must remove those reservations and connect the real Memory, Ghost and wet-master channels.",
        "4. **Integrated multi-unit SSI2164 ownership**\n\n"
        "   U60 remains one physical SSI2164. Sheet 05 owns units 1, 2 and 4 for Memory, Ghost and wet master. Sheet 06 owns unit 3 for Return and unit 5 for common power. All five units share reference and value `U60 / SSI2164`; no second physical device is created.",
        "Return multi-unit ownership section",
    )
    text = replace_once(
        text,
        "- all-five-unit staged placement check;",
        "- all-five-unit integrated ownership check across sheets 05 and 06;",
        "Return generated-gate ownership line",
    )
    text = replace_once(
        text,
        "- the symbol/pin and staged-unit contract against the committed native file;",
        "- the symbol/pin and integrated shared-unit contract against the committed native files;",
        "Return committed-rerun ownership line",
    )
    RETURN_VALIDATION.write_text(text, encoding="utf-8")


def write_wet_validation() -> None:
    WET_VALIDATION.write_text(
        """# 05_MEMORY_GHOST_WET — Validation Record

## Status

```text
GENERATED ARTIFACT: PASS
HIERARCHY / EXPORT CONTRACT: PASS
SSI2164 SYMBOL / PHYSICAL-PIN CONTRACT: PASS
SHARED MULTI-UNIT DEVICE CONTRACT: PASS
KICAD 10 HIERARCHICAL ERC: PASS — 0 ERRORS / 0 WARNINGS
COMMITTED-FILE RERUN: PASS — GENERATION SKIPPED
PCB / FOOTPRINT / MECHANICAL AUTHORITY: NOT GRANTED
```

## Locked sheet boundary

Inputs:

```text
RAIL_P12
RAIL_N12
MEMORY_DAC
GHOST_DAC
VCA_MEMORY_CTRL
VCA_GHOST_CTRL
VCA_WET_CTRL
```

Only this signal may leave sheet 05:

```text
WET_MIX
```

Memory, Ghost, wet-sum, SSI2164 current and control-filter nodes remain local.

## Shared SSI2164 ownership

`U60` is one physical five-unit device shared by sheets 05 and 06:

```text
unit 1 — Memory channel 1:    pin 2 IIN1, pin 3 VC1, pin 4 IOUT1
unit 2 — Ghost channel 2:     pin 7 IIN2, pin 6 VC2, pin 5 IOUT2
unit 3 — Return channel 3:    pin 15 IIN3, pin 14 VC3, pin 13 IOUT3 — sheet 06
unit 4 — wet-master channel:  pin 10 IIN4, pin 11 VC4, pin 12 IOUT4
unit 5 — common power:         MODE/GND/V−/V+ — sheet 06
```

The native validator requires exactly five SSI2164 unit instances across all sheets, references all equal to `U60`, values all equal to `SSI2164`, units exactly `1..5`, and no accepted footprint.

## Captured analogue path

Memory and Ghost each use:

```text
10 µF AC coupling
20 kΩ SSI2164 input resistor
220 Ω / 1.2 nF stability network
1 kΩ / 100 nF control isolation and filtering
20 kΩ / 100 pF OPA1679 current-to-voltage stage
```

Their outputs enter an equal inverting sum:

```text
R_MEMORY = 40.2 kΩ
R_GHOST  = 40.2 kΩ
R_FB     = 20.0 kΩ

per-branch magnitude = 20.0 / 40.2 ≈ 0.4975
combined equal full-scale magnitude ≈ 0.995
```

The sum is AC-coupled through SSI2164 channel 4, converted by the final OPA1679 stage, isolated by `47 Ω`, and exported as `WET_MIX`.

## Generator-boundary repairs

The pinned schematic API mirrors Y coordinates returned for pins in the project-local multi-unit SSI2164 symbol. Exact post-generation repairs move only the nine sheet-05 and six sheet-06 SSI2164 attachments to their actual native KiCad pin coordinates.

The same API accepts but does not serialise the hierarchical-label shape argument. Exact named post-generation repairs set only:

```text
WET_MIX = output
RETURN_LIMITED = output
RETURN_FEED = output
ABSENCE_INFLUENCE = output
```

Both repairs fail closed if an expected named label or coordinate is missing or duplicated.

## First passing artifact

The dedicated sheet-05 workflow passed:

- native sheet-05 and integrated sheet-06 generation;
- exact hierarchy-direction checks;
- official SSI2164 symbol and physical-pin mapping;
- units `1/2/4` on sheet 05 and units `3/5` on sheet 06;
- one-reference, one-value, no-duplicate-device enforcement;
- equal half-sum resistor and gain contract;
- KiCad CLI `10.0.4` hierarchical ERC;
- strict captured-sheet warning policy.

ERC result:

```text
0 errors
0 warnings
```

Only that passing native artifact was promoted in commit `917b98a`.

## Committed-file rerun

The follow-up workflow detected `05_MEMORY_GHOST_WET_CAPTURED` and skipped:

```text
generation
physical-coordinate repair
output-direction repair
promotion
```

It then passed the same native contract validator, KiCad 10 hierarchical ERC, and strict warning policy directly against committed files. The integrated Return workflow independently skipped Return generation and passed its shared-U60 ownership and ERC gates.

`05_MEMORY_GHOST_WET` is closed at schematic-capture level. Exact packages, footprints, physical placement, measured gain/control law, noise, distortion, loop safety and endurance remain later independent gates.
""",
        encoding="utf-8",
    )


def main() -> None:
    update_readme()
    update_return_validation()
    write_wet_validation()
    print("Updated sheet-05 and integrated Return hardware status documentation")


if __name__ == "__main__":
    main()
