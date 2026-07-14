#!/usr/bin/env python3
"""Add the missing controls-sheet interfaces before sheet 08 capture.

The accepted MCU pin allocation reserves eight ADC inputs and three operating
inputs, but the first hierarchy scaffold did not expose them between
08_CONTROLS_STATE and 02_MCU_CLOCK_DEBUG.

This amendment:
- adds those signals to the two hierarchical sheets and top-level nets;
- connects the MCU-side labels to a temporary non-BOM/non-board harness;
- establishes the power sheet's ground net as KiCad's global GND;
- preserves the project-local TI symbols while resaving sheet 01;
- updates the machine-readable interface manifest.

It does not alter any accepted audio or Return boundary.
"""

from __future__ import annotations

import json
from pathlib import Path

import kicad_sch_api as ksa
from kicad_sch_api.core.types import HierarchicalLabelShape

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP_FILE = ROOT / f"{PROJECT}.kicad_sch"
POWER_FILE = ROOT / "01_POWER_PROTECTION.kicad_sch"
MCU_FILE = ROOT / "02_MCU_CLOCK_DEBUG.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MANIFEST_FILE = ROOT / "hierarchy-manifest.json"
MARKER = ROOT / "CONTROLS_INTERFACES_AMENDED"

PANEL_SIGNALS = (
    "PANEL_MEMORY_TIME",
    "PANEL_MEMORY_FADE",
    "PANEL_MEMORY_BLUR",
    "PANEL_GHOST_DISTANCE",
    "PANEL_GHOST_DRIFT",
    "PANEL_GHOST_PRESENCE",
    "PANEL_RETURN_AMOUNT",
    "PANEL_PRESENT_WET",
)

OPERATING_SIGNALS = (
    "SERVICE_TEST",
    "RESET_CLEAR",
    "SAFE_MUTE",
)

ALL_SIGNALS = PANEL_SIGNALS + OPERATING_SIGNALS


def actual_pin_position(sheet: dict, side: str, offset: float) -> tuple[float, float]:
    x = sheet["position"]["x"]
    y = sheet["position"]["y"]
    width = sheet["size"]["width"]
    height = sheet["size"]["height"]

    if side == "left":
        return (x, y + height - offset)
    if side == "right":
        return (x + width, y + offset)
    raise ValueError(f"Unsupported side: {side}")


def find_sheet(top: ksa.Schematic, filename: str) -> dict:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == filename:
            return sheet
    raise RuntimeError(f"Sheet not found: {filename}")


def add_sheet_signals(
    top: ksa.Schematic,
    sheet: dict,
    signals: tuple[str, ...],
    pin_type: str,
    side: str,
) -> None:
    existing = {pin["name"] for pin in sheet.get("pins", [])}
    wanted_rotation = 180 if side == "left" else 0
    side_pins = [
        pin for pin in sheet.get("pins", [])
        if pin.get("rotation") == wanted_rotation
    ]
    next_offset = 5.08 + 2.54 * len(side_pins)

    for signal in signals:
        if signal in existing:
            continue
        top.sheets.add_sheet_pin(
            sheet["uuid"],
            signal,
            pin_type,
            side,
            next_offset,
        )
        top.add_label(signal, position=actual_pin_position(sheet, side, next_offset))
        next_offset += 2.54


def amend_mcu_scaffold() -> None:
    sch = ksa.load_schematic(str(MCU_FILE))
    existing = {label.text for label in sch.hierarchical_labels}
    pending = [signal for signal in ALL_SIGNALS if signal not in existing]

    if pending:
        harness = sch.components.add(
            "Connector_Generic:Conn_01x11",
            "J912",
            "CONTROLS_TO_MCU_NOT_FITTED",
            position=(170.18, 160.02),
        )
        harness.in_bom = False
        harness.on_board = False
        harness.footprint = ""
        harness.add_property("Purpose", "Temporary controls hierarchy/ERC harness", hidden=True)

        for number, signal in enumerate(ALL_SIGNALS, start=1):
            pin = sch.get_component_pin_position("J912", str(number))
            if pin is None:
                raise RuntimeError(f"Could not resolve temporary MCU harness pin {number}")
            label_at = (pin.x - 20.32, pin.y)
            sch.add_wire(start=(pin.x, pin.y), end=label_at)
            sch.add_hierarchical_label(
                signal,
                position=label_at,
                shape=HierarchicalLabelShape.INPUT,
                size=1.27,
            )

    sch.add_text(
        "PANEL / OPERATING INPUTS ADDED BY V5.2 CONTROLS INTERFACE AMENDMENT\n"
        "J912 is a temporary non-BOM/non-board harness until MCU capture.",
        position=(35.56, 109.22),
        size=1.27,
    )
    sch.save(str(MCU_FILE))


def establish_global_ground() -> None:
    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))

    sch = ksa.load_schematic(str(POWER_FILE))
    references = {component.reference for component in sch.components}
    if "#PWR0101" not in references:
        ground = sch.components.add(
            "power:GND",
            "#PWR0101",
            "GND",
            position=(20.32, 114.30),
        )
        ground.in_bom = False
        ground.on_board = False
        pin = sch.get_component_pin_position("#PWR0101", "1")
        if pin is None:
            raise RuntimeError("Could not resolve global GND power symbol")
        sch.add_label("GND", position=(pin.x, pin.y))
        sch.add_text(
            "Global GND established here and driven by the existing ground PWR_FLAG.",
            position=(20.32, 121.92),
            size=1.27,
        )
    sch.save(str(POWER_FILE))


def amend_manifest() -> None:
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))

    sheet02 = next(sheet for sheet in manifest["sheets"] if sheet["code"] == "02")
    sheet08 = next(sheet for sheet in manifest["sheets"] if sheet["code"] == "08")

    def add_manifest_pins(sheet: dict, direction: str) -> None:
        existing = {pin["name"] for pin in sheet["pins"]}
        for signal in ALL_SIGNALS:
            if signal not in existing:
                sheet["pins"].append({"name": signal, "direction": direction})

    add_manifest_pins(sheet02, "input")
    add_manifest_pins(sheet08, "output")

    manifest["controls_interface_amendment"] = {
        "reason": "Expose accepted eight panel ADC signals and three operating inputs between sheets 08 and 02.",
        "panel_signals": list(PANEL_SIGNALS),
        "operating_signals": list(OPERATING_SIGNALS),
        "mcu_scaffold_harness": "J912 — temporary, non-BOM, non-board",
        "global_ground_source": "01_POWER_PROTECTION",
    }

    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    top = ksa.load_schematic(str(TOP_FILE))
    sheet02 = find_sheet(top, MCU_FILE.name)
    sheet08 = find_sheet(top, "08_CONTROLS_STATE.kicad_sch")

    add_sheet_signals(top, sheet02, ALL_SIGNALS, "input", "left")
    add_sheet_signals(top, sheet08, ALL_SIGNALS, "output", "right")
    top.save(str(TOP_FILE))

    amend_mcu_scaffold()
    establish_global_ground()
    amend_manifest()

    MARKER.write_text(
        "Eight panel controls and three operating inputs added between sheets 08 and 02; global GND established.\n",
        encoding="utf-8",
    )

    print("Controls/state hierarchy interfaces amended.")
    for signal in ALL_SIGNALS:
        print(signal)


if __name__ == "__main__":
    main()
