#!/usr/bin/env python3
"""Close the accepted sheet-07 gate in the hardware README."""

from __future__ import annotations

from pathlib import Path

README = Path("hardware/memory-core-prototype-a/README.md")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one README match, found {count}: {old[:80]!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = README.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "05_MEMORY_GHOST_WET COMPLETE / ERC VALIDATED\n"
        "07_OUTPUT_MUTE_PROTECTION NEXT\n"
        "PCB WORK BLOCKED",
        "05_MEMORY_GHOST_WET COMPLETE / ERC VALIDATED\n"
        "07_OUTPUT_MUTE_PROTECTION COMPLETE / ERC VALIDATED\n"
        "09_TEST_SERVICE NEXT\n"
        "PCB WORK BLOCKED",
    )

    text = replace_once(
        text,
        "├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch NEXT CAPTURE\n"
        "├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED\n"
        "└── 09_TEST_SERVICE.kicad_sch           INTERFACE SCAFFOLD",
        "├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch CAPTURED / ERC VALIDATED\n"
        "├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED\n"
        "└── 09_TEST_SERVICE.kicad_sch           NEXT CAPTURE",
    )

    text = replace_once(
        text,
        "- U60 is one physical SSI2164: units 1/2/4 are on sheet 05; units 3/5 are on sheet 06.\n",
        "- U60 is one physical SSI2164: units 1/2/4 are on sheet 05; units 3/5 are on sheet 06.\n"
        "- U32 is one physical OPA1679: units 1/5 are on sheet 03; units 2/3/4 are on sheet 07.\n"
        "- Sheet 07 consumes only `DIRECT_PRESENT`, `WET_MIX`, `HARDWARE_FAULT_N` and the accepted ±12 V rails.\n"
        "- Sheet 07 exports no hierarchical audio or control net; the protected output jack remains local.\n",
    )

    output_section = """## Captured sheet 07 — Output / Mute / Protection

Captured signal route:

```text
DIRECT_PRESENT ─40.2 kΩ─┐
                         ├─ U32B equal half-sum
WET_MIX       ─40.2 kΩ─┘        ↓
                         passive output level
                                ↓
                         U32C level buffer
                                ↓
                         fail-muted JFET shunt
                                ↓
                         U32D post-mute driver
                                ↓
                         AC coupling + output protection
                                ↓
                         logical WQP518MA mono output
```

Locked output relationship:

```text
Direct input resistor = 40.2 kΩ
Wet input resistor    = 40.2 kΩ
feedback resistor     = 20.0 kΩ

per-branch magnitude = 20.0 / 40.2 ≈ 0.4975
6 Vpp Direct + 6 Vpp Wet calculated maximum ≈ 5.97 Vpp
passive output level can only attenuate
```

Locked shared-device ownership:

```text
U32 unit 1 = Return converter A — sheet 03
U32 unit 2 = final half-sum B — sheet 07
U32 unit 3 = output-level buffer C — sheet 07
U32 unit 4 = post-mute driver D — sheet 07
U32 unit 5 = common power — sheet 03
```

Fail-muted control:

```text
fault or undefined HARDWARE_FAULT_N → optocoupler on → MUTE_GATE toward 0 V → shunt mute on
healthy HARDWARE_FAULT_N → optocoupler off → MUTE_GATE toward −10.91 V
healthy release time constant ≈ 90.9 ms
first-pass 50% CTR fault-clamp estimate ≈ 12.7 ms
```

Validation:

```text
native sheet-03 / sheet-07 generation passed
no-export hierarchy contract passed
shared five-unit U32 ownership and official-pin contract passed
seven physical OPA1679 package allocation passed
Direct/Wet gain and calculated output-headroom contract passed
fail-muted control and first-pass timing contract passed
provisional control symbols use explicit logical pins and blank footprints
logical WQP518MA output boundary passed
KiCad 10 hierarchical ERC passed
0 ERC errors
0 ERC warnings
committed-file rerun passed with generation and promotion skipped
```

Still open:

- exact OPA1679 TSSOP-14 footprint review;
- exact J113-class mute device, pin map, footprint and `VGS(off)` spread;
- exact optocoupler and NPN fault-inverter parts and packages;
- exact output-level potentiometer and WQP518MA physical pin/footprint review;
- panel alignment and jack clearance;
- measured output level, load drive, noise and distortion;
- measured mute depth, fault timing, release timing and pop behaviour;
- measured output-protection current and 30-minute endurance;
- all PCB placement, routing and physical implementation gates.

"""
    text = replace_once(
        text,
        "## Captured sheet 04 — Input / Pressure / Absence\n",
        output_section + "## Captured sheet 04 — Input / Pressure / Absence\n",
    )

    text = replace_once(
        text,
        "The integrated sheet-05 gate currently reports `0 errors, 0 warnings`. Temporary scaffold warnings are not accepted permanent exceptions.",
        "The integrated sheet-07 gate and current-stage authority gate report `0 errors, 0 warnings`. Temporary scaffold warnings are not accepted permanent exceptions.",
    )

    text = replace_once(
        text,
        "[x] 05_MEMORY_GHOST_WET\n"
        "[ ] 07_OUTPUT_MUTE_PROTECTION  NEXT\n"
        "[ ] 09_TEST_SERVICE",
        "[x] 05_MEMORY_GHOST_WET\n"
        "[x] 07_OUTPUT_MUTE_PROTECTION\n"
        "[ ] 09_TEST_SERVICE             NEXT",
    )

    text = replace_once(
        text,
        "Sheet 07 is the next bounded capture. It must consume `DIRECT_PRESENT`, `WET_MIX`, `HARDWARE_FAULT_N`, and the accepted ±12 V rails; implement the output summing, deterministic mute and output-protection path; and keep physical jack, footprint and panel decisions outside this schematic gate.",
        "Sheet 09 is the next bounded capture. It must replace the temporary service harness with the accepted test-point, connector, service-mode, reset/clear and safe-mute access circuitry while keeping production connector, footprint, fixture and panel decisions outside this schematic gate.",
    )

    README.write_text(text, encoding="utf-8")
    print("Closed sheet 07 in hardware README; advanced active capture to sheet 09")


if __name__ == "__main__":
    main()
