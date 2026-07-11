#!/usr/bin/env python3
"""ERC repair wrapper for 01_POWER_PROTECTION.

Repairs the component-level KiCad 10 findings:

- use KiCad's stock `Device:L_Ferrite` symbol;
- move R6 so it cannot physically join R5's CT node;
- add source annotations only after passive protection/conversion boundaries.

`RAIL_5V_CODEC` is driven directly by the TPS7A2050 power-output pin and must
not receive a second PWR_FLAG.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import kicad_sch_api as ksa


BASE_PATH = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("power_protection_capture_base_v3", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load base capture script: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

original_add_part = base.add_part
original_add_two_pin = base.add_two_pin


def corrected_add_part(sch, lib_id, reference, value, position, footprint=""):
    if lib_id == "Device:Ferrite_Bead":
        lib_id = "Device:L_Ferrite"
    return original_add_part(sch, lib_id, reference, value, position, footprint)


def corrected_add_two_pin(
    sch,
    lib_id,
    reference,
    value,
    position,
    net_1,
    net_2,
    footprint="",
):
    if reference == "R6":
        position = (251.46, 91.44)
    return original_add_two_pin(
        sch,
        lib_id,
        reference,
        value,
        position,
        net_1,
        net_2,
        footprint,
    )


def add_power_flag(sch: ksa.Schematic, reference: str, net: str, position) -> None:
    base.add_part(sch, "power:PWR_FLAG", reference, "PWR_FLAG", position)
    base.label_pin(sch, reference, "1", net)


def main() -> None:
    base.add_part = corrected_add_part
    base.add_two_pin = corrected_add_two_pin
    base.build_power_sheet()

    sch = ksa.load_schematic(str(base.POWER_SHEET))
    for reference, net, position in (
        ("#FLG04", "RAIL_P12", (137.16, 76.20)),
        ("#FLG05", "RAIL_N12", (137.16, 106.68)),
        ("#FLG06", "RAIL_3V3", (248.92, 66.04)),
        ("#FLG07", "RAIL_5V45_PRE", (248.92, 116.84)),
    ):
        add_power_flag(sch, reference, net, position)

    sch.add_text(
        "PWR_FLAG markers identify rails after passive protection/conversion boundaries for ERC.\n"
        "RAIL_5V_CODEC is driven directly by U3 and needs no source annotation.",
        position=(251.46, 167.64),
        size=1.27,
    )
    sch.save(str(base.POWER_SHEET))
    print("Applied final power-source annotations and supervisor spacing repair.")


if __name__ == "__main__":
    main()
