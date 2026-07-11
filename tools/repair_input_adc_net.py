#!/usr/bin/env python3
"""Repair the sheet-04 ADC buffer/output net boundary after generation.

The capture generator originally labelled both sides of R415 with exported
ADC_ANALOG_IN and also left an obsolete ADC_ANALOG_IN_OUT label. This bounded
repair keeps U41C and R415 pin 1 on local ADC_BUFFER, removes the obsolete
label, and leaves only R415 pin 2 as exported ADC_ANALOG_IN.
"""

import re
from pathlib import Path

SHEET = Path("hardware/memory-core-prototype-a/04_INPUT_PRESSURE_ABSENCE.kicad_sch")

RENAMES = (
    ((327.66, 171.45), "ADC_ANALOG_IN", "ADC_BUFFER"),
    ((327.66, 168.91), "ADC_ANALOG_IN", "ADC_BUFFER"),
    ((337.82, 107.95), "ADC_ANALOG_IN", "ADC_BUFFER"),
)


def rename_label(text: str, position: tuple[float, float], old: str, new: str) -> str:
    x, y = position
    pattern = rf'(\(label "){re.escape(old)}("\s+\(at {x} {y} 0\))'
    repaired, count = re.subn(pattern, rf'\g<1>{new}\g<2>', text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected one {old} label at {position}, found {count}")
    return repaired


def remove_obsolete_label(text: str) -> str:
    pattern = (
        r'\n\t\(label "ADC_ANALOG_IN_OUT"\s+'
        r'\(at 337\.82 115\.57 0\)'
        r'.*?\n\t\)'
    )
    repaired, count = re.subn(pattern, "", text, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"Expected one obsolete ADC_ANALOG_IN_OUT label, found {count}")
    return repaired


def main() -> None:
    text = SHEET.read_text(encoding="utf-8")
    for position, old, new in RENAMES:
        text = rename_label(text, position, old, new)
    text = remove_obsolete_label(text)
    SHEET.write_text(text, encoding="utf-8")
    print("Renamed U41C and R415 input side to ADC_BUFFER")
    print("Removed obsolete ADC_ANALOG_IN_OUT label")
    print("R415 output remains the only exported ADC_ANALOG_IN node")


if __name__ == "__main__":
    main()
