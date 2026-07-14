#!/usr/bin/env python3
"""Expose the accepted Return-sheet safety interfaces.

Sheet 06 needs the 3.3 V clamp reference and active-low hardware-fault net for:

- local SSI2164 control-input clamps;
- bounded ABSENCE_INFLUENCE output;
- immediate neutralisation of Return-derived control during fault.

This amendment changes hierarchy/interface metadata only. It does not add PCB,
footprint, fabrication, purchasing, or mechanical authority.
"""

from __future__ import annotations

import json
from pathlib import Path

import kicad_sch_api as ksa

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP_FILE = ROOT / f"{PROJECT}.kicad_sch"
MANIFEST_FILE = ROOT / "hierarchy-manifest.json"
MARKER = ROOT / "RETURN_SAFETY_INTERFACES_AMENDED"
SHEET_FILE = "06_RETURN_BREAK_LIMITER.kicad_sch"
SIGNALS = (
    ("RAIL_3V3", "input"),
    ("HARDWARE_FAULT_N", "input"),
)


def actual_pin_position(sheet: dict, side: str, offset: float) -> tuple[float, float]:
    x = sheet["position"]["x"]
    y = sheet["position"]["y"]
    width = sheet["size"]["width"]
    height = sheet["size"]["height"]
    if side == "left":
        return (x, y + height - offset)
    if side == "right":
        return (x + width, y + offset)
    raise ValueError(side)


def find_sheet(top: ksa.Schematic) -> dict:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE:
            return sheet
    raise RuntimeError(f"Sheet not found: {SHEET_FILE}")


def amend_top() -> None:
    top = ksa.load_schematic(str(TOP_FILE))
    sheet = find_sheet(top)
    existing = {pin["name"] for pin in sheet.get("pins", [])}
    left_pins = [pin for pin in sheet.get("pins", []) if pin.get("rotation") == 180]
    next_offset = 5.08 + 2.54 * len(left_pins)

    for name, direction in SIGNALS:
        if name in existing:
            continue
        top.sheets.add_sheet_pin(sheet["uuid"], name, direction, "left", next_offset)
        top.add_label(name, position=actual_pin_position(sheet, "left", next_offset))
        next_offset += 2.54

    top.save(str(TOP_FILE))


def amend_manifest() -> None:
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    sheet = next(item for item in manifest["sheets"] if item["code"] == "06")
    existing = {pin["name"] for pin in sheet["pins"]}
    for name, direction in SIGNALS:
        if name not in existing:
            sheet["pins"].append({"name": name, "direction": direction})

    manifest["return_safety_interface_amendment"] = {
        "reason": (
            "Sheet 06 requires RAIL_3V3 for bounded control clamps and "
            "HARDWARE_FAULT_N to neutralise ABSENCE_INFLUENCE during fault."
        ),
        "signals": [name for name, _ in SIGNALS],
        "scope": "06_RETURN_BREAK_LIMITER only",
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    amend_top()
    amend_manifest()
    MARKER.write_text(
        "RAIL_3V3 and HARDWARE_FAULT_N added to 06_RETURN_BREAK_LIMITER hierarchy.\n",
        encoding="utf-8",
    )
    print("Return safety hierarchy amendment complete.")


if __name__ == "__main__":
    main()
