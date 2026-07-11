#!/usr/bin/env python3
"""Validate current V5.2 native-capture authority before or after sheet 09."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")

CAPTURED_BASE = (
    "01_POWER_PROTECTION_CAPTURED",
    "02_MCU_CLOCK_DEBUG_CAPTURED",
    "03_CODEC_CONVERSION_CAPTURED",
    "04_INPUT_PRESSURE_ABSENCE_CAPTURED",
    "05_MEMORY_GHOST_WET_CAPTURED",
    "06_RETURN_BREAK_LIMITER_CAPTURED",
    "07_OUTPUT_MUTE_PROTECTION_CAPTURED",
    "08_CONTROLS_STATE_CAPTURED",
)


def main() -> None:
    manifest = json.loads((ROOT / "hierarchy-manifest.json").read_text(encoding="utf-8"))
    assert manifest["stage"] == "hierarchy-and-interface-capture"
    assert len(manifest["sheets"]) == 9
    assert {sheet["code"] for sheet in manifest["sheets"]} == {
        f"{number:02d}" for number in range(1, 10)
    }

    expected_files = {sheet["filename"] for sheet in manifest["sheets"]}
    found_files = {path.name for path in ROOT.glob("[0-9][0-9]_*.kicad_sch")}
    assert found_files == expected_files, (found_files, expected_files)

    for marker in CAPTURED_BASE:
        assert (ROOT / marker).exists(), marker

    sheet07 = next(sheet for sheet in manifest["sheets"] if sheet["code"] == "07")
    assert sheet07["pins"] == [
        {"name": "RAIL_P12", "direction": "input"},
        {"name": "RAIL_N12", "direction": "input"},
        {"name": "DIRECT_PRESENT", "direction": "input"},
        {"name": "WET_MIX", "direction": "input"},
        {"name": "HARDWARE_FAULT_N", "direction": "input"},
    ]

    sheet09 = next(sheet for sheet in manifest["sheets"] if sheet["code"] == "09")
    assert sheet09["pins"] == [
        {"name": "RAIL_3V3", "direction": "input"},
        {"name": "HARDWARE_FAULT_N", "direction": "input"},
        {"name": "SHAPED_PRESENT", "direction": "input"},
        {"name": "ADC_ANALOG_IN", "direction": "input"},
        {"name": "RETURN_LIMITED", "direction": "input"},
        {"name": "RETURN_FEED", "direction": "input"},
        {"name": "ABSENCE_INFLUENCE", "direction": "input"},
        {"name": "WET_MIX", "direction": "input"},
    ]

    assert (ROOT / "MerrinLab_PrototypeA.kicad_sym").exists()
    assert (ROOT / "sym-lib-table").exists()

    if (ROOT / "09_TEST_SERVICE_CAPTURED").exists():
        print("Current schematic authority: all nine component sheets captured: PASS")
    else:
        print("Current schematic authority: eight captured sheets and sheet 09 scaffold: PASS")
    print("Sheet-07 and sheet-09 hierarchy manifest contracts: PASS")


if __name__ == "__main__":
    main()
