#!/usr/bin/env python3
"""Validate provisional sheet-07 control symbols and blank-footprint boundary."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"


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
    raise AssertionError(f"Unterminated S-expression at {start}")


def symbol_definition(text: str, name: str) -> str:
    marker = f'\t(symbol "{name}"'
    start = text.index(marker) + 1
    return balanced_block(text, start)


def instance_for_reference(text: str, reference: str) -> str:
    marker = "\n\t(symbol\n\t\t(lib_id "
    offset = 0
    matches = []
    while True:
        found = text.find(marker, offset)
        if found == -1:
            break
        start = found + 2
        block = balanced_block(text, start)
        if f'(property "Reference" "{reference}"' in block:
            matches.append(block)
        offset = start + len(block)
    assert len(matches) == 1, (reference, len(matches))
    return matches[0]


def assert_pin_contract(block: str, pins: dict[str, str]) -> None:
    for number, name in pins.items():
        assert f'(name "{name}"' in block, name
        assert f'(number "{number}"' in block, number


def main() -> None:
    sheet = SHEET.read_text(encoding="utf-8")
    library = LIBRARY.read_text(encoding="utf-8")

    npn_name = "NPN_FAULT_INVERTER_APPLICATION"
    pot_name = "OUTPUT_LEVEL_POT_APPLICATION"
    assert_pin_contract(
        symbol_definition(library, npn_name),
        {"1": "BASE", "2": "COLLECTOR", "3": "EMITTER"},
    )
    assert_pin_contract(
        symbol_definition(library, pot_name),
        {"1": "LOW", "2": "WIPER", "3": "HIGH"},
    )

    q71 = instance_for_reference(sheet, "Q71")
    rv700 = instance_for_reference(sheet, "RV700")
    assert f'(lib_id "MerrinLab_PrototypeA:{npn_name}")' in q71
    assert f'(lib_id "MerrinLab_PrototypeA:{pot_name}")' in rv700
    assert re.search(r'\(property "Footprint" ""', q71)
    assert re.search(r'\(property "Footprint" ""', rv700)

    assert "Transistor_BJT:Q_NPN_BCE" not in sheet
    assert "Device:Q_NPN_BCE" not in sheet
    assert "Device:R_Potentiometer" not in sheet

    print("Sheet-07 NPN and output-pot logical pin contracts: PASS")
    print("Sheet-07 provisional control footprints remain blank: PASS")


if __name__ == "__main__":
    main()
