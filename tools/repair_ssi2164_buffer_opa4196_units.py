#!/usr/bin/env python3
"""Correct U63 OPA4196 multi-unit pin attachments after native generation.

The pinned schematic API mirrors Y coordinates returned for custom multi-unit
symbol pins. This repair moves only the U63 input, feedback, output and common-
power labels to the physical OPA4196 pin coordinates. Circuit topology, values,
references and footprints are not changed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

GEOMETRY_PATH = Path(__file__).with_name("repair_return_ssi_units.py")
SPEC = importlib.util.spec_from_file_location("opa4196_physical_geometry", GEOMETRY_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load physical geometry helpers: {GEOMETRY_PATH}")

geometry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = geometry
SPEC.loader.exec_module(geometry)

ROOT = Path("hardware/memory-core-prototype-a")
SHEET05 = ROOT / "05_MEMORY_GHOST_WET.kicad_sch"
SHEET06 = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"

MEMORY_POSITION = (101.60, 111.76)
GHOST_POSITION = (101.60, 165.10)
WET_POSITION = (261.62, 157.48)
RETURN_POSITION = (139.70, 114.30)
POWER_POSITION = (139.70, 160.02)

SHEET05_LABELS = (
    ("MEM_CTRL_BUFFER_IN", MEMORY_POSITION, "left", 1),
    ("MEM_CTRL_BUFFER_OUT", MEMORY_POSITION, "left", 3),
    ("MEM_CTRL_BUFFER_OUT", MEMORY_POSITION, "right", 2),
    ("GHOST_CTRL_BUFFER_IN", GHOST_POSITION, "left", 1),
    ("GHOST_CTRL_BUFFER_OUT", GHOST_POSITION, "left", 3),
    ("GHOST_CTRL_BUFFER_OUT", GHOST_POSITION, "right", 2),
    ("WET_CTRL_BUFFER_IN", WET_POSITION, "left", 1),
    ("WET_CTRL_BUFFER_OUT", WET_POSITION, "left", 3),
    ("WET_CTRL_BUFFER_OUT", WET_POSITION, "right", 2),
)

SHEET06_LABELS = (
    ("RETURN_CTRL_BUFFER_IN", RETURN_POSITION, "left", 1),
    ("RETURN_CTRL_BUFFER_OUT", RETURN_POSITION, "left", 3),
    ("RETURN_CTRL_BUFFER_OUT", RETURN_POSITION, "right", 2),
    ("RAIL_N12", POWER_POSITION, "left", 3),
    ("RAIL_P12", POWER_POSITION, "right", 2),
)


def repair(path: Path, labels: tuple[tuple[str, tuple[float, float], str, int], ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for name, position, side, row in labels:
        text = geometry.repair_label(text, name, position, side, row)
    path.write_text(text, encoding="utf-8")


def repair_sheet05() -> None:
    repair(SHEET05, SHEET05_LABELS)
    print("Corrected sheet-05 U63A/U63B/U63D physical pin attachments")


def repair_sheet06() -> None:
    repair(SHEET06, SHEET06_LABELS)
    print("Corrected sheet-06 U63C/common-power physical pin attachments")


def main() -> None:
    repair_sheet05()
    repair_sheet06()


if __name__ == "__main__":
    main()
