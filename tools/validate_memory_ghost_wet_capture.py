#!/usr/bin/env python3
"""Validate the sheet-05 capture and integrated SSI2164 ownership contract."""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from collections import Counter
from pathlib import Path

import kicad_sch_api as ksa

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


def hierarchical_labels(text: str) -> dict[str, str]:
    rows = re.findall(
        r'\(hierarchical_label "([^"]+)"\s+\(shape ([^)]+)\)',
        text,
        re.MULTILINE,
    )
    labels = dict(rows)
    if len(labels) != len(rows):
        raise AssertionError(f"Duplicate hierarchical label names: {rows}")
    return labels


def check_unique_references(schematic, expected_multi_ref: str | None = None) -> None:
    refs = [
        component.reference
        for component in schematic.components
        if not component.reference.startswith("#")
    ]
    duplicates = sorted(
        reference
        for reference, count in Counter(refs).items()
        if count > 1 and reference != expected_multi_ref
    )
    assert not duplicates, duplicates


def unit_text(rendered: str, unit: int) -> str:
    marker = f'(symbol "SSI2164S_MULTI_{unit}_1"'
    start = rendered.index(marker)
    next_markers = [
        rendered.find(f'(symbol "SSI2164S_MULTI_{later}_1"', start + 1)
        for later in range(unit + 1, 6)
    ]
    ends = [index for index in next_markers if index != -1]
    end = min(ends) if ends else len(rendered)
    return rendered[start:end]


def main() -> None:
    assert (ROOT / "05_MEMORY_GHOST_WET_CAPTURED").exists()
    assert (ROOT / "06_RETURN_BREAK_LIMITER_CAPTURED").exists()
    assert SHEET05.exists() and SHEET06.exists() and LIBRARY.exists()

    wet = load_module("memory_ghost_wet_capture", "tools/capture_memory_ghost_wet_sheet.py")
    ret = load_module("return_break_limiter_capture", "tools/capture_return_break_limiter_sheet.py")

    expected_wet_inputs = {
        "RAIL_P12",
        "RAIL_N12",
        "MEMORY_DAC",
        "GHOST_DAC",
        "VCA_MEMORY_CTRL",
        "VCA_GHOST_CTRL",
        "VCA_WET_CTRL",
    }
    assert set(wet.HIER_INPUTS) == expected_wet_inputs
    assert wet.HIER_OUTPUTS == ("WET_MIX",)
    assert wet.ALLOWED_EXPORTS == frozenset({"WET_MIX"})
    assert wet.SSI_REFERENCE == "U60"
    assert wet.SSI_CHANNEL_PINS == {
        1: {"iin": "2", "vc": "3", "iout": "4", "role": "MEMORY"},
        2: {"iin": "7", "vc": "6", "iout": "5", "role": "GHOST"},
        4: {"iin": "10", "vc": "11", "iout": "12", "role": "WET MASTER"},
    }
    assert math.isclose(wet.VCA_INPUT_KOHM, wet.VCA_IV_KOHM)
    assert math.isclose(wet.SUM_BRANCH_GAIN, 20.0 / 40.2, abs_tol=1e-12)
    assert 0.497 < wet.SUM_BRANCH_GAIN < 0.498
    assert 2 * wet.SUM_BRANCH_GAIN < 1.0

    rendered = ret.render_ssi2164_multi_symbol()
    expected_units = {
        1: (("2", "IIN1"), ("3", "VC1"), ("4", "IOUT1")),
        2: (("7", "IIN2"), ("6", "VC2"), ("5", "IOUT2")),
        3: (("15", "IIN3"), ("14", "VC3"), ("13", "IOUT3")),
        4: (("10", "IIN4"), ("11", "VC4"), ("12", "IOUT4")),
        5: (("1", "MODE"), ("8", "GND"), ("9", "V-"), ("16", "V+")),
    }
    for unit, pins in expected_units.items():
        body = unit_text(rendered, unit)
        for number, name in pins:
            assert f'(name "{name}"' in body, (unit, name)
            assert f'(number "{number}"' in body, (unit, number)

    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(LIBRARY.resolve()))
    sheet05 = ksa.load_schematic(str(SHEET05))
    sheet06 = ksa.load_schematic(str(SHEET06))

    units05 = sorted(
        component._data.unit
        for component in sheet05.components
        if component.reference == "U60" and component.lib_id.endswith("SSI2164S_MULTI")
    )
    units06 = sorted(
        component._data.unit
        for component in sheet06.components
        if component.reference == "U60" and component.lib_id.endswith("SSI2164S_MULTI")
    )
    assert units05 == [1, 2, 4], units05
    assert units06 == [3, 5], units06
    assert sorted(units05 + units06) == [1, 2, 3, 4, 5]

    all_ssi = []
    for path in sorted(ROOT.glob("[0-9][0-9]_*.kicad_sch")):
        schematic = ksa.load_schematic(str(path))
        for component in schematic.components:
            if component.lib_id.endswith("SSI2164S_MULTI"):
                all_ssi.append((path.name, component.reference, component._data.unit))
    assert len(all_ssi) == 5, all_ssi
    assert {reference for _path, reference, _unit in all_ssi} == {"U60"}
    assert sorted(unit for _path, _reference, unit in all_ssi) == [1, 2, 3, 4, 5]

    for component in sheet05.components:
        if component.reference == "U60":
            pins = wet.SSI_CHANNEL_PINS[component._data.unit]
            for pin in (pins["iin"], pins["vc"], pins["iout"]):
                assert component.get_pin_position(pin) is not None, (
                    component._data.unit,
                    pin,
                )

    check_unique_references(sheet05, "U60")
    check_unique_references(sheet06, "U60")

    text05 = SHEET05.read_text(encoding="utf-8")
    text06 = SHEET06.read_text(encoding="utf-8")
    labels05 = hierarchical_labels(text05)
    labels06 = hierarchical_labels(text06)
    assert labels05 == {
        **{name: "input" for name in expected_wet_inputs},
        "WET_MIX": "output",
    }, labels05
    assert labels06 == {
        **{name: "input" for name in ret.HIER_INPUTS},
        **{name: "output" for name in ret.HIER_OUTPUTS},
    }, labels06

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

    print("Memory/Ghost/wet hierarchy direction contract: PASS")
    print("SSI2164 physical-pin and five-unit ownership contract: PASS")
    print("No duplicate SSI2164 physical device: PASS")
    print("Memory/Ghost half-sum and WET_MIX export contract: PASS")


if __name__ == "__main__":
    main()
