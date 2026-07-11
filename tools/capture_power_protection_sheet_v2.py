#!/usr/bin/env python3
"""Compatibility wrapper for the power/protection capture generator.

KiCad's stock Device library names the ferrite symbol `L_Ferrite`. The base
capture script used the descriptive but nonexistent alias `Ferrite_Bead`.
This wrapper maps only that stock-library name; circuit content is unchanged.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


BASE_PATH = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("power_protection_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load base capture script: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

original_add_part = base.add_part


def corrected_add_part(sch, lib_id, reference, value, position, footprint=""):
    if lib_id == "Device:Ferrite_Bead":
        lib_id = "Device:L_Ferrite"
    return original_add_part(sch, lib_id, reference, value, position, footprint)


def main() -> None:
    base.add_part = corrected_add_part
    base.build_power_sheet()


if __name__ == "__main__":
    main()
