#!/usr/bin/env python3
"""Qualify the sheet-07 mute-depth annotation without changing circuit topology."""

from pathlib import Path

SHEET = Path("hardware/memory-core-prototype-a/07_OUTPUT_MUTE_PROTECTION.kicad_sch")

OLD = (
    "120k isolation with 100 ohm worst JFET on-resistance calculates better than 60 dB "
    "static attenuation; bench proof remains Gate C."
)
NEW = (
    "120k isolation with the 100 ohm MMBFJ113 maximum at TJ = 25 C calculates 61.5 dB "
    "static attenuation; temperature, spread and measured mute depth remain Gate C."
)


def main() -> None:
    text = SHEET.read_text(encoding="utf-8")
    if OLD in text:
        assert text.count(OLD) == 1
        text = text.replace(OLD, NEW)
        SHEET.write_text(text, encoding="utf-8")
        print("Sheet-07 25 C mute-depth qualification: APPLIED")
    elif NEW in text:
        print("Sheet-07 25 C mute-depth qualification: CURRENT")
    else:
        raise SystemExit("Expected sheet-07 mute-depth annotation was not found")


if __name__ == "__main__":
    main()
