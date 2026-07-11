#!/usr/bin/env python3
"""Validate sheet 07 and the shared U32 OPA1679 integration contract."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET03 = ROOT / "03_CODEC_CONVERSION.kicad_sch"
SHEET07 = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MANIFEST = ROOT / "hierarchy-manifest.json"


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
                    block, r'\(property "Reference" "([^"]+)"', "reference"
                ),
                "value": required_field(
                    block, r'\(property "Value" "([^"]*)"', "value"
                ),
                "unit": int(required_field(block, r'\(unit (\d+)\)', "unit")),
                "footprint": optional_field(
                    block, r'\(property "Footprint" "([^"]*)"'
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


def library_symbol_block(text: str, name: str) -> str:
    marker = f'\t(symbol "{name}"'
    start = text.index(marker)
    return balanced_block(text, start + 1)


def unit_text(rendered: str, symbol_name: str, unit: int, max_unit: int) -> str:
    marker = f'(symbol "{symbol_name}_{unit}_1"'
    start = rendered.index(marker)
    later = [
        rendered.find(f'(symbol "{symbol_name}_{candidate}_1"', start + 1)
        for candidate in range(unit + 1, max_unit + 1)
    ]
    ends = [index for index in later if index != -1]
    return rendered[start : min(ends) if ends else len(rendered)]


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
    for required in (
        ROOT / "03_CODEC_CONVERSION_CAPTURED",
        ROOT / "07_OUTPUT_MUTE_PROTECTION_CAPTURED",
        SHEET03,
        SHEET07,
        LIBRARY,
        MANIFEST,
    ):
        assert required.exists(), required

    output = load_module(
        "output_mute_protection_capture",
        "tools/capture_output_mute_protection_sheet.py",
    )
    codec = load_module(
        "codec_conversion_capture",
        "tools/capture_codec_conversion_sheet.py",
    )
    support = load_module("opa1679_multi_support", "tools/opa1679_multi_support.py")

    expected_inputs = {
        "RAIL_P12",
        "RAIL_N12",
        "DIRECT_PRESENT",
        "WET_MIX",
        "HARDWARE_FAULT_N",
    }
    assert set(output.HIER_INPUTS) == expected_inputs
    assert output.HIER_OUTPUTS == ()
    assert output.ALLOWED_EXPORTS == frozenset()

    assert math.isclose(output.SUM_BRANCH_GAIN, 20.0 / 40.2, abs_tol=1e-12)
    assert 0.497 < output.SUM_BRANCH_GAIN < 0.498
    assert output.MAX_CALCULATED_MIX_VPP < 6.0
    assert output.MAX_CALCULATED_MIX_VPP < 10.0
    assert output.MUTE_GATE_STEADY_V < -10.0
    assert 80.0 < output.MUTE_RELEASE_TAU_MS < 100.0
    assert output.OPTO_LED_CURRENT_MA > 1.9
    assert output.CALCULATED_FAULT_CLAMP_MS < 20.0

    expected_opa_pins = {
        1: {"3": "IN_A+", "2": "IN_A-", "1": "OUT_A"},
        2: {"5": "IN_B+", "6": "IN_B-", "7": "OUT_B"},
        3: {"10": "IN_C+", "9": "IN_C-", "8": "OUT_C"},
        4: {"12": "IN_D+", "13": "IN_D-", "14": "OUT_D"},
        5: {"11": "V-", "4": "V+"},
    }
    rendered = support.render_symbol()
    for unit, pins in expected_opa_pins.items():
        body = unit_text(rendered, support.SYMBOL_NAME, unit, 5)
        for number, name in pins.items():
            assert f'(name "{name}"' in body, (unit, name)
            assert f'(number "{number}"' in body, (unit, number)

    rows03 = instances(SHEET03)
    rows07 = instances(SHEET07)
    shared03 = [
        row for row in rows03 if str(row["lib_id"]).endswith(support.SYMBOL_NAME)
    ]
    shared07 = [
        row for row in rows07 if str(row["lib_id"]).endswith(support.SYMBOL_NAME)
    ]
    assert sorted(int(row["unit"]) for row in shared03) == [1, 5], shared03
    assert sorted(int(row["unit"]) for row in shared07) == [2, 3, 4], shared07

    all_shared: list[tuple[str, dict[str, object]]] = []
    all_opamps: list[tuple[str, dict[str, object]]] = []
    for path in sorted(ROOT.glob("[0-9][0-9]_*.kicad_sch")):
        for row in instances(path):
            lib_id = str(row["lib_id"])
            if lib_id.endswith(support.SYMBOL_NAME):
                all_shared.append((path.name, row))
            if lib_id.endswith("OPA1679_PW_APPLICATION") or lib_id.endswith(
                support.SYMBOL_NAME
            ):
                all_opamps.append((path.name, row))

    assert len(all_shared) == 5, all_shared
    assert {str(row["reference"]) for _path, row in all_shared} == {"U32"}
    assert {str(row["value"]) for _path, row in all_shared} == {"OPA1679"}
    assert sorted(int(row["unit"]) for _path, row in all_shared) == [1, 2, 3, 4, 5]
    for path_name, row in all_shared:
        assert row["footprint"] == "", (path_name, row)

    expected_physical_packages = {"U31", "U32", "U40", "U41", "U50", "U61", "U62"}
    opamp_refs = {str(row["reference"]) for _path, row in all_opamps}
    assert opamp_refs == expected_physical_packages, opamp_refs
    assert len(opamp_refs) == 7
    assert not any(
        str(row["reference"]) == "U32"
        and str(row["lib_id"]).endswith("OPA1679_PW_APPLICATION")
        for row in rows03
    )

    assert_unique_references(rows03, "U32")
    assert_unique_references(rows07, "U32")

    text03 = SHEET03.read_text(encoding="utf-8")
    text07 = SHEET07.read_text(encoding="utf-8")
    expected_codec_labels = {
        **{name: "input" for name in codec.HIER_INPUTS},
        "CTRL_I2C_SDA": "bidirectional",
        **{name: "output" for name in codec.HIER_OUTPUTS},
    }
    assert hierarchical_labels(text03) == expected_codec_labels
    assert hierarchical_labels(text07) == {
        name: "input" for name in expected_inputs
    }

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sheet07 = next(item for item in manifest["sheets"] if item["code"] == "07")
    assert {pin["name"] for pin in sheet07["pins"]} == expected_inputs
    assert all(pin["direction"] == "input" for pin in sheet07["pins"])

    library = LIBRARY.read_text(encoding="utf-8")
    assert f'(symbol "{support.SYMBOL_NAME}"' in library
    opto_block = library_symbol_block(library, "LTV817S_MUTE_APPLICATION")
    for number, name in {"1": "LED_A", "2": "LED_K", "3": "EMITTER", "4": "COLLECTOR"}.items():
        assert f'(name "{name}"' in opto_block
        assert f'(number "{number}"' in opto_block
    jack_block = library_symbol_block(library, "WQP518MA_APPLICATION")
    for number, name in {"1": "TIP", "2": "TIP_NORMAL", "3": "SLEEVE"}.items():
        assert f'(name "{name}"' in jack_block
        assert f'(number "{number}"' in jack_block

    for token in (
        "40.2k 1% Direct sum",
        "40.2k 1% Wet sum",
        "20k 1% half-sum feedback",
        "10k A OUTPUT LEVEL",
        "10k mute isolation",
        "J113 OUTPUT MUTE SHUNT",
        "10k fault inverter base",
        "2.2k +12V fault pull-up",
        "3.3k optocoupler LED",
        "100k controlled release",
        "1uF mute ramp",
        "1k output protection",
        "WQP518MA / THONKICONN OUTPUT",
        "Exactly seven physical OPA1679 packages remain",
        "No audio or control net is exported from this sheet",
    ):
        assert token in text07, token
    for forbidden in (
        "SHEET_INTERFACE_NOT_FITTED",
        "Temporary hierarchy/ERC harness",
        'Reference" "J907',
        "U32B_SPARE",
        "U32C_SPARE",
        "U32D_SPARE",
    ):
        assert forbidden not in text07
        if forbidden.startswith("U32"):
            assert forbidden not in text03

    active_refs = {"U32", "U70", "Q70", "Q71", "J70"}
    for row in rows07:
        if str(row["reference"]) in active_refs:
            assert row["footprint"] in (None, ""), row

    print("Output hierarchy and no-export boundary contract: PASS")
    print("Shared U32 OPA1679 official-pin and seven-package allocation contract: PASS")
    print("Direct/wet half-sum, output-level and <=10 Vpp calculated contract: PASS")
    print("Fail-muted hardware control and provisional <20 ms clamp calculation: PASS")
    print("Protected WQP518MA logical output-jack and blank-footprint contract: PASS")


if __name__ == "__main__":
    main()
