#!/usr/bin/env python3
"""Add the missing controls-sheet interfaces before sheet 08 capture.

The accepted MCU pin allocation reserves eight ADC inputs and three operating
inputs, but the first hierarchy scaffold did not expose them between
08_CONTROLS_STATE and 02_MCU_CLOCK_DEBUG. This amendment adds those signals to
both hierarchical sheets, the top-level nets, the MCU scaffold and the machine-
readable manifest.

It does not alter 01_POWER_PROTECTION or any accepted audio boundary.
"""

from __future__ import annotations

import json
from pathlib import Path

import kicad_sch_api as ksa
from kicad_sch_api.core.types import HierarchicalLabelShape

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP_FILE = ROOT / f"{PROJECT}.kicad_sch"
MCU_FILE = ROOT / "02_MCU_CLOCK_DEBUG.kicad_sch"
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
    side_pins = [pin for pin in sheet.get("pins", []) if pin.get("rotation") == (180 if side == "left" else 0)]
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
        label_at = actual_pin_position(sheet, side, next_offset)
        top.add_label(signal, position=label_at)
        next_offset += 2.54


def amend_mcu_scaffold() -> None:
    sch = ksa.load_schematic(str(MCU_FILE))
    existing = {
        label.text for label in sch.hierarchical_labels
    }

    y = 119.38
    for signal in ALL_SIGNALS:
        if signal in existing:
            continue
        sch.add_hierarchical_label(
            signal,
            position=(45.72, y),
            shape=HierarchicalLabelShape.INPUT,
            size=1.27,
        )
        y += 5.08

    sch.add_text(
        "PANEL / OPERATING INPUTS ADDED BY V5.2 CONTROLS INTERFACE AMENDMENT\n"
        "Temporary isolated labels remain until 02_MCU_CLOCK_DEBUG is captured.",
        position=(35.56, 109.22),
        size=1.27,
    )
    sch.save(str(MCU_FILE))


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
    amend_manifest()

    MARKER.write_text(
        "Eight panel controls and three operating inputs added between sheets 08 and 02.\n",
        encoding="utf-8",
    )

    print("Controls/state hierarchy interfaces amended.")
    for signal in ALL_SIGNALS:
        print(signal)


if __name__ == "__main__":
    main()
