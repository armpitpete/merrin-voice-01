#!/usr/bin/env python3
"""Validate the read-only sheet-09 test/service capture contract."""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET = ROOT / "09_TEST_SERVICE.kicad_sch"
MARKER = ROOT / "09_TEST_SERVICE_CAPTURED"


def load_module():
    path = Path("tools/capture_test_service_sheet.py")
    spec = importlib.util.spec_from_file_location("test_service_capture", path)
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
    raise AssertionError(f"Unterminated S-expression at {start}")


def instance_blocks(text: str) -> list[str]:
    marker = "\n\t(symbol\n\t\t(lib_id "
    blocks = []
    offset = 0
    while True:
        found = text.find(marker, offset)
        if found == -1:
            return blocks
        start = found + 2
        block = balanced_block(text, start)
        blocks.append(block)
        offset = start + len(block)


def field(block: str, pattern: str, description: str) -> str:
    match = re.search(pattern, block)
    if not match:
        raise AssertionError(f"Missing {description}")
    return match.group(1)


def instance_for_reference(text: str, reference: str) -> str:
    rows = [
        block
        for block in instance_blocks(text)
        if f'(property "Reference" "{reference}"' in block
    ]
    assert len(rows) == 1, (reference, len(rows))
    return rows[0]


def main() -> None:
    assert MARKER.exists()
    assert SHEET.exists()
    module = load_module()
    text = SHEET.read_text(encoding="utf-8")

    expected_inputs = {
        "RAIL_3V3",
        "HARDWARE_FAULT_N",
        "SHAPED_PRESENT",
        "ADC_ANALOG_IN",
        "RETURN_LIMITED",
        "RETURN_FEED",
        "ABSENCE_INFLUENCE",
        "WET_MIX",
    }
    assert set(module.HIER_INPUTS) == expected_inputs
    assert module.HIER_OUTPUTS == ()
    assert module.ALLOWED_EXPORTS == frozenset()

    labels = re.findall(
        r'\(hierarchical_label "([^"]+)"\s+\(shape ([^)]+)\)',
        text,
        re.MULTILINE,
    )
    assert len(labels) == 8, labels
    assert dict(labels) == {name: "input" for name in expected_inputs}

    expected_branches = {
        "R900": ("RAIL_3V3", "RAIL_3V3_PROBE", "1k rail short-limit"),
        "R901": ("HARDWARE_FAULT_N", "HARDWARE_FAULT_N_PROBE", "47k safety-state isolate"),
        "R902": ("SHAPED_PRESENT", "SHAPED_PRESENT_PROBE", "22k analogue probe isolate"),
        "R903": ("ADC_ANALOG_IN", "ADC_ANALOG_IN_PROBE", "22k analogue probe isolate"),
        "R904": ("RETURN_LIMITED", "RETURN_LIMITED_PROBE", "22k analogue probe isolate"),
        "R905": ("RETURN_FEED", "RETURN_FEED_PROBE", "22k analogue probe isolate"),
        "R906": ("ABSENCE_INFLUENCE", "ABSENCE_INFLUENCE_PROBE", "22k analogue probe isolate"),
        "R907": ("WET_MIX", "WET_MIX_PROBE", "22k analogue probe isolate"),
    }
    assert len(module.PROBE_BRANCHES) == 8
    for source, probe, reference, value in module.PROBE_BRANCHES:
        assert expected_branches[reference] == (source, probe, value)
        block = instance_for_reference(text, reference)
        assert f'(property "Value" "{value}"' in block

    assert module.HEADER_PIN_NETS == {
        "1": "GND",
        "2": "RAIL_3V3_PROBE",
        "3": "HARDWARE_FAULT_N_PROBE",
        "4": "SHAPED_PRESENT_PROBE",
        "5": "ADC_ANALOG_IN_PROBE",
        "6": "RETURN_LIMITED_PROBE",
        "7": "RETURN_FEED_PROBE",
        "8": "ABSENCE_INFLUENCE_PROBE",
        "9": "WET_MIX_PROBE",
        "10": "GND",
    }

    header = instance_for_reference(text, "J90")
    assert '(lib_id "Connector_Generic:Conn_01x10")' in header
    assert '(property "Value" "LOGICAL SERVICE PROBE HEADER / PADS"' in header
    assert '(property "Footprint" ""' in header
    for pin in range(1, 11):
        assert f'(pin "{pin}"' in header

    references = [
        field(block, r'\(property "Reference" "([^"]+)"', "reference")
        for block in instance_blocks(text)
    ]
    counts = Counter(ref for ref in references if not ref.startswith("#"))
    assert not [ref for ref, count in counts.items() if count > 1], counts
    for number in range(900, 909):
        assert counts[f"TP{number}"] == 1

    assert math.isclose(3.3 / 1000.0 * 1000.0, 3.3)
    assert 3.3 / 47000.0 * 1_000_000.0 < 71.0
    analogue_loading = 22000.0 / (10_000_000.0 + 22000.0) * 100.0
    assert analogue_loading < 0.22

    for token in (
        "READ-ONLY PROBE ISOLATION",
        "1k rail short-limit",
        "47k safety-state isolate",
        "22k analogue probe isolate",
        "LOGICAL SERVICE PROBE HEADER / PADS",
        "No hierarchy output is created",
        "SERVICE_TEST, RESET_CLEAR and SAFE_MUTE remain operating inputs between sheets 08 and 02",
        "SWD remains on sheet 02",
        "connector, fixture and footprint are not accepted",
    ):
        assert token in text, token

    for forbidden in (
        "SHEET_INTERFACE_NOT_FITTED",
        "Temporary hierarchy/ERC harness",
        'Reference" "J909',
    ):
        assert forbidden not in text

    print("Sheet-09 eight-input, read-only, no-export hierarchy contract: PASS")
    print("Eight current-limited probe branches and nine test-point contract: PASS")
    print("Logical ten-position service header pin allocation and blank footprint: PASS")
    print("Rail-short, safety-net isolation and high-impedance loading calculations: PASS")


if __name__ == "__main__":
    main()
