#!/usr/bin/env python3
"""Validate the fail-closed Gate-B input/output jack exact-part lane."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET04 = ROOT / "04_INPUT_PRESSURE_ABSENCE.kicad_sch"
SHEET07 = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
INPUT_GENERATOR = Path("tools/capture_input_pressure_absence_sheet.py")
OUTPUT_GENERATOR = Path("tools/capture_output_mute_protection_sheet.py")
AUDIT = ROOT / "INPUT_OUTPUT_JACK_AUDIT.json"
REVIEW = ROOT / "INPUT_OUTPUT_JACK_EXACT_PART_REVIEW.md"
CONTRACT = ROOT / "JACK_EXACT_PART_EDIT_CONTRACT.md"
FOOTPRINT = (
    ROOT
    / "jack-footprint-audits"
    / "Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical.kicad_mod"
)

EXPECTED_SOURCE_COMMIT = "14a88866e93b8ce4a31ad376b0c6eb85cd4d2cf3"
EXPECTED_SOURCE_BLOB = "1ebfa641294a0fd38f9c0e2c5c8b85dbc71ccaf6"
EXPECTED_SHA256 = "9f54f81d8f0152e77082746b47158c297c84154dd6fbe0b459ef147a86b10678"


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
    result: list[str] = []
    offset = 0
    while True:
        found = text.find(marker, offset)
        if found == -1:
            return result
        start = found + 2
        block = balanced_block(text, start)
        result.append(block)
        offset = start + len(block)


def field(block: str, pattern: str, description: str) -> str:
    match = re.search(pattern, block)
    assert match, f"Missing {description}"
    return match.group(1)


def instances(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for block in instance_blocks(path.read_text(encoding="utf-8")):
        rows.append(
            {
                "block": block,
                "lib_id": field(block, r'\(lib_id "([^"]+)"', "lib_id"),
                "reference": field(
                    block, r'\(property "Reference" "([^"]+)"', "reference"
                ),
                "value": field(block, r'\(property "Value" "([^"]*)"', "value"),
                "footprint": field(
                    block, r'\(property "Footprint" "([^"]*)"', "footprint"
                ),
            }
        )
    return rows


def one(rows: list[dict[str, str]], reference: str) -> dict[str, str]:
    matches = [row for row in rows if row["reference"] == reference]
    assert len(matches) == 1, (reference, len(matches))
    return matches[0]


def symbol_definition(text: str, name: str) -> str:
    marker = f'\t(symbol "{name}"'
    start = text.index(marker) + 1
    return balanced_block(text, start)


def assert_symbol_pin(block: str, number: str, name: str) -> None:
    number_token = f'(number "{number}"'
    name_token = f'(name "{name}"'
    assert block.count(number_token) == 1, (number, block.count(number_token))
    assert block.count(name_token) == 1, (name, block.count(name_token))


def footprint_pads(text: str) -> dict[str, tuple[float, float, float, float, float, float]]:
    result: dict[str, tuple[float, float, float, float, float, float]] = {}
    for match in re.finditer(
        r'\(pad\s+([^\s]+)\s+thru_hole\s+[^\s]+\s+'
        r'\(at\s+([-\d.]+)\s+([-\d.]+)\)\s+'
        r'\(size\s+([-\d.]+)\s+([-\d.]+)\)\s+'
        r'\(drill\s+oval\s+([-\d.]+)\s+([-\d.]+)\)',
        text,
    ):
        pad = match.group(1).strip('"')
        result[pad] = tuple(float(value) for value in match.groups()[1:])
    return result


def assert_generator_contracts(input_text: str, output_text: str) -> None:
    for token in (
        'add_part(sch, "MerrinLab_PrototypeA:WQP518MA_APPLICATION", "J40",',
        'label_pin(sch, "J40", "1", "INPUT_TIP")',
        'label_pin(sch, "J40", "2", "GND")',
        'label_pin(sch, "J40", "3", "GND")',
    ):
        assert token in input_text, token

    for token in (
        'add_part(sch, "MerrinLab_PrototypeA:WQP518MA_APPLICATION", "J70",',
        'label_pin(sch, "J70", "1", "OUTPUT_TIP")',
        'sch.no_connects.add(position=pin_position(sch, "J70", "2"))',
        'label_pin(sch, "J70", "3", "GND")',
    ):
        assert token in output_text, token


def main() -> None:
    for required in (
        SHEET04,
        SHEET07,
        LIBRARY,
        INPUT_GENERATOR,
        OUTPUT_GENERATOR,
        AUDIT,
        REVIEW,
        CONTRACT,
        FOOTPRINT,
    ):
        assert required.exists(), required

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["schema_version"] == 1
    authority = audit["authority"]
    assert authority["base_commit"] == "651d594e3c9993b2fdc6ca527328887458a7d849"
    assert authority["pcb_authorised"] is False
    assert authority["panel_fabrication_authorised"] is False
    assert authority["purchasing_authorised"] is False

    candidate = audit["candidate"]
    assert candidate["exact_orderable_name"] == "WQP518MA"
    assert candidate["status"] == "RETAINED_CANDIDATE_NOT_ACCEPTED"
    assert candidate["contacts"] == {
        "1": "TIP",
        "2": "TIP_NORMAL",
        "3": "SLEEVE",
        "no_plug_state": "contacts 1 and 2 closed",
        "plug_inserted_state": "contacts 1 and 2 open; contact 1 remains plug tip",
    }
    assert audit["supplier_evidence"]["drawing_model_label"] == "PJ398SM"
    assert audit["supplier_evidence"]["manufacturer_controlled_wqp518ma_drawing_found"] is False

    library = LIBRARY.read_text(encoding="utf-8")
    symbol = symbol_definition(library, "WQP518MA_APPLICATION")
    assert_symbol_pin(symbol, "1", "TIP")
    assert_symbol_pin(symbol, "2", "TIP_NORMAL")
    assert_symbol_pin(symbol, "3", "SLEEVE")
    assert '(property "Footprint" ""' in symbol

    rows04 = instances(SHEET04)
    rows07 = instances(SHEET07)
    j40 = one(rows04, "J40")
    j70 = one(rows07, "J70")
    for row, value in (
        (j40, "WQP518MA / THONKICONN INPUT"),
        (j70, "WQP518MA / THONKICONN OUTPUT"),
    ):
        assert row["lib_id"] == "MerrinLab_PrototypeA:WQP518MA_APPLICATION", row
        assert row["value"] == value, row
        assert row["footprint"] == "", row

    assert_generator_contracts(
        INPUT_GENERATOR.read_text(encoding="utf-8"),
        OUTPUT_GENERATOR.read_text(encoding="utf-8"),
    )

    use = audit["schematic_use"]
    assert use["J40"] == {
        "role": "INPUT",
        "pin_1": "INPUT_TIP",
        "pin_2": "GND",
        "pin_3": "GND",
        "normal_contact_required": True,
        "no_cable_result": "INPUT_TIP is grounded through the closed 1-2 contact",
    }
    assert use["J70"] == {
        "role": "OUTPUT",
        "pin_1": "OUTPUT_TIP",
        "pin_2": "NO_CONNECT",
        "pin_3": "GND",
        "normal_contact_required": False,
    }

    raw = FOOTPRINT.read_bytes()
    actual_hash = hashlib.sha256(raw).hexdigest()
    footprint = audit["footprint_candidate"]
    assert footprint["source_commit"] == EXPECTED_SOURCE_COMMIT
    assert footprint["source_blob_sha"] == EXPECTED_SOURCE_BLOB
    assert footprint["sha256"] == EXPECTED_SHA256 == actual_hash
    assert footprint["source_testing_status"] == "UNTESTED BY UPSTREAM LIBRARY"

    pads = footprint_pads(raw.decode("utf-8"))
    expected_pads = {
        "T": (0.0, -4.92, 2.6, 2.6, 1.6, 0.6),
        "TN": (0.0, 3.38, 2.6, 2.6, 1.6, 0.6),
        "S": (0.0, 6.48, 3.1, 2.3, 1.6, 0.6),
    }
    assert pads == expected_pads, pads
    assert set(footprint["pads"]) == {"T", "TN", "S"}

    mapping = footprint["symbol_pad_mapping"]
    assert mapping["schematic_identifiers"] == ["1", "2", "3"]
    assert mapping["footprint_identifiers"] == ["T", "TN", "S"]
    assert mapping["direct_assignment_valid"] is False
    assert set(mapping["schematic_identifiers"]).isdisjoint(
        mapping["footprint_identifiers"]
    )

    panel = audit["panel_and_mounting"]
    assert panel["candidate_panel_hole_mm"] == 6.5
    assert panel["candidate_panel_hole_status"] == "DERIVED_CLEARANCE_NOT_ACCEPTED"
    assert panel["exact_thread"] == "UNKNOWN"
    assert panel["exact_nut"] == "NOT_SELECTED"
    assert panel["exact_washer"] == "NOT_SELECTED"
    assert panel["maximum_panel_thickness"] == "UNKNOWN"
    assert panel["panel_to_pcb_seating_distance"] == "NOT_YET_ACCEPTED"

    decision = audit["decision"]
    assert decision == {
        "contact_contract": "PASS",
        "current_schematic_use": "PASS",
        "exact_orderable_identity": "BLOCKED_BY_WQP518MA_TO_PJ398SM_DRAWING_EQUIVALENCE",
        "direct_source_footprint_assignment": "FAIL_PAD_IDENTIFIER_MISMATCH",
        "panel_geometry": "BLOCKED",
        "mounting_hardware": "BLOCKED",
        "footprints_assigned": False,
        "overall": "RETURN_FOR_EVIDENCE_AND_NUMERIC_FOOTPRINT_REPAIR",
    }

    review_text = REVIEW.read_text(encoding="utf-8")
    contract_text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "FOOTPRINTS ASSIGNED                         NONE",
        "PCB / PANEL FAB / PURCHASING                BLOCKED",
        "source footprint uses semantic pad identifiers",
        "panel-to-PCB seating distance",
    ):
        assert token.lower() in review_text.lower(), token
    assert "no direct assignment" in contract_text.lower()

    print("J40 switched-input and quiet-no-cable contact contract: PASS")
    print("J70 output contact and unused-normal contract: PASS")
    print("WQP518MA numeric symbol pin contract: PASS")
    print("Pinned PJ398SM/WQP518MA candidate footprint bytes and geometry: PASS")
    print("Unsafe numeric-to-semantic direct footprint assignment: BLOCKED AS REQUIRED")
    print("Exact drawing equivalence, panel stack and mounting hardware: BLOCKED AS REQUIRED")
    print("J40/J70 footprints remain blank: PASS")
    print("PCB placement, routing, panel fabrication and purchasing remain blocked.")


if __name__ == "__main__":
    main()
