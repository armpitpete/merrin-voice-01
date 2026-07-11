#!/usr/bin/env python3
"""Correct project-local SSI2164 multi-unit pin attachments after sheet-06 generation.

The pinned schematic API mirrors the Y coordinate returned for pins in custom
multi-unit symbols. This repair moves only the six channel-3/common-power
attachments to their actual KiCad coordinates and normalises both units to the
same physical-device value.

No placeholder copies of channels 1, 2 or 4 are created. Those genuine units
remain available for sheet 05 under the same U60 reference.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET_FILE = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"

# Symbol geometry is fixed by capture_return_break_limiter_sheet.py.
CHANNEL_POSITION = (116.84, 101.60)
POWER_POSITION = (116.84, 139.70)
HALF_HEIGHT = 6.35

PIN_GEOMETRY = {
    "SSI_IIN3": (CHANNEL_POSITION, "left", 1),
    "SSI_VC3": (CHANNEL_POSITION, "left", 3),
    "SSI_IOUT3": (CHANNEL_POSITION, "right", 2),
    "MODE_NC": (POWER_POSITION, "left", 1),
    "GND": (POWER_POSITION, "left", 3),
    "RAIL_N12": (POWER_POSITION, "left", 4),
    "RAIL_P12": (POWER_POSITION, "right", 2),
}


def actual_pin_position(position: tuple[float, float], side: str, row: int) -> tuple[float, float]:
    local_y = HALF_HEIGHT - 2.54 * row
    x = position[0] - 10.16 if side == "left" else position[0] + 10.16
    y = position[1] - local_y
    return (round(x, 2), round(y, 2))


def mirrored_pin_position(position: tuple[float, float], side: str, row: int) -> tuple[float, float]:
    local_y = HALF_HEIGHT - 2.54 * row
    x = position[0] - 10.16 if side == "left" else position[0] + 10.16
    y = position[1] + local_y
    return (round(x, 2), round(y, 2))


def number_pattern(value: float) -> str:
    integer = int(value)
    if value == integer:
        return rf"{integer}(?:\.0+)?"
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return re.escape(text)


def repair_label(text: str, name: str, position: tuple[float, float], side: str, row: int) -> str:
    wrong_x, wrong_y = mirrored_pin_position(position, side, row)
    right_x, right_y = actual_pin_position(position, side, row)
    pattern = (
        rf'(\(label "{re.escape(name)}"\s+\(at '
        rf'{number_pattern(wrong_x)} {number_pattern(wrong_y)} )0(?:\.0+)?(\))'
    )
    replacement = rf"\g<1>0\g<2>"
    repaired, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise RuntimeError(
            f"Expected one mirrored label for {name} at {(wrong_x, wrong_y)}, found {count}"
        )
    # Replace only the coordinates inside the captured match.
    wrong_fragment = f'(label "{name}"\n\t\t(at {wrong_x} {wrong_y} 0)'
    right_fragment = f'(label "{name}"\n\t\t(at {right_x} {right_y} 0)'
    if wrong_fragment in repaired:
        repaired = repaired.replace(wrong_fragment, right_fragment, 1)
    else:
        # Serialisation may use equivalent integer forms; apply a direct regex.
        coordinate_pattern = (
            rf'(\(label "{re.escape(name)}"\s+\(at )'
            rf'{number_pattern(wrong_x)} {number_pattern(wrong_y)} 0(\))'
        )
        repaired, coordinate_count = re.subn(
            coordinate_pattern,
            rf"\g<1>{right_x} {right_y} 0\g<2>",
            repaired,
            count=1,
        )
        if coordinate_count != 1:
            raise RuntimeError(f"Could not rewrite coordinates for {name}")
    return repaired


def repair_no_connect(text: str) -> str:
    position, side, row = PIN_GEOMETRY["MODE_NC"]
    wrong_x, wrong_y = mirrored_pin_position(position, side, row)
    right_x, right_y = actual_pin_position(position, side, row)
    pattern = (
        rf'(\(no_connect\s+\(at )'
        rf'{number_pattern(wrong_x)} {number_pattern(wrong_y)}(\))'
    )
    repaired, count = re.subn(
        pattern,
        rf"\g<1>{right_x} {right_y}\g<2>",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Expected one mirrored MODE no-connect marker")
    return repaired


def normalise_value(text: str) -> str:
    replacements = (
        ('"SSI2164 — RETURN CH3"', '"SSI2164"'),
        ('"SSI2164 — COMMON POWER"', '"SSI2164"'),
    )
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"Missing expected SSI2164 value: {old}")
        text = text.replace(old, new, 1)
    return text


def main() -> None:
    text = SHEET_FILE.read_text(encoding="utf-8")
    for name in ("SSI_IIN3", "SSI_VC3", "SSI_IOUT3", "GND", "RAIL_N12", "RAIL_P12"):
        position, side, row = PIN_GEOMETRY[name]
        text = repair_label(text, name, position, side, row)
    text = repair_no_connect(text)
    text = normalise_value(text)
    SHEET_FILE.write_text(text, encoding="utf-8")

    print("Corrected SSI2164 official channel-3 pins 15/14/13 and common-power attachments")
    print("No placeholder units created; U60 units 1/2/4 remain available for sheet 05")


if __name__ == "__main__":
    main()
