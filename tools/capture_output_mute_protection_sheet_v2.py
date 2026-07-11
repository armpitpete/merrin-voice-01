#!/usr/bin/env python3
"""Run the reviewed sheet-07 capture with the KiCad-10 generic NPN library ID.

The reviewed generator used the correct generic symbol name but the wrong stock
library namespace. KiCad 10 provides Q_NPN_BCE in Device, not Transistor_BJT.
No electrical topology, pin order, values or boundary signals are changed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_output_mute_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("output_mute_protection_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load output capture: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

ORIGINAL_ADD_PART = base.add_part


def corrected_add_part(sch, lib_id, reference, value, position, footprint="", unit=1):
    if lib_id == "Transistor_BJT:Q_NPN_BCE":
        lib_id = "Device:Q_NPN_BCE"
    return ORIGINAL_ADD_PART(
        sch,
        lib_id,
        reference,
        value,
        position,
        footprint,
        unit,
    )


def main() -> None:
    base.add_part = corrected_add_part
    base.build()
    print("Sheet-07 generic NPN resolved through Device:Q_NPN_BCE")


if __name__ == "__main__":
    main()
