#!/usr/bin/env python3
"""Run sheet 07 with project-local provisional NPN and output-pot symbols.

KiCad 10's installed stock libraries do not provide the generic symbol IDs used
by the reviewed generator. This wrapper substitutes application symbols with
explicit logical pins and blank footprints. Electrical topology and values are
unchanged; exact devices, packages and footprints remain blocked.
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

ORIGINAL_APPEND = base.append_symbols
ORIGINAL_ADD_PART = base.add_part

NPN = base.helpers.SymbolDefinition(
    "NPN_FAULT_INVERTER_APPLICATION",
    "Provisional NPN fault inverter; logical B/C/E pins; exact device and footprint pending",
    "",
    (
        base.helpers.SymbolPin("1", "BASE", "input", "left", 2),
        base.helpers.SymbolPin("2", "COLLECTOR", "passive", "right", 1),
        base.helpers.SymbolPin("3", "EMITTER", "passive", "right", 3),
    ),
)

OUTPUT_POT = base.helpers.SymbolDefinition(
    "OUTPUT_LEVEL_POT_APPLICATION",
    "10k output-level potentiometer; logical low/wiper/high pins; physical part pending",
    "",
    (
        base.helpers.SymbolPin("1", "LOW", "passive", "left", 3),
        base.helpers.SymbolPin("2", "WIPER", "passive", "right", 2),
        base.helpers.SymbolPin("3", "HIGH", "passive", "left", 1),
    ),
)


def append_application_symbol(definition) -> None:
    text = base.SYMBOL_LIBRARY.read_text(encoding="utf-8")
    if f'(symbol "{definition.name}"' in text:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    base.SYMBOL_LIBRARY.write_text(
        stripped[:-1] + base.helpers.render_symbol(definition) + ")\n",
        encoding="utf-8",
    )


def append_symbols() -> None:
    ORIGINAL_APPEND()
    append_application_symbol(NPN)
    append_application_symbol(OUTPUT_POT)


def corrected_add_part(sch, lib_id, reference, value, position, footprint="", unit=1):
    if lib_id in {"Transistor_BJT:Q_NPN_BCE", "Device:Q_NPN_BCE"}:
        lib_id = "MerrinLab_PrototypeA:NPN_FAULT_INVERTER_APPLICATION"
    elif lib_id == "Device:R_Potentiometer":
        lib_id = "MerrinLab_PrototypeA:OUTPUT_LEVEL_POT_APPLICATION"
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
    base.append_symbols = append_symbols
    base.add_part = corrected_add_part
    base.build()
    print("Sheet-07 provisional NPN and output pot resolved through project symbols")


if __name__ == "__main__":
    main()
