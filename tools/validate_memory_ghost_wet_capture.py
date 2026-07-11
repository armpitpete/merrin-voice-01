#!/usr/bin/env python3
"""Validate native sheet-05 capture and integrated SSI2164 ownership.

This validator reads emitted KiCad S-expressions directly. KiCad 10 remains the
authoritative parser in the following ERC step. These checks enforce the bounded
symbol, physical-pin, shared-device, gain and hierarchy contracts first.
"""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET05 = ROOT / "05_MEMORY_GHOST_WET.kicad_sch"
SHEET06 = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def balanced_block(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise AssertionError(f"Unterminated S-expression at offset {start}")


def instance_blocks(text: str) -> list[str]:
    """Return native symbol-instance blocks, excluding embedded library symbols."""
    marker = "\n\t(symbol\n\t\t(lib_id "
    blocks: list[str] = []
    offset = 0
    while True:
        found = text.find(marker, offset)
        if found == -1:
            return blocks
        start = found + 2
        block = balanced_block(text, start)
        blocks.append(block)
        offset = start + len(block)


def required_field(block: str, pattern: str, description: str) -> str:
    match = re.search(pattern, block)
    if not match:
        raise AssertionError(f"Missing {description} in symbol instance")
    return match.group(1)


def optional_field(block: str, pattern: str) -> str | None:
    match = re.search(pattern, block)
    return match.group(1) if match else None


def instances(path: Path) -> list[dict[str, object]]:
    rows = []
    for block in instance_blocks(path.read_text(encoding="utf-8")):
        rows.append(
            {
                "lib_id": required_field(block, r'\(lib_id "([^"]+)"', "lib_id"),
                "reference": required_field(
                    block,
                    r'\(property "Reference" "([^"]+)"',
                    "reference",
                ),
                "unit": int(required_field(block, r'\(unit (\d+)\)', "unit")),
                "footprint": optional_field(
                    block,
                    r'\(property "Footprint" "([^"]*)"',
                ),
            }
        )
    return rows


def hierarchical_labels(text: str) -> dict[str, str]:
    rows = re.findall(
        r'\(hierarchical_label "([^"]+)"\s+\(shape ([^)]+)\)',
        text,
        re.MULTILINE,
    )
    labels = dict(rows)
    assert len(labels) == len(rows), f"Duplicate hierarchical labels: {rows}"
    return labels


def unit_text(rendered: str, unit: int) -> str:
    marker = f'(symbol "SSI2164S_MULTI_{unit}_1"'
    start = rendered.index(marker)
    later = [
        rendered.find(f'(symbol "SSI2164S_MULTI_{candidate}_1"', start + 1)
        for candidate in range(unit + 1, 6)
    ]
    ends = [index for index in later if index != -1]
    end = min(ends) if ends else len(rendered)
    return rendered[start:end]


def assert_unique_references(rows: list[dict[str, object]], multi_ref: str) -> None:
    counts = Counter(
        str(row["reference"])
        for row in rows
        if not str(row["reference"]).startswith("#")
    )
    duplicates = sorted(
        reference
        for reference, count in counts.items()
        if count > 1 and reference != multi_ref
    )
    assert not duplicates, f"Duplicate references: {duplicates}"


def main() -> None:
    assert (ROOT / "05_MEMORY_GHOST_WET_CAPTURED").exists()
    assert (ROOT / "06_RETURN_BREAK_LIMITER_CAPTURED").exists()
    assert SHEET05.exists() and SHEET06.exists() and LIBRARY.exists()

    wet = load_module("memory_ghost_wet_capture", "tools/capture_memory_ghost_wet_sheet.py")
    ret = load_module("return_break_limiter_capture", "tools/capture_return_break_limiter_sheet.py")

    wet_inputs = {
        "RAIL_P12",
        "RAIL_N12",
        "MEMORY_DAC",
        "GHOST_DAC",
        "VCA_MEMORY_CTRL",
        "VCA_GHOST_CTRL",
        "VCA_WET_CTRL",
    }
    assert set(wet.HIER_INPUTS) == wet_inputs
    assert wet.HIER_OUTPUTS == ("WET_MIX",)
    assert wet.ALLOWED_EXPORTS == frozenset({"WET_MIX"})
    assert wet.SSI_REFERENCE == "U60"
    assert math.isclose(wet.VCA_INPUT_KOHM, wet.VCA_IV_KOHM)
    assert math.isclose(wet.SUM_BRANCH_GAIN, 20.0 / 40.2, abs_tol=1e-12)
    assert 0.497 < wet.SUM_BRANCH_GAIN < 0.498
    assert 2 * wet.SUM_BRANCH_GAIN < 1.0

    expected_pins = {
        1: {"2": "IIN1", "3": "VC1", "4": "IOUT1"},
        2: {"7": "IIN2", "6": "VC2", "5": "IOUT2"},
        3: {"15": "IIN3", "14": "VC3", "13": "IOUT3"},
        4: {"10": "IIN4", "11": "VC4", "12": "IOUT4"},
        5: {"1": "MODE", "8": "GND", "9": "V-", "16": "V+"},
    }
    rendered = ret.render_ssi2164_multi_symbol()
    for unit, pins in expected_pins.items():
        body = unit_text(rendered, unit)
        for number, name in pins.items():
            assert f'(name "{name}"' in body, (unit, name)
            assert f'(number "{number}"' in body, (unit, number)

    rows05 = instances(SHEET05)
    rows06 = instances(SHEET06)
    ssi05 = [row for row in rows05 if str(row["lib_id"]).endswith("SSI2164S_MULTI")]
    ssi06 = [row for row in rows06 if str(row["lib_id"]).endswith("SSI2164S_MULTI")]
    assert sorted(int(row["unit"]) for row in ssi05) == [1, 2, 4]
    assert sorted(int(row["unit"]) for row in ssi06) == [3, 5]

    all_ssi: list[tuple[str, dict[str, object]]] = []
    for path in sorted(ROOT.glob("[0-9][0-9]_*.kicad_sch")):
        for row in instances(path):
            if str(row["lib_id"]).endswith("SSI2164S_MULTI"):
                all_ssi.append((path.name, row))
    assert len(all_ssi) == 5, all_ssi
    assert {str(row["reference"]) for _path, row in all_ssi} == {"U60"}
    assert sorted(int(row["unit"]) for _path, row in all_ssi) == [1, 2, 3, 4, 5]
    for path_name, row in all_ssi:
        assert row["footprint"] == "", (path_name, row["unit"], row["footprint"])

    assert_unique_references(rows05, "U60")
    assert_unique_references(rows06, "U60")

    text05 = SHEET05.read_text(encoding="utf-8")
    text06 = SHEET06.read_text(encoding="utf-8")
    assert hierarchical_labels(text05) == {
        **{name: "input" for name in wet_inputs},
        "WET_MIX": "output",
    }
    assert hierarchical_labels(text06) == {
        **{name: "input" for name in ret.HIER_INPUTS},
        **{name: "output" for name in ret.HIER_OUTPUTS},
    }

    for token in (
        "SSI2164 — MEMORY CH1",
        "SSI2164 — GHOST CH2",
        "SSI2164 — WET MASTER CH4",
        "40.2k 1% Memory sum",
        "40.2k 1% Ghost sum",
        "20k 1% half-sum feedback",
        "47R output isolate",
        "Only WET_MIX crosses",
        "no second SSI2164 is created",
    ):
        assert token in text05, token
    assert "visible staged reservations for sheet 05" not in text06
    assert "same physical SSI2164" not in text06
    assert "pins 10 IIN3" not in text06

    print("Memory/Ghost/wet hierarchy and output-direction contract: PASS")
    print("SSI2164 symbol and physical-pin contract: PASS")
    print("SSI2164 five-unit shared ownership and unique-device contract: PASS")
    print("Memory/Ghost half-sum and WET_MIX export contract: PASS")


if __name__ == "__main__":
    main()
