#!/usr/bin/env python3
"""Complete staged SSI2164 unit placement for sheet-06 ERC.

KiCad ERC requires every unit of a multi-unit device to be placed. Sheet 06 owns
SSI2164 channel 3 and the common power unit; channels 1, 2 and 4 will become the
Memory, Ghost and wet-master channels on sheet 05.

This staged repair:

1. applies the reviewed physical-pin attachment correction;
2. places U60 units 1, 2 and 4 visibly on sheet 06;
3. marks every reserved pin explicitly no-connect;
4. labels them as temporary reservations for sheet 05.

The units share the same U60 reference and therefore do not duplicate the chip.
They must be removed from sheet 06 when their real sheet-05 circuits are placed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import kicad_sch_api as ksa

BASE_PATH = Path(__file__).with_name("repair_return_ssi_units.py")
SPEC = importlib.util.spec_from_file_location("return_ssi_physical_repair", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load SSI2164 repair: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

ROOT = Path("hardware/memory-core-prototype-a")
SHEET_FILE = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
LIB_ID = "MerrinLab_PrototypeA:SSI2164S_MULTI"
HALF_HEIGHT = 6.35

# Unit -> (position, pins as (number, side, row)).
RESERVED_UNITS = {
    1: ((370.84, 205.74), (("2", "left", 1), ("3", "left", 3), ("4", "right", 2))),
    2: ((370.84, 231.14), (("7", "left", 1), ("6", "left", 3), ("5", "right", 2))),
    4: ((370.84, 256.54), (("10", "left", 1), ("11", "left", 3), ("12", "right", 2))),
}


def actual_pin_position(
    position: tuple[float, float], side: str, row: int
) -> tuple[float, float]:
    local_y = HALF_HEIGHT - 2.54 * row
    x = position[0] - 10.16 if side == "left" else position[0] + 10.16
    y = position[1] - local_y
    return (round(x, 2), round(y, 2))


def place_reserved_units() -> None:
    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))
    sch = ksa.load_schematic(str(SHEET_FILE))

    existing_units = {
        component._data.unit
        for component in sch.components
        if component.reference == "U60" and component.lib_id.endswith("SSI2164S_MULTI")
    }
    if existing_units != {3, 5}:
        raise RuntimeError(f"Expected U60 units 3 and 5 before reservations, found {existing_units}")

    for unit, (position, pins) in RESERVED_UNITS.items():
        component = sch.components.add(
            lib_id=LIB_ID,
            reference="U60",
            value="SSI2164",
            position=position,
            unit=unit,
        )
        component.in_bom = True
        component.on_board = True
        for _number, side, row in pins:
            sch.no_connects.add(position=actual_pin_position(position, side, row))

    sch.add_text(
        "U60 units 1, 2 and 4 are visible staged reservations for sheet 05.\n"
        "They are the same physical SSI2164 as units 3 and 5, not duplicate chips.\n"
        "Sheet 05 must remove these reservations and place the real Memory/Ghost/Wet circuits.",
        position=(322.58, 276.86),
        size=1.0,
    )
    sch.save(str(SHEET_FILE))


def main() -> None:
    base.main()
    place_reserved_units()
    print("Placed visible U60 units 1, 2 and 4 as staged sheet-05 reservations")


if __name__ == "__main__":
    main()
