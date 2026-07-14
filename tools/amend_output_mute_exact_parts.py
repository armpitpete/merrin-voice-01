#!/usr/bin/env python3
"""Apply the reviewed exact-part correction to sheet 07.

The amendment is deterministic and idempotent. It replaces the provisional
mute/fault devices with exact physical pin maps, changes the fault path to a
powered healthy-release path, fixes the timing/isolation values, and assigns
only the three independently reviewed package footprints. PCB work remains
outside this script.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "07_OUTPUT_MUTE_EXACT_PARTS_AMENDED"
SOT23 = "Package_TO_SOT_SMD:SOT-23"
SMDIP4 = "Package_DIP:SMDIP-4_W7.62mm"


def balanced_block(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise RuntimeError(f"Unterminated S-expression at offset {start}")


def effects(hidden: bool = False) -> str:
    hide = " hide" if hidden else ""
    return (
        "\t\t\t(effects\n"
        "\t\t\t\t(font\n"
        "\t\t\t\t\t(size 1.27 1.27)\n"
        "\t\t\t\t)"
        f"{hide}\n"
        "\t\t\t)\n"
    )


def property_block(name: str, value: str, y: float, hidden: bool = False) -> str:
    return (
        f'\t\t(property "{name}" "{value}"\n'
        f"\t\t\t(at 0 {y} 0)\n"
        f"{effects(hidden)}"
        "\t\t)\n"
    )


def render_symbol(name: str, reference: str, footprint: str, datasheet: str,
                  description: str, pins: tuple[tuple[str, str, str, float, float, int], ...],
                  *, qualified: bool) -> str:
    rendered_name = f"MerrinLab_PrototypeA:{name}" if qualified else name
    out = [
        f'\t\t(symbol "{rendered_name}"\n',
        "\t\t\t(exclude_from_sim no)\n",
        "\t\t\t(in_bom yes)\n",
        "\t\t\t(on_board yes)\n",
        property_block("Reference", reference, 10.16),
        property_block("Value", name, -10.16),
        property_block("Footprint", footprint, 0, True),
        property_block("Datasheet", datasheet, 0, True),
        property_block("Description", description, 0, True),
        f'\t\t\t(symbol "{name}_1_1"\n',
        "\t\t\t\t(rectangle\n",
        "\t\t\t\t\t(start -6.35 7.62)\n",
        "\t\t\t\t\t(end 6.35 -7.62)\n",
        "\t\t\t\t\t(stroke\n",
        "\t\t\t\t\t\t(width 0.254)\n",
        "\t\t\t\t\t\t(type default)\n",
        "\t\t\t\t\t)\n",
        "\t\t\t\t\t(fill\n",
        "\t\t\t\t\t\t(type background)\n",
        "\t\t\t\t\t)\n",
        "\t\t\t\t)\n",
    ]
    for number, pin_name, pin_type, x, y, rotation in pins:
        out.extend([
            f"\t\t\t\t(pin {pin_type} line\n",
            f"\t\t\t\t\t(at {x} {y} {rotation})\n",
            "\t\t\t\t\t(length 3.81)\n",
            f'\t\t\t\t\t(name "{pin_name}"\n',
            "\t\t\t\t\t\t(effects\n",
            "\t\t\t\t\t\t\t(font\n",
            "\t\t\t\t\t\t\t\t(size 0.762 0.762)\n",
            "\t\t\t\t\t\t\t)\n",
            "\t\t\t\t\t\t)\n",
            "\t\t\t\t\t)\n",
            f'\t\t\t\t\t(number "{number}"\n',
            "\t\t\t\t\t\t(effects\n",
            "\t\t\t\t\t\t\t(font\n",
            "\t\t\t\t\t\t\t\t(size 1.016 1.016)\n",
            "\t\t\t\t\t\t\t)\n",
            "\t\t\t\t\t\t)\n",
            "\t\t\t\t\t)\n",
            "\t\t\t\t)\n",
        ])
    out.extend(["\t\t\t)\n", "\t\t)\n"])
    return "".join(out)


SYMBOLS = {
    "MMBFJ113_APPLICATION": dict(
        reference="Q", footprint=SOT23,
        datasheet="https://www.onsemi.com/pdf/datasheet/mmbfj113-d.pdf",
        description="Exact onsemi MMBFJ113 N-channel JFET, SOT-23 pins 1 drain, 2 source, 3 gate",
        pins=(("1", "DRAIN", "passive", -10.16, 5.08, 0),
              ("3", "GATE", "input", -10.16, 2.54, 0),
              ("2", "SOURCE", "passive", 10.16, 5.08, 180)),
    ),
    "PMV20XNE_APPLICATION": dict(
        reference="Q", footprint=SOT23,
        datasheet="https://assets.nexperia.com/documents/data-sheet/PMV20XNE.pdf",
        description="Exact Nexperia PMV20XNE 30 V N-channel MOSFET, SOT-23 pins 1 gate, 2 source, 3 drain",
        pins=(("1", "GATE", "input", -10.16, 2.54, 0),
              ("3", "DRAIN", "passive", 10.16, 5.08, 180),
              ("2", "SOURCE", "passive", 10.16, 0.0, 180)),
    ),
    "VO617A_3X007T_APPLICATION": dict(
        reference="U", footprint=SMDIP4,
        datasheet="https://www.vishay.com/docs/83430/vo617a.pdf",
        description="Exact Vishay VO617A-3X007T optocoupler, option-7 SMD-4 pins 1 A, 2 K, 3 E, 4 C",
        pins=(("1", "LED_A", "input", -10.16, 5.08, 0),
              ("2", "LED_K", "passive", -10.16, 0.0, 0),
              ("3", "EMITTER", "passive", 10.16, 0.0, 180),
              ("4", "COLLECTOR", "passive", 10.16, 5.08, 180)),
    ),
}
OLD_TO_NEW = {
    "J113_SHUNT_APPLICATION": "MMBFJ113_APPLICATION",
    "NPN_FAULT_INVERTER_APPLICATION": "PMV20XNE_APPLICATION",
    "LTV817S_MUTE_APPLICATION": "VO617A_3X007T_APPLICATION",
}


def replace_symbol_definition(text: str, old: str, new: str, *, qualified: bool) -> str:
    old_name = f"MerrinLab_PrototypeA:{old}" if qualified else old
    new_name = f"MerrinLab_PrototypeA:{new}" if qualified else new
    indent = "\t\t" if qualified else "\t"
    old_marker = f'{indent}(symbol "{old_name}"'
    new_marker = f'{indent}(symbol "{new_name}"'
    block = render_symbol(new, qualified=qualified, **SYMBOLS[new])
    if not qualified:
        block = "".join(line[1:] if line.startswith("\t") else line
                        for line in block.splitlines(keepends=True))
    marker = old_marker if old_marker in text else new_marker if new_marker in text else None
    if marker is None:
        raise RuntimeError(f"Neither old nor new symbol found: {old} / {new}")
    marker_start = text.index(marker)
    start = marker_start + len(indent)
    current = balanced_block(text, start)
    return text[:marker_start] + block + text[start + len(current):]


def instance_block(text: str, reference: str) -> tuple[int, str]:
    marker = "\n\t(symbol\n\t\t(lib_id "
    matches = []
    offset = 0
    while True:
        found = text.find(marker, offset)
        if found == -1:
            break
        start = found + 2
        block = balanced_block(text, start)
        if f'(property "Reference" "{reference}"' in block:
            matches.append((start, block))
        offset = start + len(block)
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {reference} instance, found {len(matches)}")
    return matches[0]


def replace_instance(text: str, reference: str, *, old_lib: str, new_lib: str,
                     old_value: str, new_value: str, footprint: str) -> str:
    start, original = instance_block(text, reference)
    block = original
    old_id = f'(lib_id "MerrinLab_PrototypeA:{old_lib}")'
    new_id = f'(lib_id "MerrinLab_PrototypeA:{new_lib}")'
    if old_id in block:
        block = block.replace(old_id, new_id, 1)
    elif new_id not in block:
        raise RuntimeError(f"Unexpected {reference} library id")
    old_token = f'(property "Value" "{old_value}"'
    new_token = f'(property "Value" "{new_value}"'
    if old_token in block:
        block = block.replace(old_token, new_token, 1)
    elif new_token not in block:
        raise RuntimeError(f"Unexpected {reference} value")
    block, count = re.subn(r'\(property "Footprint" "[^"]*"',
                           f'(property "Footprint" "{footprint}"', block, count=1)
    if count != 1:
        raise RuntimeError(f"Could not update {reference} footprint")
    return text[:start] + block + text[start + len(original):]


def replace_value(text: str, old: str, new: str) -> str:
    old_token = f'(property "Value" "{old}"'
    new_token = f'(property "Value" "{new}"'
    if old_token in text:
        if text.count(old_token) != 1:
            raise RuntimeError(f"Ambiguous value {old!r}")
        return text.replace(old_token, new_token, 1)
    if new_token in text:
        return text
    raise RuntimeError(f"Neither old nor new value found: {old!r}")


def replace_label_at(text: str, old: str, new: str, x: str, y: str) -> str:
    old_token = f'(label "{old}"\n\t\t(at {x} {y} 0)'
    new_token = f'(label "{new}"\n\t\t(at {x} {y} 0)'
    if old_token in text:
        if text.count(old_token) != 1:
            raise RuntimeError(f"Ambiguous label {old} at {x},{y}")
        return text.replace(old_token, new_token, 1)
    if new_token in text:
        return text
    raise RuntimeError(f"Label not found: {old}/{new} at {x},{y}")


def replace_text_once(text: str, old: str, new: str) -> str:
    if old in text:
        if text.count(old) != 1:
            raise RuntimeError(f"Ambiguous text {old!r}")
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise RuntimeError(f"Text not found: {old!r}")


def amend_library() -> None:
    text = LIBRARY.read_text(encoding="utf-8")
    for old, new in OLD_TO_NEW.items():
        text = replace_symbol_definition(text, old, new, qualified=False)
    LIBRARY.write_text(text, encoding="utf-8")


def amend_sheet() -> None:
    text = SHEET.read_text(encoding="utf-8")
    for old, new in OLD_TO_NEW.items():
        text = replace_symbol_definition(text, old, new, qualified=True)
    text = replace_instance(text, "Q70", old_lib="J113_SHUNT_APPLICATION",
                            new_lib="MMBFJ113_APPLICATION",
                            old_value="J113 OUTPUT MUTE SHUNT",
                            new_value="MMBFJ113 OUTPUT MUTE SHUNT", footprint=SOT23)
    text = replace_instance(text, "Q71", old_lib="NPN_FAULT_INVERTER_APPLICATION",
                            new_lib="PMV20XNE_APPLICATION",
                            old_value="MMBT3904 fault inverter provisional",
                            new_value="PMV20XNE HEALTHY-RELEASE DRIVER", footprint=SOT23)
    text = replace_instance(text, "U70", old_lib="LTV817S_MUTE_APPLICATION",
                            new_lib="VO617A_3X007T_APPLICATION",
                            old_value="LTV-817S-CLASS FAIL-MUTE",
                            new_value="VO617A-3X007T HEALTHY RELEASE", footprint=SMDIP4)
    for old, new in (
        ("10k mute isolation", "120k 1% mute isolation"),
        ("10k fault inverter base", "10k fault gate series"),
        ("100k fault base pull-down", "100k fault gate pull-down"),
        ("2.2k +12V fault pull-up", "820R 1% optocoupler LED series A"),
        ("3.3k optocoupler LED", "1k 1% optocoupler LED series B"),
        ("100k controlled release", "10k 1% negative release"),
        ("1M power-off mute", "100k 1% fail-mute pull"),
        ("1uF mute ramp", "100nF C0G 50V mute timing"),
    ):
        text = replace_value(text, old, new)
    for x, y in (("91.44", "201.93"), ("106.68", "209.55"), ("121.92", "195.58")):
        text = replace_label_at(text, "FAULT_INV_BASE", "FAULT_GATE", x, y)
    for old, new, x, y in (
        ("MUTE_FAULT_HIGH", "MUTE_LED_K", "142.24", "193.04"),
        ("MUTE_FAULT_HIGH", "MUTE_LED_SUPPLY", "154.94", "186.69"),
        ("MUTE_FAULT_HIGH", "MUTE_LED_SUPPLY", "170.18", "194.31"),
        ("GND", "MUTE_LED_K", "193.04", "198.12"),
        ("MUTE_GATE", "RELEASE_SINK", "213.36", "198.12"),
        ("GND", "MUTE_GATE", "213.36", "193.04"),
        ("MUTE_GATE", "RELEASE_SINK", "238.76", "186.69"),
    ):
        text = replace_label_at(text, old, new, x, y)
    text = replace_text_once(
        text,
        '(comment 2 "Output jack and active-device footprints remain blocked pending independent review.")',
        '(comment 2 "Q70/Q71/U70 exact parts and package footprints verified; PCB placement remains blocked.")')
    text = replace_text_once(
        text,
        "DIRECT + WET HALF-SUM • OUTPUT LEVEL • FAIL-MUTED JFET • PROTECTED MONO OUT",
        "DIRECT + WET HALF-SUM • OUTPUT LEVEL • HEALTHY-RELEASE FAIL-MUTE • PROTECTED MONO OUT")
    text = replace_text_once(
        text,
        "FAIL-MUTE CONTRACT\\nFault/undefined HARDWARE_FAULT_N lights U70 and clamps MUTE_GATE toward 0 V.\\nHealthy release approaches -10.91 V from RAIL_N12 with about 90.9 ms RC time constant.\\nAt 50% assumed CTR, the first-pass fault-clamp estimate is 12.7 ms; exact optocoupler/JFET parts remain a later measured gate.",
        "EXACT FAIL-MUTE CONTRACT\\nHealthy HARDWARE_FAULT_N drives PMV20XNE and VO617A-3X007T, connecting the negative release path.\\nFault or +12 V loss removes release drive; 100k/100nF returns MUTE_GATE toward 0 V and crosses -3 V in about 12.6 ms.\\n120k isolation with 100 ohm worst JFET on-resistance calculates better than 60 dB static attenuation; bench proof remains Gate C.")
    text = replace_text_once(
        text,
        "No audio or control net is exported from this sheet; physical jack/footprint acceptance remains blocked.",
        "No audio or control net is exported; Q70/Q71/U70 package mappings are accepted, while jack mechanics and PCB work remain blocked.")
    for token in ("J113_SHUNT_APPLICATION", "NPN_FAULT_INVERTER_APPLICATION",
                  "LTV817S_MUTE_APPLICATION", "FAULT_INV_BASE", "MUTE_FAULT_HIGH"):
        if token in text:
            raise RuntimeError(f"Obsolete output-mute token remains: {token}")
    SHEET.write_text(text, encoding="utf-8")


def verify_calculations() -> None:
    isolation_min = 120_000 * 0.99
    attenuation_db = -20 * math.log10(100.0 / (isolation_min + 100.0))
    assert attenuation_db > 60.0
    healthy_gate = (-12.0 + 0.4) * 100_000 / 110_000
    crossing_ms = 100_000 * 100e-9 * 1000 * math.log(abs(healthy_gate) / 3.0)
    assert healthy_gate < -10.0 and crossing_ms < 20.0
    gate_low = 3.3 * 0.95 * (100_000 * 0.99) / (
        10_000 * 1.01 + 10_000 * 1.01 + 100_000 * 0.99)
    assert gate_low > 2.5
    led_low_ma = (12.0 * 0.95 - 1.65) / ((820 + 1000) * 1.01) * 1000
    release_ma = abs(healthy_gate) / 10_000 * 1000
    assert led_low_ma >= 5.0 and led_low_ma > 4 * release_ma


def main() -> None:
    for required in (SHEET, LIBRARY):
        if not required.exists():
            raise SystemExit(f"Missing required file: {required}")
    amend_library()
    amend_sheet()
    verify_calculations()
    MARKER.write_text(
        "Sheet 07 exact mute parts, healthy-release fault path and three package footprints amended and awaiting/holding ERC evidence.\n",
        encoding="utf-8")
    print("Output-mute exact-part amendment: PASS")
    print("Q70 MMBFJ113 / Q71 PMV20XNE / U70 VO617A-3X007T: APPLIED")
    print("Calculated static mute attenuation: >60 dB")
    print("Calculated worst-cutoff crossing after fault/+12 V loss: <20 ms")


if __name__ == "__main__":
    main()
