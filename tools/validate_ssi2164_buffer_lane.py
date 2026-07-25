#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")

def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def number_pattern(value: float) -> str:
    integer = int(value)
    if value == integer:
        return rf"{integer}(?:\.0+)?"
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return re.escape(text)


COINCIDENT_LABEL_COUNTS = {
    ("MEM_CTRL_BUFFER_IN", 91.44, 107.95): 2,
    ("GHOST_CTRL_BUFFER_IN", 91.44, 161.29): 2,
}


def assert_label_at(text: str, name: str, x: float, y: float) -> None:
    pattern = (
        rf'\(label "{re.escape(name)}"\s+\(at '
        rf'{number_pattern(x)} {number_pattern(y)} 0(?:\.0+)?\)'
    )
    count = len(re.findall(pattern, text, re.MULTILINE))
    expected_count = COINCIDENT_LABEL_COUNTS.get((name, x, y), 1)
    assert count == expected_count, (name, x, y, expected_count, count)


def main() -> None:
    assert blob(ROOT / "08_CONTROLS_STATE.kicad_sch") == "2d681089ed95fada6f476060cb6163311a3fde45"
    assert blob(ROOT / "MerrinGriefSynthMemoryCoreA.kicad_sch") == "8ef352f7a72197214e34dacdf998046382589937"
    assert blob(Path("tools/capture_controls_state_sheet.py")) == "0485f51b3c78ab95aa8b8f94d01b8aeedc73d188"

    audit = json.loads((ROOT / "SSI2164_BUFFER_AUDIT.json").read_text())
    assert audit["buffer"]["part"] == "OPA4196"
    assert audit["buffer"]["footprint_assigned"] is False
    assert audit["ssi2164"]["footprint_assigned"] is False
    assert audit["calculation"]["nominal_attenuation_db"] > 99.7
    assert audit["calculation"]["lower_reference_attenuation_db"] > 98.0
    assert all(value is False for value in audit["authority"].values())

    library = (ROOT / "MerrinLab_PrototypeA.kicad_sym").read_text()
    for unit in range(1, 6):
        assert f'(symbol "OPA4196_PW_MULTI_{unit}_1"' in library
    assert 'property "Footprint" ""' in library

    sheet05 = (ROOT / "05_MEMORY_GHOST_WET.kicad_sch").read_text()
    sheet06 = (ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch").read_text()
    for token in ("R525", "R526", "R527", "20R buffer isolate", "D500", "D505"):
        assert token in sheet05, token
    for token in ("R604A", "20R buffer isolate", "C642", "C643", "D600", "D601"):
        assert token in sheet06, token
    assert sheet05.count('property "Reference" "U63"') == 3
    assert sheet06.count('property "Reference" "U63"') == 2

    for name, x, y in (
        ("MEM_CTRL_BUFFER_IN", 91.44, 107.95),
        ("MEM_CTRL_BUFFER_OUT", 91.44, 113.03),
        ("MEM_CTRL_BUFFER_OUT", 111.76, 110.49),
        ("GHOST_CTRL_BUFFER_IN", 91.44, 161.29),
        ("GHOST_CTRL_BUFFER_OUT", 91.44, 166.37),
        ("GHOST_CTRL_BUFFER_OUT", 111.76, 163.83),
        ("WET_CTRL_BUFFER_IN", 251.46, 153.67),
        ("WET_CTRL_BUFFER_OUT", 251.46, 158.75),
        ("WET_CTRL_BUFFER_OUT", 271.78, 156.21),
    ):
        assert_label_at(sheet05, name, x, y)

    for name, x, y in (
        ("RETURN_CTRL_BUFFER_IN", 129.54, 110.49),
        ("RETURN_CTRL_BUFFER_OUT", 129.54, 115.57),
        ("RETURN_CTRL_BUFFER_OUT", 149.86, 113.03),
        ("RAIL_N12", 129.54, 161.29),
        ("RAIL_P12", 149.86, 158.75),
    ):
        assert_label_at(sheet06, name, x, y)

    assert sheet05.count('property "Footprint" ""') > 0
    assert sheet06.count('property "Footprint" ""') > 0

    print("OPA4196 shared five-unit symbol and ownership: PASS")
    print("SSI2164 buffered 20-ohm control law: PASS")
    print("Sheet 08 and top-level hierarchy unchanged: PASS")
    print("Footprints and downstream authority remain blocked: PASS")

if __name__ == "__main__":
    main()
