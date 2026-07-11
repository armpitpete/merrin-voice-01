#!/usr/bin/env python3
"""Shared OPA1679 multi-unit symbol and hierarchy repair helpers.

U32 is one physical OPA1679 shared across sheets 03 and 07:
unit 1 (A) plus unit 5 (power) remain on the codec sheet; units 2/3/4
(B/C/D) implement final mix, output level buffering and post-mute drive.
Active-device footprints remain blank pending the independent footprint gate.
"""

from __future__ import annotations

import re
from pathlib import Path

SYMBOL_NAME = "OPA1679_PW_MULTI"
LIB_ID = f"MerrinLab_PrototypeA:{SYMBOL_NAME}"
REFERENCE = "U32"
VALUE = "OPA1679"
HALF_HEIGHT = 6.35

# Unit -> pin number -> (name, electrical type, side, row)
UNITS = {
    1: {
        "3": ("IN_A+", "input", "left", 1),
        "2": ("IN_A-", "input", "left", 3),
        "1": ("OUT_A", "output", "right", 2),
    },
    2: {
        "5": ("IN_B+", "input", "left", 1),
        "6": ("IN_B-", "input", "left", 3),
        "7": ("OUT_B", "output", "right", 2),
    },
    3: {
        "10": ("IN_C+", "input", "left", 1),
        "9": ("IN_C-", "input", "left", 3),
        "8": ("OUT_C", "output", "right", 2),
    },
    4: {
        "12": ("IN_D+", "input", "left", 1),
        "13": ("IN_D-", "input", "left", 3),
        "14": ("OUT_D", "output", "right", 2),
    },
    5: {
        "11": ("V-", "power_in", "left", 3),
        "4": ("V+", "power_in", "right", 1),
    },
}


def _property(name: str, value: str, y: float, hidden: bool = False) -> str:
    hide = "\n\t\t\t\t hide" if hidden else ""
    return (
        f'\t\t(property "{name}" "{value}"\n'
        f"\t\t\t(at 0 {y} 0)\n"
        "\t\t\t(effects\n"
        "\t\t\t\t(font (size 1.27 1.27))"
        f"{hide}\n"
        "\t\t\t)\n"
        "\t\t)\n"
    )


def render_symbol() -> str:
    out = [
        f'\t(symbol "{SYMBOL_NAME}"\n',
        "\t\t(exclude_from_sim no)\n",
        "\t\t(in_bom yes)\n",
        "\t\t(on_board yes)\n",
        _property("Reference", "U", 8.89),
        _property("Value", SYMBOL_NAME, -8.89),
        _property("Footprint", "", 0, True),
        _property("Datasheet", "https://www.ti.com/lit/ds/symlink/opa1679.pdf", 0, True),
        _property(
            "Description",
            "OPA1679 quad audio op amp; five-unit TSSOP-14 symbol; official pin map; footprint pending",
            0,
            True,
        ),
    ]
    for unit in range(1, 6):
        out.extend(
            [
                f'\t\t(symbol "{SYMBOL_NAME}_{unit}_1"\n',
                "\t\t\t(rectangle\n",
                f"\t\t\t\t(start -6.35 {HALF_HEIGHT})\n",
                f"\t\t\t\t(end 6.35 {-HALF_HEIGHT})\n",
                "\t\t\t\t(stroke (width 0.254) (type default))\n",
                "\t\t\t\t(fill (type background))\n",
                "\t\t\t)\n",
            ]
        )
        for number, (name, pin_type, side, row) in UNITS[unit].items():
            local_y = HALF_HEIGHT - 2.54 * row
            x = -10.16 if side == "left" else 10.16
            rotation = 0 if side == "left" else 180
            out.extend(
                [
                    f"\t\t\t(pin {pin_type} line\n",
                    f"\t\t\t\t(at {x} {local_y} {rotation})\n",
                    "\t\t\t\t(length 3.81)\n",
                    f'\t\t\t\t(name "{name}" (effects (font (size 0.762 0.762))))\n',
                    f'\t\t\t\t(number "{number}" (effects (font (size 1.016 1.016))))\n',
                    "\t\t\t)\n",
                ]
            )
        out.append("\t\t)\n")
    out.append("\t)\n")
    return "".join(out)


def append_symbol_library(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if f'(symbol "{SYMBOL_NAME}"' in text:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    path.write_text(stripped[:-1] + render_symbol() + ")\n", encoding="utf-8")


def _number_pattern(value: float) -> str:
    integer = int(value)
    if value == integer:
        return rf"{integer}(?:\.0+)?"
    return re.escape(f"{value:.2f}".rstrip("0").rstrip("."))


def serialized_component_position(text: str, unit: int) -> tuple[float, float]:
    pattern = (
        rf'\(symbol\s+\(lib_id "{re.escape(LIB_ID)}"\)\s+'
        rf'\(at ([+-]?[0-9.]+) ([+-]?[0-9.]+) [^)]+\)\s+'
        rf'\(unit {unit}\)'
    )
    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) != 1:
        raise RuntimeError(f"Expected one serialized U32 unit {unit}, found {len(matches)}")
    return (float(matches[0][0]), float(matches[0][1]))


def repair_label(
    text: str,
    name: str,
    component_position: tuple[float, float],
    unit: int,
    pin: str,
) -> str:
    """Move one API-mirrored label to the serialized U32 physical pin."""
    del component_position
    position = serialized_component_position(text, unit)
    _pin_name, _pin_type, side, row = UNITS[unit][str(pin)]
    local_y = HALF_HEIGHT - 2.54 * row
    x = position[0] - 10.16 if side == "left" else position[0] + 10.16
    wrong_y = position[1] + local_y
    right_y = position[1] - local_y
    pattern = (
        rf'(\(label "{re.escape(name)}"\s+\(at )'
        rf'{_number_pattern(x)} {_number_pattern(wrong_y)} 0(?:\.0+)?(\))'
    )
    repaired, count = re.subn(
        pattern,
        rf"\g<1>{round(x, 2)} {round(right_y, 2)} 0\g<2>",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError(
            f"Expected one mirrored label {name} for U32 unit {unit} pin {pin} "
            f"at {(round(x, 2), round(wrong_y, 2))}, found {count}"
        )
    return repaired


def repair_hierarchical_shape(
    text: str,
    name: str,
    expected_shape: str,
    required_shape: str,
) -> str:
    pattern = (
        rf'(\(hierarchical_label "{re.escape(name)}"\s+\(shape )'
        rf'{re.escape(expected_shape)}(\))'
    )
    repaired, count = re.subn(
        pattern,
        rf"\g<1>{required_shape}\g<2>",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError(
            f"Expected exactly one {expected_shape}-shaped hierarchy label for {name}"
        )
    return repaired


def repair_hierarchical_output(text: str, name: str) -> str:
    return repair_hierarchical_shape(text, name, "input", "output")
