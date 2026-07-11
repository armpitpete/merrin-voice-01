#!/usr/bin/env python3
"""Expose the accepted ±12 V rails on 03_CODEC_CONVERSION.

The first hierarchy scaffold gave the codec sheet only 3.3 V and quiet 5 V.
The accepted OPA1679 conversion stages require RAIL_P12 and RAIL_N12.
This amendment adds those two inputs to sheet 03, labels them on the top sheet,
and updates the machine-readable manifest. It does not change any audio or
Return boundary.
"""

from __future__ import annotations

import json
from pathlib import Path

import kicad_sch_api as ksa

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP_FILE = ROOT / f"{PROJECT}.kicad_sch"
MANIFEST_FILE = ROOT / "hierarchy-manifest.json"
MARKER = ROOT / "CODEC_ANALOG_RAILS_AMENDED"
SHEET_FILE = "03_CODEC_CONVERSION.kicad_sch"
RAILS = ("RAIL_P12", "RAIL_N12")


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

    for rail in RAILS:
        if rail in existing:
            continue
        top.sheets.add_sheet_pin(sheet["uuid"], rail, "input", "left", next_offset)
        top.add_label(rail, position=actual_pin_position(sheet, "left", next_offset))
        next_offset += 2.54

    top.save(str(TOP_FILE))


def amend_manifest() -> None:
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    sheet = next(item for item in manifest["sheets"] if item["code"] == "03")
    existing = {pin["name"] for pin in sheet["pins"]}
    for rail in RAILS:
        if rail not in existing:
            sheet["pins"].append({"name": rail, "direction": "input"})

    manifest["codec_analogue_rail_amendment"] = {
        "reason": "OPA1679 converter-boundary stages use the accepted ±12 V analogue rails.",
        "rails": list(RAILS),
        "scope": "03_CODEC_CONVERSION only",
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    amend_top()
    amend_manifest()
    MARKER.write_text(
        "RAIL_P12 and RAIL_N12 added to 03_CODEC_CONVERSION hierarchy.\n",
        encoding="utf-8",
    )
    print("Codec analogue rail hierarchy amendment complete.")


if __name__ == "__main__":
    main()
