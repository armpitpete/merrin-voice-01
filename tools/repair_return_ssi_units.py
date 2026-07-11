#!/usr/bin/env python3
"""Repair and complete SSI2164 multi-unit placement after sheet-06 generation.

The pinned schematic API currently mirrors the Y coordinate of pins from
project-local multi-unit symbols when `Component.get_pin_position()` is used.
This script corrects the channel-3/power-unit attachments using the known
symbol geometry and places channels 1, 2 and 4 as explicit reserved units.
Those reserved units are removed/replaced by real wet circuitry when sheet 05
is captured.
"""

import re
from pathlib import Path

import kicad_sch_api as ksa

ROOT = Path("hardware/memory-core-prototype-a")
SHEET_FILE = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
LIB_ID = "MerrinLab_PrototypeA:SSI2164S_APPLICATION"

# Corrections use actual KiCad pin coordinates for the custom symbol:
# actual_y = component_y - local_symbol_y. Patterns tolerate KiCad's equivalent
# integer/decimal serialisation, such as 127 and 127.0.
STRUCTURAL_REPAIRS = (
    (
        r'(\(label "SSI_IIN3"\s+\(at 81\.28 )93\.98( 0\))',
        r'\g<1>88.9\g<2>',
    ),
    (
        r'(\(label "SSI_IOUT3"\s+\(at 101\.6 )93\.98( 0\))',
        r'\g<1>88.9\g<2>',
    ),
    (
        r'(\(label "GND"\s+\(at 81\.28 )127(?:\.0)?( 0\))',
        r'\g<1>132.08\g<2>',
    ),
    (
        r'(\(label "RAIL_P12"\s+\(at 101\.6 )132\.08( 0\))',
        r'\g<1>127\g<2>',
    ),
    (
        r'(\(label "RAIL_N12"\s+\(at 101\.6 )127(?:\.0)?( 0\))',
        r'\g<1>132.08\g<2>',
    ),
    (
        r'(\(no_connect\s+\(at 81\.28 )132\.08(\))',
        r'\g<1>127\g<2>',
    ),
)

# Keep the six safety-critical coordinates deterministic after the schematic API
# writes equivalent KiCad numeric forms such as 0.0000 and 127.
SERIALISATION_NORMALISATIONS = (
    (
        r'(\(label "SSI_IIN3"\s+\(at 81\.28 88\.9 )0(?:\.0+)?(\))',
        r'\g<1>0\g<2>',
    ),
    (
        r'(\(label "SSI_IOUT3"\s+\(at 101\.6 88\.9 )0(?:\.0+)?(\))',
        r'\g<1>0\g<2>',
    ),
    (
        r'(\(label "GND"\s+\(at 81\.28 132\.08 )0(?:\.0+)?(\))',
        r'\g<1>0\g<2>',
    ),
    (
        r'(\(label "RAIL_P12"\s+\(at 101\.6 )127(?:\.0+)? 0(?:\.0+)?(\))',
        r'\g<1>127.0 0\g<2>',
    ),
    (
        r'(\(label "RAIL_N12"\s+\(at 101\.6 132\.08 )0(?:\.0+)?(\))',
        r'\g<1>0\g<2>',
    ),
    (
        r'(\(no_connect\s+\(at 81\.28 )127(?:\.0+)?(\))',
        r'\g<1>127.0\g<2>',
    ),
)

VALUE_REPLACEMENTS = {
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


def apply_one_regex(text, pattern, replacement):
    repaired, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected one structural SSI repair target, found {count}: {pattern!r}")
    return repaired


def replace_exact(text, old, new):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one SSI value repair target, found {count}: {old!r}")
    return text.replace(old, new, 1)


def main():
    text = SHEET_FILE.read_text(encoding="utf-8")
    for pattern, replacement in STRUCTURAL_REPAIRS:
        text = apply_one_regex(text, pattern, replacement)
    for old, new in VALUE_REPLACEMENTS.items():
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

    final_text = SHEET_FILE.read_text(encoding="utf-8")
    for pattern, replacement in SERIALISATION_NORMALISATIONS:
        final_text = apply_one_regex(final_text, pattern, replacement)
    SHEET_FILE.write_text(final_text, encoding="utf-8")

    print("Corrected SSI2164 channel-3 and power-unit physical pin attachments")
    print("Placed reserved U50 units 1, 2 and 4 with explicit no-connect pins")
    print("Normalised safety-critical SSI2164 coordinate serialisation")


if __name__ == "__main__":
    main()
