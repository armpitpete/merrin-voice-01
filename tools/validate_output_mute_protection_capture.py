#!/usr/bin/env python3
"""Validate sheet 07 after the exact output-mute and fault-path amendment."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET03 = ROOT / "03_CODEC_CONVERSION.kicad_sch"
SHEET07 = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MANIFEST = ROOT / "hierarchy-manifest.json"
MARKER = ROOT / "07_OUTPUT_MUTE_EXACT_PARTS_AMENDED"
SOT23 = "Package_TO_SOT_SMD:SOT-23"
SMDIP4 = "Package_DIP:SMDIP-4_W7.62mm"


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
    assert match, f"Missing {description}"
    return match.group(1)


def instances(path: Path) -> list[dict[str, object]]:
    rows = []
    for block in instance_blocks(path.read_text(encoding="utf-8")):
        rows.append({
            "block": block,
            "lib_id": field(block, r'\(lib_id "([^"]+)"', "lib_id"),
            "reference": field(block, r'\(property "Reference" "([^"]+)"', "reference"),
            "value": field(block, r'\(property "Value" "([^"]*)"', "value"),
            "footprint": field(block, r'\(property "Footprint" "([^"]*)"', "footprint"),
            "unit": int(field(block, r'\(unit (\d+)\)', "unit")),
        })
    return rows


def one(rows: list[dict[str, object]], reference: str) -> dict[str, object]:
    matches = [row for row in rows if row["reference"] == reference]
    assert len(matches) == 1, (reference, len(matches))
    return matches[0]


def symbol_definition(text: str, name: str) -> str:
    marker = f'\t(symbol "{name}"'
    start = text.index(marker) + 1
    return balanced_block(text, start)


def assert_pin_contract(block: str, pins: dict[str, str]) -> None:
    for number, name in pins.items():
        assert f'(name "{name}"' in block, (number, name)
        assert f'(number "{number}"' in block, (number, name)


def assert_label(text: str, name: str, x: str, y: str) -> None:
    token = f'(label "{name}"\n\t\t(at {x} {y} 0)'
    assert text.count(token) == 1, (name, x, y, text.count(token))


def hierarchical_labels(text: str) -> dict[str, str]:
    rows = re.findall(r'\(hierarchical_label "([^"]+)"\s+\(shape ([^)]+)\)', text)
    labels = dict(rows)
    assert len(labels) == len(rows), rows
    return labels


def main() -> None:
    for required in (SHEET03, SHEET07, LIBRARY, MANIFEST, MARKER):
        assert required.exists(), required

    text07 = SHEET07.read_text(encoding="utf-8")
    library = LIBRARY.read_text(encoding="utf-8")
    rows03 = instances(SHEET03)
    rows07 = instances(SHEET07)

    expected_inputs = {"RAIL_P12", "RAIL_N12", "DIRECT_PRESENT", "WET_MIX", "HARDWARE_FAULT_N"}
    assert hierarchical_labels(text07) == {name: "input" for name in expected_inputs}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sheet07 = next(item for item in manifest["sheets"] if item["code"] == "07")
    assert {pin["name"] for pin in sheet07["pins"]} == expected_inputs
    assert all(pin["direction"] == "input" for pin in sheet07["pins"])

    exact_symbols = {
        "MMBFJ113_APPLICATION": ({"1": "DRAIN", "2": "SOURCE", "3": "GATE"}, SOT23,
                                  "https://www.onsemi.com/pdf/datasheet/mmbfj113-d.pdf"),
        "PMV20XNE_APPLICATION": ({"1": "GATE", "2": "SOURCE", "3": "DRAIN"}, SOT23,
                                 "https://assets.nexperia.com/documents/data-sheet/PMV20XNE.pdf"),
        "VO617A_3X007T_APPLICATION": ({"1": "LED_A", "2": "LED_K", "3": "EMITTER", "4": "COLLECTOR"}, SMDIP4,
                                      "https://www.vishay.com/docs/83430/vo617a.pdf"),
    }
    for name, (pins, footprint, datasheet) in exact_symbols.items():
        block = symbol_definition(library, name)
        assert_pin_contract(block, pins)
        assert f'(property "Footprint" "{footprint}"' in block
        assert f'(property "Datasheet" "{datasheet}"' in block
        embedded = symbol_definition(text07, f"MerrinLab_PrototypeA:{name}")
        assert_pin_contract(embedded, pins)
        assert f'(property "Footprint" "{footprint}"' in embedded

    exact_instances = {
        "Q70": ("MMBFJ113_APPLICATION", "MMBFJ113 OUTPUT MUTE SHUNT", SOT23),
        "Q71": ("PMV20XNE_APPLICATION", "PMV20XNE HEALTHY-RELEASE DRIVER", SOT23),
        "U70": ("VO617A_3X007T_APPLICATION", "VO617A-3X007T HEALTHY RELEASE", SMDIP4),
    }
    for reference, (name, value, footprint) in exact_instances.items():
        row = one(rows07, reference)
        assert row["lib_id"] == f"MerrinLab_PrototypeA:{name}", row
        assert row["value"] == value, row
        assert row["footprint"] == footprint, row

    expected_values = {
        "R703": "120k 1% mute isolation",
        "R711": "10k fault gate series",
        "R712": "100k fault gate pull-down",
        "R713": "820R 1% optocoupler LED series A",
        "R714": "1k 1% optocoupler LED series B",
        "R715": "10k 1% negative release",
        "R716": "100k 1% fail-mute pull",
        "C710": "100nF C0G 50V mute timing",
    }
    for reference, value in expected_values.items():
        assert one(rows07, reference)["value"] == value

    for name, x, y in (
        ("MUTE_NODE", "254", "142.24"),
        ("MUTE_GATE", "254", "144.78"),
        ("GND", "274.32", "142.24"),
        ("FAULT_GATE", "121.92", "195.58"),
        ("MUTE_LED_K", "142.24", "193.04"),
        ("GND", "142.24", "198.12"),
        ("MUTE_LED_A", "193.04", "193.04"),
        ("MUTE_LED_K", "193.04", "198.12"),
        ("RELEASE_SINK", "213.36", "198.12"),
        ("MUTE_GATE", "213.36", "193.04"),
        ("RELEASE_SINK", "238.76", "186.69"),
    ):
        assert_label(text07, name, x, y)

    for token in (
        "J113_SHUNT_APPLICATION", "NPN_FAULT_INVERTER_APPLICATION",
        "LTV817S_MUTE_APPLICATION", "FAULT_INV_BASE", "MUTE_FAULT_HIGH",
        "MMBT3904 fault inverter provisional", "LTV-817S-CLASS FAIL-MUTE",
    ):
        assert token not in text07, token

    all_u32 = [row for row in rows03 + rows07 if row["reference"] == "U32"]
    assert len(all_u32) == 5, all_u32
    assert sorted(int(row["unit"]) for row in all_u32) == [1, 2, 3, 4, 5]
    assert {row["value"] for row in all_u32} == {"OPA1679"}
    assert {row["footprint"] for row in all_u32} == {""}

    counts = Counter(row["reference"] for row in rows07 if not str(row["reference"]).startswith("#"))
    assert all(count == 1 or reference == "U32" for reference, count in counts.items())

    isolation_min = 120_000 * 0.99
    attenuation_db = -20 * math.log10(100.0 / (isolation_min + 100.0))
    assert attenuation_db > 60.0
    healthy_gate = (-12.0 + 0.4) * 100_000 / 110_000
    fault_crossing_ms = 100_000 * 100e-9 * 1000 * math.log(abs(healthy_gate) / 3.0)
    assert healthy_gate < -10.0 and fault_crossing_ms < 20.0
    gate_low = 3.3 * 0.95 * (100_000 * 0.99) / (
        10_000 * 1.01 + 10_000 * 1.01 + 100_000 * 0.99)
    assert gate_low > 2.5
    led_current_low_ma = (12.0 * 0.95 - 1.65) / ((820 + 1000) * 1.01) * 1000
    release_current_ma = abs(healthy_gate) / 10_000 * 1000
    assert led_current_low_ma >= 5.0 and led_current_low_ma > 4 * release_current_ma

    for token in (
        "120k isolation with 100 ohm worst JFET on-resistance calculates better than 60 dB",
        "Fault or +12 V loss removes release drive", "bench proof remains Gate C",
        "No audio or control net is exported",
    ):
        assert token in text07, token

    print("Output hierarchy and no-export boundary contract: PASS")
    print("Q70 MMBFJ113, Q71 PMV20XNE and U70 VO617A-3X007T physical-pin contracts: PASS")
    print("SOT-23 / SOT-23 / option-7 SMD-4 footprint mappings: PASS")
    print(f"Worst-case calculated static mute attenuation: PASS — {attenuation_db:.2f} dB")
    print(f"Fault/+12-loss worst-cutoff crossing: PASS — {fault_crossing_ms:.2f} ms")
    print(f"Minimum healthy MOSFET gate estimate: PASS — {gate_low:.3f} V")
    print(f"Minimum optocoupler LED current estimate: PASS — {led_current_low_ma:.3f} mA")
    print("Shared U32 OPA1679 ownership remains unchanged and footprint-blocked: PASS")


if __name__ == "__main__":
    main()
