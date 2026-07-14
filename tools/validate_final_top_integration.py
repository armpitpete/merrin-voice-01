#!/usr/bin/env python3
"""Validate the final 00_TOP parent/child and interface integration contract."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
MANIFEST = ROOT / "hierarchy-manifest.json"
TOP = ROOT / "MerrinGriefSynthMemoryCoreA.kicad_sch"
MARKER = ROOT / "00_TOP_FINAL_REVIEW_COMPLETE"

CAPTURE_MARKERS = tuple(f"{code:02d}_{name}_CAPTURED" for code, name in ())
EXPECTED_MARKERS = (
    "01_POWER_PROTECTION_CAPTURED",
    "02_MCU_CLOCK_DEBUG_CAPTURED",
    "03_CODEC_CONVERSION_CAPTURED",
    "04_INPUT_PRESSURE_ABSENCE_CAPTURED",
    "05_MEMORY_GHOST_WET_CAPTURED",
    "06_RETURN_BREAK_LIMITER_CAPTURED",
    "07_OUTPUT_MUTE_PROTECTION_CAPTURED",
    "08_CONTROLS_STATE_CAPTURED",
    "09_TEST_SERVICE_CAPTURED",
)

RESTRICTED_OUTPUTS = {
    "04": {"DIRECT_PRESENT", "SHAPED_PRESENT", "ADC_ANALOG_IN"},
    "05": {"WET_MIX"},
    "06": {"RETURN_LIMITED", "RETURN_FEED", "ABSENCE_INFLUENCE"},
    "07": set(),
    "09": set(),
}

TEMPORARY_TOKENS = (
    "SHEET_INTERFACE_NOT_FITTED",
    "Temporary hierarchy/ERC harness",
    "INTERFACE CAPTURE ONLY",
    "visible staged reservations",
)


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


def top_sheet_blocks(text: str) -> list[str]:
    marker = "\n\t(sheet\n"
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


def required(block: str, pattern: str, description: str) -> str:
    match = re.search(pattern, block)
    if not match:
        raise AssertionError(f"Missing {description}")
    return match.group(1)


def main() -> None:
    for marker in EXPECTED_MARKERS:
        assert (ROOT / marker).exists(), marker
    assert MARKER.exists()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["project"] == "MerrinGriefSynthMemoryCoreA"
    assert manifest["stage"] == "component-capture-complete"
    assert manifest["temporary_interface_harnesses"] is False
    assert manifest["component_sheets_captured"] is True
    assert manifest["top_schematic"] == TOP.name
    assert len(manifest["sheets"]) == 9

    top_text = TOP.read_text(encoding="utf-8")
    blocks = top_sheet_blocks(top_text)
    assert len(blocks) == 9, len(blocks)

    top_by_file: dict[str, tuple[str, list[tuple[str, str]]]] = {}
    for block in blocks:
        filename = required(
            block, r'\(property "Sheetfile" "([^"]+)"', "sheet filename"
        )
        name = required(block, r'\(property "Sheetname" "([^"]+)"', "sheet name")
        pins = re.findall(r'\(pin "([^"]+)" ([a-z_]+)', block)
        assert filename not in top_by_file, filename
        top_by_file[filename] = (name, pins)

    net_ends: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    expected_files = set()
    for sheet in manifest["sheets"]:
        filename = sheet["filename"]
        expected_files.add(filename)
        expected_pins = [
            (pin["name"], pin["direction"])
            for pin in sheet["pins"]
        ]
        assert filename in top_by_file, filename
        top_name, top_pins = top_by_file[filename]
        assert top_name == f"{sheet['code']} {sheet['title']}", top_name
        assert top_pins == expected_pins, (sheet["code"], top_pins, expected_pins)

        child_text = (ROOT / filename).read_text(encoding="utf-8")
        child_labels = re.findall(
            r'\(hierarchical_label "([^"]+)"\s+\(shape ([^)]+)\)',
            child_text,
            re.MULTILINE,
        )
        assert len(child_labels) == len(expected_pins) == len(dict(child_labels)), (
            sheet["code"], child_labels, expected_pins
        )
        assert dict(child_labels) == dict(expected_pins), (
            sheet["code"], child_labels, expected_pins
        )

        for name, direction in expected_pins:
            net_ends[name].append((sheet["code"], direction))

    assert set(top_by_file) == expected_files
    assert {path.name for path in ROOT.glob("[0-9][0-9]_*.kicad_sch")} == expected_files

    for name, ends in net_ends.items():
        providers = [end for end in ends if end[1] in {"output", "bidirectional"}]
        consumers = [end for end in ends if end[1] in {"input", "bidirectional"}]
        assert providers, (name, ends)
        assert consumers, (name, ends)

    for code, expected in RESTRICTED_OUTPUTS.items():
        sheet = next(item for item in manifest["sheets"] if item["code"] == code)
        actual = {
            pin["name"]
            for pin in sheet["pins"]
            if pin["direction"] == "output"
        }
        assert actual == expected, (code, actual, expected)

    assert manifest["return_sheet_allowed_outputs"] == [
        "ABSENCE_INFLUENCE",
        "RETURN_FEED",
        "RETURN_LIMITED",
    ]

    for path in [TOP, *sorted(ROOT.glob("[0-9][0-9]_*.kicad_sch"))]:
        text = path.read_text(encoding="utf-8")
        for token in TEMPORARY_TOKENS:
            assert token not in text, (path.name, token)
        assert not re.search(
            r'\(property "Reference" "J90[1-9]"', text
        ), (path.name, "former harness reference")

    assert 'V5.2 integrated schematic review' in top_text
    assert (
        'All nine component sheets captured. Final integrated interface and ERC review.'
        in top_text
    )
    assert 'Detailed circuits replace temporary harnesses sheet by sheet.' not in top_text

    assert (ROOT / "05_MEMORY_GHOST_WET_VALIDATION.md").exists()
    assert (ROOT / "07_OUTPUT_MUTE_PROTECTION_VALIDATION.md").exists()
    assert (ROOT / "09_TEST_SERVICE_VALIDATION.md").exists()

    print("Final parent-sheet / child-label interface reconciliation: PASS")
    print(f"Provider/consumer coverage for {len(net_ends)} hierarchy nets: PASS")
    print("Restricted sheet-output boundaries and Return exports: PASS")
    print("Temporary interface harness and former J901-J909 references removed: PASS")
    print("Top-sheet and manifest authority advanced to component-capture-complete: PASS")


if __name__ == "__main__":
    main()
