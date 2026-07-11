#!/usr/bin/env python3
"""Current entrypoint for 08_CONTROLS_STATE capture.

Repairs two generator-level issues without changing the electrical design:

- provisional resistor references are mapped to unique numeric references;
- the unavailable stock `Q_NPN_BCE` alias is replaced by a project-local
  generic base/collector/emitter symbol with no footprint.
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
original_add_part = base.add_part
original_append_symbols = base.append_project_symbols

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

GENERIC_NPN = base.helpers.SymbolDefinition(
    "Q_NPN_BCE",
    "Generic low-current NPN LED driver; exact transistor and footprint pending",
    "",
    (
        base.helpers.SymbolPin("1", "B", "input", "left", 2),
        base.helpers.SymbolPin("2", "C", "passive", "right", 1),
        base.helpers.SymbolPin("3", "E", "passive", "right", 3),
    ),
)


def append_generic_npn() -> None:
    original_append_symbols()
    library = base.SYMBOL_LIBRARY
    text = library.read_text(encoding="utf-8")
    if f'(symbol "{GENERIC_NPN.name}"' in text:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    updated = stripped[:-1] + base.helpers.render_symbol(GENERIC_NPN) + ")\n"
    library.write_text(updated, encoding="utf-8")


def corrected_add_part(sch, lib_id, reference, value, position, footprint=""):
    if lib_id == "Transistor_BJT:Q_NPN_BCE":
        lib_id = "MerrinLab_PrototypeA:Q_NPN_BCE"
    return original_add_part(sch, lib_id, reference, value, position, footprint)


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
    base.append_project_symbols = append_generic_npn
    base.add_part = corrected_add_part
    base.add_two_pin = corrected_add_two_pin
    base.build()


if __name__ == "__main__":
    main()
