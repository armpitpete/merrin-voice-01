#!/usr/bin/env python3
"""Current entrypoint for 08_CONTROLS_STATE capture.

This wrapper applies reviewed generator/ERC repairs without changing the
accepted controls architecture:

- numeric-only resistor references;
- project-local generic NPN, potentiometer and LED symbols;
- application-specific TMUX1574 input/output electrical pin types;
- separated selector pull-down/release/fault-clamp placements;
- explicit global GND connection on the captured sheet.
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

GENERIC_POT = base.helpers.SymbolDefinition(
    "R_POT_123",
    "Generic panel potentiometer; exact mechanical part and footprint pending",
    "",
    (
        base.helpers.SymbolPin("1", "END_A", "passive", "left", 1),
        base.helpers.SymbolPin("3", "END_B", "passive", "left", 3),
        base.helpers.SymbolPin("2", "WIPER", "passive", "right", 2),
    ),
)

GENERIC_LED = base.helpers.SymbolDefinition(
    "LED_AK",
    "Generic low-current state LED; exact colour/device/footprint pending",
    "",
    (
        base.helpers.SymbolPin("1", "K", "passive", "left", 2),
        base.helpers.SymbolPin("2", "A", "passive", "right", 2),
    ),
)

APPLICATION_TMUX1574 = base.helpers.SymbolDefinition(
    "TMUX1574PW",
    "Four-channel 2:1 fail-safe selector; application directions; verified TSSOP-16 pin map",
    "https://www.ti.com/lit/ds/symlink/tmux1574.pdf",
    (
        base.helpers.SymbolPin("16", "VDD", "power_in", "left", 1),
        base.helpers.SymbolPin("15", "EN_N", "input", "left", 2),
        base.helpers.SymbolPin("1", "SEL", "input", "left", 3),
        base.helpers.SymbolPin("8", "GND", "power_in", "left", 4),
        base.helpers.SymbolPin("2", "S1A", "input", "left", 6),
        base.helpers.SymbolPin("3", "S1B", "input", "left", 7),
        base.helpers.SymbolPin("5", "S2A", "input", "left", 8),
        base.helpers.SymbolPin("6", "S2B", "input", "left", 9),
        base.helpers.SymbolPin("11", "S3A", "input", "left", 10),
        base.helpers.SymbolPin("10", "S3B", "input", "left", 11),
        base.helpers.SymbolPin("14", "S4A", "input", "left", 12),
        base.helpers.SymbolPin("13", "S4B", "input", "left", 13),
        base.helpers.SymbolPin("4", "D1", "output", "right", 6),
        base.helpers.SymbolPin("7", "D2", "output", "right", 8),
        base.helpers.SymbolPin("9", "D3", "output", "right", 10),
        base.helpers.SymbolPin("12", "D4", "output", "right", 12),
    ),
)


def append_repaired_symbols() -> None:
    base.TMUX1574 = APPLICATION_TMUX1574
    original_append_symbols()

    library = base.SYMBOL_LIBRARY
    text = library.read_text(encoding="utf-8")
    additions = []
    for definition in (GENERIC_NPN, GENERIC_POT, GENERIC_LED):
        if f'(symbol "{definition.name}"' not in text:
            additions.append(base.helpers.render_symbol(definition))

    if not additions:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    library.write_text(stripped[:-1] + "".join(additions) + ")\n", encoding="utf-8")


def corrected_add_part(sch, lib_id, reference, value, position, footprint=""):
    replacements = {
        "Transistor_BJT:Q_NPN_BCE": "MerrinLab_PrototypeA:Q_NPN_BCE",
        "Device:R_Potentiometer": "MerrinLab_PrototypeA:R_POT_123",
        "Device:LED": "MerrinLab_PrototypeA:LED_AK",
    }
    return original_add_part(
        sch,
        replacements.get(lib_id, lib_id),
        reference,
        value,
        position,
        footprint,
    )


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
    if reference == "R85":
        position = (152.40, 66.04)
    elif reference == "D81":
        position = (165.10, 73.66)

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


def establish_sheet_ground() -> None:
    sch = base.ksa.load_schematic(str(base.SHEET_FILE))
    references = {component.reference for component in sch.components}
    if "#PWR0801" not in references:
        ground = sch.components.add(
            "power:GND",
            "#PWR0801",
            "GND",
            position=(355.60, 170.18),
        )
        ground.in_bom = False
        ground.on_board = False
        pin = sch.get_component_pin_position("#PWR0801", "1")
        if pin is None:
            raise RuntimeError("Could not resolve sheet-08 global ground symbol")
        sch.add_label("GND", position=(pin.x, pin.y))
    sch.save(str(base.SHEET_FILE))


def main() -> None:
    base.append_project_symbols = append_repaired_symbols
    base.add_part = corrected_add_part
    base.add_two_pin = corrected_add_two_pin
    base.build()
    establish_sheet_ground()


if __name__ == "__main__":
    main()
