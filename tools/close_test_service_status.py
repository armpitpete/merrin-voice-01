#!/usr/bin/env python3
"""Close the accepted sheet-09 gate in the hardware README."""

from __future__ import annotations

from pathlib import Path

README = Path("hardware/memory-core-prototype-a/README.md")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one README match, found {count}: {old[:100]!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = README.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "07_OUTPUT_MUTE_PROTECTION COMPLETE / ERC VALIDATED\n"
        "09_TEST_SERVICE NEXT\n"
        "PCB WORK BLOCKED",
        "07_OUTPUT_MUTE_PROTECTION COMPLETE / ERC VALIDATED\n"
        "09_TEST_SERVICE COMPLETE / ERC VALIDATED\n"
        "00_TOP FINAL INTEGRATED REVIEW NEXT\n"
        "PCB WORK BLOCKED",
    )

    text = replace_once(
        text,
        "├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED\n"
        "└── 09_TEST_SERVICE.kicad_sch           NEXT CAPTURE",
        "├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED\n"
        "└── 09_TEST_SERVICE.kicad_sch           CAPTURED / ERC VALIDATED",
    )

    text = replace_once(
        text,
        "- Sheet 07 exports no hierarchical audio or control net; the protected output jack remains local.\n",
        "- Sheet 07 exports no hierarchical audio or control net; the protected output jack remains local.\n"
        "- Sheet 09 consumes eight accepted read-only service signals and exports no hierarchy net.\n"
        "- `SERVICE_TEST`, `RESET_CLEAR`, and `SAFE_MUTE` remain operating signals between sheets 08 and 02, not sheet-09 service commands.\n",
    )

    section = """## Captured sheet 09 — Test / Service

Captured read-only access:

```text
RAIL_3V3          → 1 kΩ probe isolation
HARDWARE_FAULT_N  → 47 kΩ probe isolation
SHAPED_PRESENT    → 22 kΩ probe isolation
ADC_ANALOG_IN     → 22 kΩ probe isolation
RETURN_LIMITED    → 22 kΩ probe isolation
RETURN_FEED       → 22 kΩ probe isolation
ABSENCE_INFLUENCE → 22 kΩ probe isolation
WET_MIX           → 22 kΩ probe isolation
```

The isolated probe nodes feed individual test points `TP900` through `TP907`. `TP908` provides service ground. A logical ten-position header or pad grouping provides the eight probe nodes plus two grounds; it has no accepted footprint.

Locked hierarchy boundary:

```text
inputs:  RAIL_3V3, HARDWARE_FAULT_N, SHAPED_PRESENT, ADC_ANALOG_IN,
         RETURN_LIMITED, RETURN_FEED, ABSENCE_INFLUENCE, WET_MIX
outputs: none
```

First-pass isolation calculations:

```text
3.3 V through 1 kΩ short limit ≈ 3.3 mA
3.3 V through 47 kΩ ≈ 70.2 µA
22 kΩ into a 10 MΩ instrument adds approximately 0.22% loading
```

Validation:

```text
native read-only service capture passed
eight-input / no-output hierarchy contract passed
eight probe branches and nine test points passed
logical ten-position service header pin map passed
blank connector-footprint boundary passed
former temporary interface harness removed
KiCad 10 hierarchical ERC passed across all nine sheets
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
```

Still open:

- exact service connector or pad format;
- production fixture architecture;
- test-point footprints and access clearances;
- current-measurement links for major power branches;
- measured probe loading and fault-injection limits;
- all PCB placement, routing and mechanical implementation gates.

"""
    text = replace_once(
        text,
        "## Captured sheet 04 — Input / Pressure / Absence\n",
        section + "## Captured sheet 04 — Input / Pressure / Absence\n",
    )

    text = replace_once(
        text,
        "The integrated sheet-07 gate and current-stage authority gate report `0 errors, 0 warnings`. Temporary scaffold warnings are not accepted permanent exceptions.",
        "All nine component sheets now report `0 errors, 0 warnings` from committed files. No temporary scaffold warning remains accepted.",
    )

    text = replace_once(
        text,
        "[x] 07_OUTPUT_MUTE_PROTECTION\n"
        "[ ] 09_TEST_SERVICE             NEXT\n"
        "[ ] 00_TOP final interface and ERC review",
        "[x] 07_OUTPUT_MUTE_PROTECTION\n"
        "[x] 09_TEST_SERVICE\n"
        "[ ] 00_TOP final interface and ERC review  NEXT",
    )

    text = replace_once(
        text,
        "Sheet 09 is the next bounded capture. It must replace the temporary service harness with the accepted test-point, connector, service-mode, reset/clear and safe-mute access circuitry while keeping production connector, footprint, fixture and panel decisions outside this schematic gate.",
        "All nine component sheets are captured. The next bounded lane is the final `00_TOP` integrated review: reconcile parent and child interfaces, confirm no temporary harness remains, revalidate shared-device ownership and restricted boundaries, run KiCad 10 ERC from committed files, and document remaining risks without entering PCB or footprint work.",
    )

    README.write_text(text, encoding="utf-8")
    print("Closed sheet 09 in hardware README; advanced active lane to 00_TOP final review")


if __name__ == "__main__":
    main()
