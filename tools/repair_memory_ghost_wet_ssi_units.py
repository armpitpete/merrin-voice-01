#!/usr/bin/env python3
"""Correct sheet-05 SSI2164 attachments after native generation.

The pinned schematic API mirrors Y coordinates returned for pins in the custom
multi-unit SSI2164 symbol. This repair moves only the nine Memory, Ghost and
wet-master labels to their actual KiCad pin coordinates and normalises all three
units to the shared physical-device value ``SSI2164``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

GEOMETRY_PATH = Path(__file__).with_name("repair_return_ssi_units.py")
SPEC = importlib.util.spec_from_file_location("ssi2164_physical_geometry", GEOMETRY_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load SSI2164 geometry helpers: {GEOMETRY_PATH}")

geometry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = geometry
SPEC.loader.exec_module(geometry)

ROOT = Path("hardware/memory-core-prototype-a")
SHEET_FILE = ROOT / "05_MEMORY_GHOST_WET.kicad_sch"

MEMORY_POSITION = (116.84, 83.82)
GHOST_POSITION = (116.84, 137.16)
WET_POSITION = (276.86, 111.76)

PIN_GEOMETRY = {
    "SSI_IIN1": (MEMORY_POSITION, "left", 1),
    "SSI_VC1": (MEMORY_POSITION, "left", 3),
    "SSI_IOUT1": (MEMORY_POSITION, "right", 2),
    "SSI_IIN2": (GHOST_POSITION, "left", 1),
    "SSI_VC2": (GHOST_POSITION, "left", 3),
    "SSI_IOUT2": (GHOST_POSITION, "right", 2),
    "SSI_IIN4": (WET_POSITION, "left", 1),
    "SSI_VC4": (WET_POSITION, "left", 3),
    "SSI_IOUT4": (WET_POSITION, "right", 2),
}

VALUES = (
    '"SSI2164 — MEMORY CH1"',
    '"SSI2164 — GHOST CH2"',
    '"SSI2164 — WET MASTER CH4"',
)


def main() -> None:
    text = SHEET_FILE.read_text(encoding="utf-8")
    for name, (position, side, row) in PIN_GEOMETRY.items():
        text = geometry.repair_label(text, name, position, side, row)

    for old in VALUES:
        if old not in text:
            raise RuntimeError(f"Missing expected SSI2164 unit value: {old}")
        text = text.replace(old, '"SSI2164"', 1)

    SHEET_FILE.write_text(text, encoding="utf-8")
    print("Corrected sheet-05 SSI2164 Memory/Ghost/wet pin attachments")
    print("Normalised U60 units 1/2/4 to the shared SSI2164 physical-device value")


if __name__ == "__main__":
    main()
