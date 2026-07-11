#!/usr/bin/env python3
"""Current entrypoint for 08_CONTROLS_STATE capture.

The base generator's provisional output-isolation and panel-filter resistor
references used trailing letters. This wrapper maps them to unique numeric
references before native capture. Circuit values and nets are unchanged.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


BASE_PATH = Path(__file__).with_name("capture_controls_state_sheet.py")
SPEC = importlib.util.spec_from_file_location("controls_state_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load controls capture generator: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

original_add_two_pin = base.add_two_pin
REFERENCE_MAP = {
    "R86A": "R90",
    "R87A": "R91",
    "R88A": "R92",
    "R89A": "R93",
    "R91A": "R150",
    "R92A": "R151",
    "R93A": "R152",
    "R94A": "R153",
    "R95A": "R154",
    "R96A": "R155",
    "R97A": "R156",
    "R98A": "R157",
}


def corrected_add_two_pin(
    sch,
    lib_id,
    reference,
    value,
    position,
    net1,
    net2,
    footprint="",
):
    return original_add_two_pin(
        sch,
        lib_id,
        REFERENCE_MAP.get(reference, reference),
        value,
        position,
        net1,
        net2,
        footprint,
    )


def main() -> None:
    base.add_two_pin = corrected_add_two_pin
    base.build()


if __name__ == "__main__":
    main()
