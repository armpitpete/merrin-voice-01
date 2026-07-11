#!/usr/bin/env python3
"""Repair and complete SSI2164 multi-unit placement after sheet-06 generation.

The pinned schematic API currently mirrors the Y coordinate of pins from
project-local multi-unit symbols when `Component.get_pin_position()` is used.
This script corrects the four channel-3/power-unit attachments using the known
symbol geometry and places channels 1, 2 and 4 as explicit reserved units.
Those reserved units are removed/replaced by real wet circuitry when sheet 05
is captured.
"""

from pathlib import Path

import kicad_sch_api as ksa

ROOT = Path("hardware/memory-core-prototype-a")
SHEET_FILE = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
LIB_ID = "MerrinLab_PrototypeA:SSI2164S_APPLICATION"

# Corrections use actual KiCad pin coordinates for the custom symbol:
# actual_y = component_y - local_symbol_y.
TEXT_REPLACEMENTS = {
    '(label "SSI_IIN3"\n\t\t(at 81.28 93.98 0)':
        '(label "SSI_IIN3"\n\t\t(at 81.28 88.9 0)',
    '(label "SSI_IOUT3"\n\t\t(at 101.6 93.98 0)':
        '(label "SSI_IOUT3"\n\t\t(at 101.6 88.9 0)',
    '(label "GND"\n\t\t(at 81.28 127.0 0)':
        '(label "GND"\n\t\t(at 81.28 132.08 0)',
    '(label "RAIL_P12"\n\t\t(at 101.6 132.08 0)':
        '(label "RAIL_P12"\n\t\t(at 101.6 127.0 0)',
    '(label "RAIL_N12"\n\t\t(at 101.6 127.0 0)':
        '(label "RAIL_N12"\n\t\t(at 101.6 132.08 0)',
    '(no_connect\n\t\t(at 81.28 132.08)':
        '(no_connect\n\t\t(at 81.28 127.0)',
    '"SSI2164 RETURN CH3"': '"SSI2164"',
    '"SSI2164 POWER"': '"SSI2164"',
}

# Unit -> (position, pins), where each pin is (number, side, row).
RESERVED_UNITS = {
    1: ((370.84, 205.74), (("2", "left", 2), ("3", "left", 3), ("4", "right", 2))),
    2: ((370.84, 231.14), (("7", "left", 2), ("6", "left", 3), ("5", "right", 2))),
    4: ((370.84, 256.54), (("15", "left", 2), ("14", "left", 3), ("13", "right", 2))),
}


def actual_pin_position(position, side, row):
    half_height = 7.62
    local_y = half_height - 2.54 * row
    x = position[0] - 10.16 if side == "left" else position[0] + 10.16
    y = position[1] - local_y
    return (round(x, 2), round(y, 2))


def replace_exact(text, old, new):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one exact SSI repair target, found {count}: {old!r}")
    return text.replace(old, new, 1)


def main():
    text = SHEET_FILE.read_text(encoding="utf-8")
    for old, new in TEXT_REPLACEMENTS.items():
        text = replace_exact(text, old, new)
    SHEET_FILE.write_text(text, encoding="utf-8")

    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))
    sch = ksa.load_schematic(str(SHEET_FILE))

    for unit, (position, pins) in RESERVED_UNITS.items():
        component = sch.components.add(
            lib_id=LIB_ID,
            reference="U50",
            value="SSI2164",
            position=position,
            unit=unit,
        )
        component.in_bom = True
        component.on_board = True
        for _pin_number, side, row in pins:
            sch.no_connects.add(position=actual_pin_position(position, side, row))

    sch.add_text(
        "U50 units A/B/D are reserved no-connect placeholders on sheet 06.\n"
        "Sheet 05 must remove these placeholders and place the real Memory/Ghost/Wet channels.",
        position=(332.74, 276.86),
        size=1.0,
    )
    sch.save(str(SHEET_FILE))

    print("Corrected SSI2164 channel-3 and power-unit physical pin attachments")
    print("Placed reserved U50 units 1, 2 and 4 with explicit no-connect pins")


if __name__ == "__main__":
    main()
