#!/usr/bin/env python3
"""Apply the bounded SSI2164 OPA4196 buffered-control patch.

This script is temporary. It fails closed on the exact pre-patch Git blob hashes
and performs only the files listed in SSI2164_BUFFER_EDIT_CONTRACT.md.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")

EXPECTED_BLOBS = {
    Path("tools/capture_memory_ghost_wet_sheet.py"): "7291b90be6793f2b0ec73e2378410e076e1e4e3e",
    Path("tools/capture_return_break_limiter_sheet.py"): "0be8a7ab89d3625a3146d3819940000731e7804d",
    Path("tools/validate_memory_ghost_wet_capture.py"): "e932231003d1f41e59d685e07ffb4356e5809b75",
    Path(".github/workflows/kicad-return-sheet-erc.yml"): "d27294e35f3c89b41a04f63a86faee9d5fc7c9b1",
    Path("docs/v5.2-ssi2164-mcp4728-fail-safe-control.md"): "7e706862e839383b8d80d8d6b010e809ca352e9e",
    Path("docs/v5.2-power-current-and-thermal-budget.md"): "1108589c0c4ac000c61b3e7b520d156b8c7b4a53",
    Path("docs/v5.2-return-limiter-and-opamp-allocation.md"): "857d4f3ae6094edd02401875752641877eafa0ec",
    ROOT / "MerrinLab_PrototypeA.kicad_sym": "71b291b78a5b08aeade53f7690391e80287f4d58",
    ROOT / "05_MEMORY_GHOST_WET.kicad_sch": "3031f5b0a19347185fb492e337b02e74676e44e2",
    ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch": "9e20d701e17b9b5dab84c54acfddb70ef4d339ff",
    ROOT / "05_MEMORY_GHOST_WET_VALIDATION.md": "61f3e63c5ee55c4ee61fdecad3c109cc27c51722",
    ROOT / "06_RETURN_BREAK_LIMITER_VALIDATION.md": "6537fe59825fb89352763b0b245da10de7ef8d73",
    ROOT / "08_CONTROLS_STATE.kicad_sch": "2d681089ed95fada6f476060cb6163311a3fde45",
    ROOT / "MerrinGriefSynthMemoryCoreA.kicad_sch": "8ef352f7a72197214e34dacdf998046382589937",
    Path("tools/capture_controls_state_sheet.py"): "0485f51b3c78ab95aa8b8f94d01b8aeedc73d188",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def assert_sources() -> None:
    for path, expected in EXPECTED_BLOBS.items():
        actual = git_blob(path)
        if actual != expected:
            raise RuntimeError(f"Unexpected source blob for {path}: {actual} != {expected}")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match in {path}, found {count}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, marker: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    if addition.strip() in text:
        raise RuntimeError(f"Addition already present in {path}")
    if marker not in text:
        raise RuntimeError(f"Marker missing in {path}: {marker!r}")
    path.write_text(text.replace(marker, addition + marker, 1), encoding="utf-8")


def patch_return_generator() -> None:
    path = Path("tools/capture_return_break_limiter_sheet.py")
    old = '''    out.append("\\t)\\n")
    return "".join(out)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    if '(symbol "SSI2164S_MULTI"' not in text:
        additions.append(render_ssi2164_multi_symbol())
'''
    new = '''    out.append("\\t)\\n")
    return "".join(out)


def render_opa4196_multi_symbol() -> str:
    name = "OPA4196_PW_MULTI"
    units = {
        1: (
            helpers.SymbolPin("3", "+IN_A", "input", "left", 1),
            helpers.SymbolPin("2", "-IN_A", "input", "left", 3),
            helpers.SymbolPin("1", "OUT_A", "output", "right", 2),
        ),
        2: (
            helpers.SymbolPin("5", "+IN_B", "input", "left", 1),
            helpers.SymbolPin("6", "-IN_B", "input", "left", 3),
            helpers.SymbolPin("7", "OUT_B", "output", "right", 2),
        ),
        3: (
            helpers.SymbolPin("10", "+IN_C", "input", "left", 1),
            helpers.SymbolPin("9", "-IN_C", "input", "left", 3),
            helpers.SymbolPin("8", "OUT_C", "output", "right", 2),
        ),
        4: (
            helpers.SymbolPin("12", "+IN_D", "input", "left", 1),
            helpers.SymbolPin("13", "-IN_D", "input", "left", 3),
            helpers.SymbolPin("14", "OUT_D", "output", "right", 2),
        ),
        5: (
            helpers.SymbolPin("11", "V-", "power_in", "left", 3),
            helpers.SymbolPin("4", "V+", "power_in", "right", 2),
        ),
    }
    out = [
        f'\\t(symbol "{name}"\\n',
        "\\t\\t(exclude_from_sim no)\\n",
        "\\t\\t(in_bom yes)\\n",
        "\\t\\t(on_board yes)\\n",
        _property("Reference", "U", 11.43),
        _property("Value", name, -11.43),
        _property("Footprint", "", 0, True),
        _property("Datasheet", "https://www.ti.com/lit/ds/symlink/opa4196.pdf", 0, True),
        _property(
            "Description",
            "OPA4196 quad low-power rail-to-rail op amp; five-unit control-buffer symbol; PW TSSOP-14 pin map",
            0,
            True,
        ),
    ]
    for unit, pins in units.items():
        out.append(_render_ssi_unit(name, unit, pins))
    out.append("\\t)\\n")
    return "".join(out)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    if '(symbol "SSI2164S_MULTI"' not in text:
        additions.append(render_ssi2164_multi_symbol())
    if '(symbol "OPA4196_PW_MULTI"' not in text:
        additions.append(render_opa4196_multi_symbol())
'''
    replace_once(path, old, new)

    old = '''    no_connect_component_pin(sch, ssi_power, "1")  # MODE open = Class AB.

    # Correct sheet-03's ~0.747 receiver to ~0.249 before the Return VCA.
'''
    new = '''    no_connect_component_pin(sch, ssi_power, "1")  # MODE open = Class AB.

    return_buffer = add_part(
        sch,
        "MerrinLab_PrototypeA:OPA4196_PW_MULTI",
        "U63",
        "OPA4196 CONTROL BUFFER",
        (139.70, 114.30),
        unit=3,
    )
    buffer_power = add_part(
        sch,
        "MerrinLab_PrototypeA:OPA4196_PW_MULTI",
        "U63",
        "OPA4196 CONTROL BUFFER",
        (139.70, 160.02),
        unit=5,
    )
    label_component_pin(sch, buffer_power, "4", "RAIL_P12")
    label_component_pin(sch, buffer_power, "11", "RAIL_N12")

    # Correct sheet-03's ~0.747 receiver to ~0.249 before the Return VCA.
'''
    replace_once(path, old, new)

    old = '''    # Return control remains in the attenuation-only 0–3.3 V range.
    add_two_pin(sch, "Device:R", "R604", "1k control isolate", (76.20, 114.30), "VCA_RETURN_CTRL", "SSI_VC3", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D600", "SSI_VC3", (91.44, 111.76))
    add_lower_clamp(sch, "D601", "SSI_VC3", (91.44, 116.84))
'''
    new = '''    # Return control is filtered, buffered at unity, isolated by 20 ohm, then clamped.
    add_two_pin(sch, "Device:R", "R604", "1k pre-buffer filter", (76.20, 114.30), "VCA_RETURN_CTRL", "RETURN_CTRL_BUFFER_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C602", "100nF control filter", (88.90, 121.92), "RETURN_CTRL_BUFFER_IN", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_component_pin(sch, return_buffer, "10", "RETURN_CTRL_BUFFER_IN")
    label_component_pin(sch, return_buffer, "9", "RETURN_CTRL_BUFFER_OUT")
    label_component_pin(sch, return_buffer, "8", "RETURN_CTRL_BUFFER_OUT")
    add_two_pin(sch, "Device:R", "R604A", "20R buffer isolate", (101.60, 114.30), "RETURN_CTRL_BUFFER_OUT", "SSI_VC3", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D600", "SSI_VC3", (114.30, 111.76))
    add_lower_clamp(sch, "D601", "SSI_VC3", (114.30, 116.84))
'''
    replace_once(path, old, new)

    old = '''    add_two_pin(sch, "Device:C", "C618", "100nF SSI + rail", (137.16, 139.70), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C619", "100nF SSI - rail", (149.86, 139.70), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
'''
    new = '''    add_two_pin(sch, "Device:C", "C618", "100nF SSI + rail", (137.16, 139.70), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C619", "100nF SSI - rail", (149.86, 139.70), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C642", "100nF OPA4196 + rail", (162.56, 139.70), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C643", "100nF OPA4196 - rail", (175.26, 139.70), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
'''
    replace_once(path, old, new)


def patch_memory_generator() -> None:
    path = Path("tools/capture_memory_ghost_wet_sheet.py")
    old = '''def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_hier(sch, name, position, shape, end):
'''
    new = '''def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_upper_clamp(sch, reference, signal, position):
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class upper clamp", position, "RAIL_3V3", signal)


def add_lower_clamp(sch, reference, signal, position):
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class lower clamp", position, signal, "GND")


def add_hier(sch, name, position, shape, end):
'''
    replace_once(path, old, new)

    old = '''    wet = add_part(
        sch,
        SSI_LIBRARY_ID,
        SSI_REFERENCE,
        "SSI2164 — WET MASTER CH4",
        (276.86, 111.76),
        unit=4,
    )

    for component, unit, prefix, position in (
'''
    new = '''    wet = add_part(
        sch,
        SSI_LIBRARY_ID,
        SSI_REFERENCE,
        "SSI2164 — WET MASTER CH4",
        (276.86, 111.76),
        unit=4,
    )
    memory_buffer = add_part(
        sch, "MerrinLab_PrototypeA:OPA4196_PW_MULTI", "U63", "OPA4196 CONTROL BUFFER", (101.60, 111.76), unit=1
    )
    ghost_buffer = add_part(
        sch, "MerrinLab_PrototypeA:OPA4196_PW_MULTI", "U63", "OPA4196 CONTROL BUFFER", (101.60, 165.10), unit=2
    )
    wet_buffer = add_part(
        sch, "MerrinLab_PrototypeA:OPA4196_PW_MULTI", "U63", "OPA4196 CONTROL BUFFER", (261.62, 157.48), unit=4
    )

    for component, unit, prefix, position in (
'''
    replace_once(path, old, new)

    replacements = [
        (
'''    add_two_pin(sch, "Device:R", "R502", "1k control isolate", (76.20, 111.76), "VCA_MEMORY_CTRL", "SSI_VC1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C502", "100nF control filter", (91.44, 111.76), "SSI_VC1", "GND", "Capacitor_SMD:C_0805_2012Metric")
''',
'''    add_two_pin(sch, "Device:R", "R502", "1k pre-buffer filter", (76.20, 111.76), "VCA_MEMORY_CTRL", "MEM_CTRL_BUFFER_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C502", "100nF control filter", (91.44, 111.76), "MEM_CTRL_BUFFER_IN", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_component_pin(sch, memory_buffer, "3", "MEM_CTRL_BUFFER_IN")
    label_component_pin(sch, memory_buffer, "2", "MEM_CTRL_BUFFER_OUT")
    label_component_pin(sch, memory_buffer, "1", "MEM_CTRL_BUFFER_OUT")
    add_two_pin(sch, "Device:R", "R525", "20R buffer isolate", (106.68, 111.76), "MEM_CTRL_BUFFER_OUT", "SSI_VC1", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D500", "SSI_VC1", (116.84, 109.22))
    add_lower_clamp(sch, "D501", "SSI_VC1", (116.84, 114.30))
'''),
        (
'''    add_two_pin(sch, "Device:R", "R506", "1k control isolate", (76.20, 165.10), "VCA_GHOST_CTRL", "SSI_VC2", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C506", "100nF control filter", (91.44, 165.10), "SSI_VC2", "GND", "Capacitor_SMD:C_0805_2012Metric")
''',
'''    add_two_pin(sch, "Device:R", "R506", "1k pre-buffer filter", (76.20, 165.10), "VCA_GHOST_CTRL", "GHOST_CTRL_BUFFER_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C506", "100nF control filter", (91.44, 165.10), "GHOST_CTRL_BUFFER_IN", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_component_pin(sch, ghost_buffer, "5", "GHOST_CTRL_BUFFER_IN")
    label_component_pin(sch, ghost_buffer, "6", "GHOST_CTRL_BUFFER_OUT")
    label_component_pin(sch, ghost_buffer, "7", "GHOST_CTRL_BUFFER_OUT")
    add_two_pin(sch, "Device:R", "R526", "20R buffer isolate", (106.68, 165.10), "GHOST_CTRL_BUFFER_OUT", "SSI_VC2", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D502", "SSI_VC2", (116.84, 162.56))
    add_lower_clamp(sch, "D503", "SSI_VC2", (116.84, 167.64))
'''),
        (
'''    add_two_pin(sch, "Device:R", "R522", "1k control isolate", (261.62, 157.48), "VCA_WET_CTRL", "SSI_VC4", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C522", "100nF control filter", (276.86, 157.48), "SSI_VC4", "GND", "Capacitor_SMD:C_0805_2012Metric")
''',
'''    add_two_pin(sch, "Device:R", "R522", "1k pre-buffer filter", (246.38, 157.48), "VCA_WET_CTRL", "WET_CTRL_BUFFER_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C522", "100nF control filter", (256.54, 165.10), "WET_CTRL_BUFFER_IN", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_component_pin(sch, wet_buffer, "12", "WET_CTRL_BUFFER_IN")
    label_component_pin(sch, wet_buffer, "13", "WET_CTRL_BUFFER_OUT")
    label_component_pin(sch, wet_buffer, "14", "WET_CTRL_BUFFER_OUT")
    add_two_pin(sch, "Device:R", "R527", "20R buffer isolate", (276.86, 157.48), "WET_CTRL_BUFFER_OUT", "SSI_VC4", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D504", "SSI_VC4", (287.02, 154.94))
    add_lower_clamp(sch, "D505", "SSI_VC4", (287.02, 160.02))
'''),
    ]
    for old, new in replacements:
        replace_once(path, old, new)

    old = '''        "U60 units 3 and 5 remain on sheet 06; no second SSI2164 is created.",
'''
    new = '''        "U60 units 3 and 5 remain on sheet 06; no second SSI2164 is created.\\n"
        "U63 OPA4196 units 1/2/4 buffer Memory/Ghost/Wet; units 3/5 remain on sheet 06.",
'''
    replace_once(path, old, new)


def patch_validators() -> None:
    path = Path("tools/validate_memory_ghost_wet_capture.py")
    replace_once(
        path,
        '''def assert_unique_references(rows: list[dict[str, object]], multi_ref: str) -> None:
''',
        '''def assert_unique_references(rows: list[dict[str, object]], multi_refs: set[str]) -> None:
''',
    )
    replace_once(
        path,
        '''        if count > 1 and reference != multi_ref
''',
        '''        if count > 1 and reference not in multi_refs
''',
    )
    replace_once(path, 'assert_unique_references(rows05, "U60")', 'assert_unique_references(rows05, {"U60", "U63"})')
    replace_once(path, 'assert_unique_references(rows06, "U60")', 'assert_unique_references(rows06, {"U60", "U63"})')

    workflow = Path(".github/workflows/kicad-return-sheet-erc.yml")
    replace_once(
        workflow,
        "if count > 1 and reference != 'U60'",
        "if count > 1 and reference not in {'U60', 'U63'}",
    )


def patch_docs() -> None:
    control = Path("docs/v5.2-ssi2164-mcp4728-fail-safe-control.md")
    replace_once(control, "Draft for acceptance before native schematic capture.", "Corrected buffered-control authority for exact-part review.")
    replace_once(
        control,
        "Each SSI control input must include current limiting and clamping appropriate to the selected analogue switch and DAC domains.",
        "Each SSI control input uses a local high-impedance OPA4196 unity buffer, a 20 ohm post-buffer isolation resistor, and post-buffer clamps to prevent negative or overrange control voltage.",
    )
    replace_once(control, "Dx  = SSI2164 control input", "Dx  = local filtered OPA4196 buffer input")
    section = '''\n# Corrected local control buffers\n\nThe former unbuffered path placed approximately 3 kΩ in series with the SSI2164 nominal 10 kΩ control input and could only deliver approximately 2.54 V from a 3.3 V request. That implementation is rejected.\n\nOne OPA4196 quad buffer is shared across sheets 05 and 06 as `U63`:\n\n```text\nunit 1 = Memory VC1 buffer\nunit 2 = Ghost VC2 buffer\nunit 3 = Return VC3 buffer\nunit 4 = wet-master VC4 buffer\nunit 5 = protected +/-12 V common power\n```\n\nEach channel uses the existing high-impedance 1 kΩ / capacitor pre-buffer filter, a unity follower, a 20 Ω output-isolation resistor and post-buffer 0 V / +3.3 V clamps. The OPA4196 footprint remains blank pending exact footprint review.\n\nAt the lowest specified SSI2164 control-port impedance and nominal 3.3 V reference:\n\n```text\nVC = 3.3 V × 9 kΩ / (9 kΩ + 20 Ω)\n   = 3.2927 V\nattenuation ≈ 3.2927 / 0.033\n            ≈ 99.8 dB\n```\n\nUsing the current resistor-only lower 3.3 V rail estimate of 3.244 V gives approximately 98.1 dB attenuation. Regulator-reference tolerance remains part of the later rail acceptance calculation; the series-loading defect is closed.\n\nThe OPA4196 is powered from protected +/-12 V so 0 V remains a true mid-rail unity command. It is not part of the seven-package OPA1679 audio allocation.\n\n'''
    append_once(control, "# Release sequence\n", section)

    power = Path("docs/v5.2-power-current-and-thermal-budget.md")
    old = '''## SSI2164

One SSI2164 in Class AB mode:

```text
typical approximately ±6 mA
maximum approximately ±8 mA
```

## Analogue-core allowance

```text
78.4 mA OPA1679 worst case
+ 8.0 mA SSI2164 maximum
= 86.4 mA per rail

locked allowance = 100 mA per rail
```

The remaining approximately 13.6 mA per rail covers references, clamps and small analogue support devices. Exceeding it reopens the budget.
'''
    new = '''## SSI2164

One SSI2164 in Class AB mode:

```text
typical approximately ±6 mA
maximum approximately ±8 mA
```

## OPA4196 SSI control buffer

One OPA4196 quad buffer on protected +/-12 V:

```text
typical = 4 × 0.140 mA = 0.56 mA per rail
worst design value = 4 × 0.250 mA = 1.00 mA per rail
```

This package is separate from the seven OPA1679 audio packages.

## Analogue-core allowance

```text
78.4 mA OPA1679 worst case
+ 8.0 mA SSI2164 maximum
+ 1.0 mA OPA4196 design maximum
= 87.4 mA per rail

locked allowance = 100 mA per rail
```

The remaining approximately 12.6 mA per rail covers references, clamps and small analogue support devices. Exceeding it reopens the budget.
'''
    replace_once(power, old, new)

    allocation = Path("docs/v5.2-return-limiter-and-opamp-allocation.md")
    addition = '''\n# OPA4196 SSI-control buffer allocation\n\nThe seven-package, 28-channel OPA1679 audio allocation remains unchanged and fully occupied. SSI2164 control buffering uses one separate OPA4196 quad package:\n\n```text\nchannel A = Memory control\nchannel B = Ghost control\nchannel C = Return control\nchannel D = wet-master control\n```\n\nThe OPA4196 is powered from protected +/-12 V, configured as four unity followers, locally bypassed with 100 nF per supply pin and isolated from the SSI2164 control inputs by 20 Ω per channel. Its footprint remains blank pending exact package/land-pattern review.\n\n'''
    append_once(allocation, "# Required test points\n", addition)

    for path in (ROOT / "05_MEMORY_GHOST_WET_VALIDATION.md", ROOT / "06_RETURN_BREAK_LIMITER_VALIDATION.md"):
        text = path.read_text(encoding="utf-8")
        text += '''\n\n## SSI2164 buffered-control amendment\n\nThe accepted sheet now includes the relevant units of shared `U63 / OPA4196 CONTROL BUFFER`. The OPA4196 presents a high-impedance load to the existing control filter and drives the SSI2164 VC pin through 20 Ω with post-buffer 0 V / +3.3 V clamps. The OPA4196 and SSI2164 footprints remain blank; PCB and mechanical authority are not granted.\n'''
        path.write_text(text, encoding="utf-8")


def write_authority_files() -> None:
    review = '''# SSI2164 buffered-control review\n\n## Decision\n\n```text\nCONTROL-PORT LOADING DEFECT       CORRECTED\nBUFFER                            OPA4196 PW / TSSOP-14 TARGET\nSHARED REFERENCE                  U63\nUNITS 1/2/4                       SHEET 05\nUNITS 3/5                         SHEET 06\nNOMINAL 3.3 V ATTENUATION         99.8 dB\nLOW RAIL / 9 kΩ CALCULATION       98.1 dB\nSSI2164 PACKAGE                   PSL16 / JEDEC MS-012-AC\nSSI2164 FOOTPRINT                 BLANK\nOPA4196 FOOTPRINT                 BLANK\nPCB / PANEL / PURCHASING          BLOCKED\n```\n\n## Primary-source basis\n\nThe SSI2164 manufacturer specifies a nominal 10 kΩ control-port impedance with a 9–11 kΩ range, a -33 mV/dB control constant and 3.3 V for approximately -100 dB attenuation. The SSI2164 orderable package is `SSI2164S-TU` or `SSI2164S-RT`, package ID `PSL16`, compliant with JEDEC MS-012-AC.\n\nTexas Instruments specifies the OPA4196 for 4.5–36 V operation, rail-to-rail input/output, 140 µA typical quiescent current per channel, unity-gain capacitive-load operation and PW TSSOP-14 availability. TI recommends 0.1 µF local supply bypass and 10–20 Ω output isolation for capacitive loads.\n\n## Remaining gates\n\n- exact SSI2164 and OPA4196 land-pattern review;\n- exact post-buffer clamp-diode selection;\n- regulator-reference tolerance in the complete attenuation bound;\n- bench measurement of unity, attenuation, startup and fault behaviour.\n'''
    (ROOT / "SSI2164_BUFFER_CONTROL_REVIEW.md").write_text(review, encoding="utf-8")

    audit = {
        "schema_version": 1,
        "base_commit": "8df52377de753c8c910d67fc31405782d52a1be8",
        "lane": "Gate B lane 03 — SSI2164 package and control law",
        "buffer": {
            "part": "OPA4196",
            "reference": "U63",
            "package_target": "PW_TSSOP_14",
            "supply": "+/-12V",
            "units_sheet05": [1, 2, 4],
            "units_sheet06": [3, 5],
            "footprint_assigned": False,
            "output_isolation_ohm": 20,
            "local_bypass_nf_each_rail": 100,
        },
        "ssi2164": {
            "reference": "U60",
            "package_id": "PSL16",
            "jedec": "MS-012-AC",
            "orderable": ["SSI2164S-TU", "SSI2164S-RT"],
            "control_impedance_kohm": {"min": 9, "nominal": 10, "max": 11},
            "gain_constant_mv_per_db": -33,
            "footprint_assigned": False,
        },
        "calculation": {
            "nominal_reference_v": 3.3,
            "lower_resistor_only_reference_v": 3.244,
            "worst_control_impedance_ohm": 9000,
            "series_ohm": 20,
            "nominal_vc_v": 3.3 * 9000 / 9020,
            "nominal_attenuation_db": (3.3 * 9000 / 9020) / 0.033,
            "lower_reference_vc_v": 3.244 * 9000 / 9020,
            "lower_reference_attenuation_db": (3.244 * 9000 / 9020) / 0.033,
        },
        "authority": {
            "pcb": False,
            "panel": False,
            "fabrication": False,
            "purchasing": False,
            "production": False,
        },
        "status": "IMPLEMENTED_PENDING_CI_AND_INDEPENDENT_REVIEW",
    }
    (ROOT / "SSI2164_BUFFER_AUDIT.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    validator = '''#!/usr/bin/env python3\nfrom __future__ import annotations\n\nimport json\nimport subprocess\nfrom pathlib import Path\n\nROOT = Path("hardware/memory-core-prototype-a")\n\ndef blob(path: Path) -> str:\n    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()\n\ndef main() -> None:\n    assert blob(ROOT / "08_CONTROLS_STATE.kicad_sch") == "2d681089ed95fada6f476060cb6163311a3fde45"\n    assert blob(ROOT / "MerrinGriefSynthMemoryCoreA.kicad_sch") == "8ef352f7a72197214e34dacdf998046382589937"\n    assert blob(Path("tools/capture_controls_state_sheet.py")) == "0485f51b3c78ab95aa8b8f94d01b8aeedc73d188"\n\n    audit = json.loads((ROOT / "SSI2164_BUFFER_AUDIT.json").read_text())\n    assert audit["buffer"]["part"] == "OPA4196"\n    assert audit["buffer"]["footprint_assigned"] is False\n    assert audit["ssi2164"]["footprint_assigned"] is False\n    assert audit["calculation"]["nominal_attenuation_db"] > 99.7\n    assert audit["calculation"]["lower_reference_attenuation_db"] > 98.0\n    assert all(value is False for value in audit["authority"].values())\n\n    library = (ROOT / "MerrinLab_PrototypeA.kicad_sym").read_text()\n    for unit in range(1, 6):\n        assert f'(symbol "OPA4196_PW_MULTI_{unit}_1"' in library\n    assert 'property "Footprint" ""' in library\n\n    sheet05 = (ROOT / "05_MEMORY_GHOST_WET.kicad_sch").read_text()\n    sheet06 = (ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch").read_text()\n    for token in ("R525", "R526", "R527", "20R buffer isolate", "D500", "D505"):\n        assert token in sheet05, token\n    for token in ("R604A", "20R buffer isolate", "C642", "C643", "D600", "D601"):\n        assert token in sheet06, token\n    assert sheet05.count('property "Reference" "U63"') == 3\n    assert sheet06.count('property "Reference" "U63"') == 2\n    assert sheet05.count('property "Footprint" ""') > 0\n    assert sheet06.count('property "Footprint" ""') > 0\n\n    print("OPA4196 shared five-unit symbol and ownership: PASS")\n    print("SSI2164 buffered 20-ohm control law: PASS")\n    print("Sheet 08 and top-level hierarchy unchanged: PASS")\n    print("Footprints and downstream authority remain blocked: PASS")\n\nif __name__ == "__main__":\n    main()\n'''
    Path("tools/validate_ssi2164_buffer_lane.py").write_text(validator, encoding="utf-8")


def main() -> None:
    assert_sources()
    patch_return_generator()
    patch_memory_generator()
    patch_validators()
    patch_docs()
    write_authority_files()
    print("SSI2164 buffer source patch applied; regeneration and validation required")


if __name__ == "__main__":
    main()
