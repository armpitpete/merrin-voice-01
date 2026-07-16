#!/usr/bin/env python3
"""Add the bounded, reproducible U63 OPA4196 coordinate repair.

This temporary patch runs only after apply_ssi2164_buffer_patch.py. It creates the
permanent coordinate-repair tool, wires that tool into the two authoritative
sheet wrappers, and strengthens the generated lane validator with exact physical
pin-coordinate assertions. It does not alter circuit topology or values.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPAIR_PATH = Path("tools/repair_ssi2164_buffer_opa4196_units.py")
VALIDATOR_PATH = Path("tools/validate_ssi2164_buffer_lane.py")

EXPECTED_BLOBS = {
    Path("tools/apply_ssi2164_buffer_patch.py"): "a698d296d7937d4d01744b603fa01563a4da9f4b",
    Path("tools/capture_memory_ghost_wet_sheet_v2.py"): "bc8055d41a1a22a1477fbae9af4b38b8d357a3c0",
    Path("tools/capture_return_break_limiter_sheet_v3.py"): "8826698d3210a73aa954c2801a5a1e5c8c59efe4",
    Path("tools/repair_return_ssi_units.py"): "8e45dd9a531c0805f34442afe8ae989a6dee2a30",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def assert_sources() -> None:
    for path, expected in EXPECTED_BLOBS.items():
        actual = git_blob(path)
        if actual != expected:
            raise RuntimeError(f"Unexpected source blob for {path}: {actual} != {expected}")
    if not VALIDATOR_PATH.exists():
        raise RuntimeError("First SSI2164 buffer patch did not create the lane validator")
    if REPAIR_PATH.exists():
        raise RuntimeError(f"Coordinate repair tool already exists: {REPAIR_PATH}")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match in {path}, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def write_repair_tool() -> None:
    content = '''#!/usr/bin/env python3
"""Correct U63 OPA4196 multi-unit pin attachments after native generation.

The pinned schematic API mirrors Y coordinates returned for custom multi-unit
symbol pins. This repair moves only the U63 input, feedback, output and common-
power labels to the physical OPA4196 pin coordinates. Circuit topology, values,
references and footprints are not changed.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

GEOMETRY_PATH = Path(__file__).with_name("repair_return_ssi_units.py")
SPEC = importlib.util.spec_from_file_location("opa4196_physical_geometry", GEOMETRY_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load physical geometry helpers: {GEOMETRY_PATH}")

geometry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = geometry
SPEC.loader.exec_module(geometry)

ROOT = Path("hardware/memory-core-prototype-a")
SHEET05 = ROOT / "05_MEMORY_GHOST_WET.kicad_sch"
SHEET06 = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"

MEMORY_POSITION = (101.60, 111.76)
GHOST_POSITION = (101.60, 165.10)
WET_POSITION = (261.62, 157.48)
RETURN_POSITION = (139.70, 114.30)
POWER_POSITION = (139.70, 160.02)

SHEET05_LABELS = (
    ("MEM_CTRL_BUFFER_IN", MEMORY_POSITION, "left", 1),
    ("MEM_CTRL_BUFFER_OUT", MEMORY_POSITION, "left", 3),
    ("MEM_CTRL_BUFFER_OUT", MEMORY_POSITION, "right", 2),
    ("GHOST_CTRL_BUFFER_IN", GHOST_POSITION, "left", 1),
    ("GHOST_CTRL_BUFFER_OUT", GHOST_POSITION, "left", 3),
    ("GHOST_CTRL_BUFFER_OUT", GHOST_POSITION, "right", 2),
    ("WET_CTRL_BUFFER_IN", WET_POSITION, "left", 1),
    ("WET_CTRL_BUFFER_OUT", WET_POSITION, "left", 3),
    ("WET_CTRL_BUFFER_OUT", WET_POSITION, "right", 2),
)

SHEET06_LABELS = (
    ("RETURN_CTRL_BUFFER_IN", RETURN_POSITION, "left", 1),
    ("RETURN_CTRL_BUFFER_OUT", RETURN_POSITION, "left", 3),
    ("RETURN_CTRL_BUFFER_OUT", RETURN_POSITION, "right", 2),
    ("RAIL_N12", POWER_POSITION, "left", 3),
    ("RAIL_P12", POWER_POSITION, "right", 2),
)


def repair(path: Path, labels: tuple[tuple[str, tuple[float, float], str, int], ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for name, position, side, row in labels:
        text = geometry.repair_label(text, name, position, side, row)
    path.write_text(text, encoding="utf-8")


def repair_sheet05() -> None:
    repair(SHEET05, SHEET05_LABELS)
    print("Corrected sheet-05 U63A/U63B/U63D physical pin attachments")


def repair_sheet06() -> None:
    repair(SHEET06, SHEET06_LABELS)
    print("Corrected sheet-06 U63C/common-power physical pin attachments")


def main() -> None:
    repair_sheet05()
    repair_sheet06()


if __name__ == "__main__":
    main()
'''
    REPAIR_PATH.write_text(content, encoding="utf-8")


def patch_wrappers() -> None:
    memory = Path("tools/capture_memory_ghost_wet_sheet_v2.py")
    replace_once(
        memory,
        '''physical = load(
    "memory_ghost_wet_ssi_repair",
    Path(__file__).with_name("repair_memory_ghost_wet_ssi_units.py"),
)
''',
        '''physical = load(
    "memory_ghost_wet_ssi_repair",
    Path(__file__).with_name("repair_memory_ghost_wet_ssi_units.py"),
)
buffer = load(
    "memory_ghost_wet_opa4196_repair",
    Path(__file__).with_name("repair_ssi2164_buffer_opa4196_units.py"),
)
''',
    )
    replace_once(
        memory,
        '''    base.build()
    physical.main()
    repair_output_directions(base.SHEET_FILE, base.HIER_OUTPUTS)
''',
        '''    base.build()
    physical.main()
    buffer.repair_sheet05()
    repair_output_directions(base.SHEET_FILE, base.HIER_OUTPUTS)
''',
    )

    ret = Path("tools/capture_return_break_limiter_sheet_v3.py")
    replace_once(
        ret,
        '''physical = load(
    "return_ssi_physical_repair",
    Path(__file__).with_name("repair_return_ssi_units.py"),
)
''',
        '''physical = load(
    "return_ssi_physical_repair",
    Path(__file__).with_name("repair_return_ssi_units.py"),
)
buffer = load(
    "return_opa4196_physical_repair",
    Path(__file__).with_name("repair_ssi2164_buffer_opa4196_units.py"),
)
''',
    )
    replace_once(
        ret,
        '''    reviewed.main()
    physical.main()
    repair_output_directions(reviewed.base.SHEET_FILE, reviewed.base.HIER_OUTPUTS)
''',
        '''    reviewed.main()
    physical.main()
    buffer.repair_sheet06()
    repair_output_directions(reviewed.base.SHEET_FILE, reviewed.base.HIER_OUTPUTS)
''',
    )


def patch_validator() -> None:
    replace_once(
        VALIDATOR_PATH,
        '''import json
import subprocess
from pathlib import Path
''',
        '''import json
import re
import subprocess
from pathlib import Path
''',
    )
    replace_once(
        VALIDATOR_PATH,
        '''def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()

def main() -> None:
''',
        '''def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def number_pattern(value: float) -> str:
    integer = int(value)
    if value == integer:
        return rf"{integer}(?:\\.0+)?"
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return re.escape(text)


def assert_label_at(text: str, name: str, x: float, y: float) -> None:
    pattern = (
        rf'\\(label "{re.escape(name)}"\\s+\\(at '
        rf'{number_pattern(x)} {number_pattern(y)} 0(?:\\.0+)?\\)'
    )
    count = len(re.findall(pattern, text, re.MULTILINE))
    assert count == 1, (name, x, y, count)


def main() -> None:
''',
    )
    replace_once(
        VALIDATOR_PATH,
        '''    assert sheet05.count('property "Reference" "U63"') == 3
    assert sheet06.count('property "Reference" "U63"') == 2
    assert sheet05.count('property "Footprint" ""') > 0
''',
        '''    assert sheet05.count('property "Reference" "U63"') == 3
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
''',
    )


def main() -> None:
    assert_sources()
    write_repair_tool()
    patch_wrappers()
    patch_validator()
    print("U63 physical-coordinate repair patch applied; regeneration and ERC required")


if __name__ == "__main__":
    main()
