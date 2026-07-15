#!/usr/bin/env python3
"""Validate Gate-B lane 02 jack evidence and the unassigned numeric footprint."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
SHEET04 = ROOT / "04_INPUT_PRESSURE_ABSENCE.kicad_sch"
SHEET07 = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
FP_TABLE = ROOT / "fp-lib-table"
INPUT_GENERATOR = Path("tools/capture_input_pressure_absence_sheet.py")
OUTPUT_GENERATOR = Path("tools/capture_output_mute_protection_sheet.py")
AUDIT = ROOT / "INPUT_OUTPUT_JACK_AUDIT.json"
REVIEW = ROOT / "INPUT_OUTPUT_JACK_EXACT_PART_REVIEW.md"
CONTRACT = ROOT / "JACK_EXACT_PART_EDIT_CONTRACT.md"
MEASUREMENT = ROOT / "WQP518MA_PANEL_STACK_MEASUREMENT_RECORD.md"
SOURCE_FP = (
    ROOT
    / "jack-footprint-audits"
    / "KiCad_Official_Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles.kicad_mod"
)
NUMERIC_FP = (
    ROOT
    / "MerrinLab_PrototypeA.pretty"
    / "Jack_3.5mm_Thonkiconn_WQP518MA_Numeric.kicad_mod"
)

SOURCE_COMMIT = "7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd"
SOURCE_BLOB = "6c9440c957bf566ae79058cdab7afabfb86955d8"
SOURCE_SHA256 = "8ae08dd1e353c7fdbea2827c890ecd150e6f5f528598770bec85a8f2422b98cc"
NUMERIC_SHA256 = "e9e095c63fa39dfd306a45755b6e8e9048e795b8592a6eeba3bf6ab734ed3685"
FOOTPRINT_ID = "MerrinLab_PrototypeA:Jack_3.5mm_Thonkiconn_WQP518MA_Numeric"


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


def sexp_blocks(text: str, token: str) -> list[str]:
    result: list[str] = []
    offset = 0
    while True:
        start = text.find(token, offset)
        if start == -1:
            return result
        block = balanced_block(text, start)
        result.append(block)
        offset = start + len(block)


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
    assert block.count(f'(number "{number}"') == 1
    assert block.count(f'(name "{name}"') == 1


def parse_pads(
    text: str,
) -> tuple[
    dict[str, tuple[float, float, float, float, float]],
    list[tuple[str, float, float, float]],
]:
    electrical: dict[str, tuple[float, float, float, float, float]] = {}
    npth: list[tuple[str, float, float, float]] = []
    for block in sexp_blocks(text, "(pad "):
        identifier_match = re.match(r'\(pad\s+(?:"([^"]*)"|([^\s]+))', block)
        assert identifier_match, block[:120]
        identifier = identifier_match.group(1)
        if identifier is None:
            identifier = identifier_match.group(2)
        at = re.search(
            r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+[-\d.]+)?\)', block
        )
        size = re.search(r'\(size\s+([-\d.]+)\s+([-\d.]+)\)', block)
        drill = re.search(r'\(drill\s+([-\d.]+)\)', block)
        assert at and size and drill, block[:200]
        x, y = (float(value) for value in at.groups())
        sx, sy = (float(value) for value in size.groups())
        diameter = float(drill.group(1))
        if " np_thru_hole " in block:
            npth.append((identifier, x, y, diameter))
        elif " thru_hole " in block:
            electrical[identifier] = (x, y, sx, sy, diameter)
    return electrical, npth


def close(actual: float, expected: float, tolerance: float = 0.001) -> None:
    assert math.isclose(actual, expected, abs_tol=tolerance), (actual, expected)


def assert_pad(
    actual: tuple[float, float, float, float, float],
    expected: list[float],
) -> None:
    assert len(expected) == 5
    for found, required in zip(actual, expected, strict=True):
        close(found, float(required))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    required = (
        SHEET04,
        SHEET07,
        LIBRARY,
        FP_TABLE,
        INPUT_GENERATOR,
        OUTPUT_GENERATOR,
        AUDIT,
        REVIEW,
        CONTRACT,
        MEASUREMENT,
        SOURCE_FP,
        NUMERIC_FP,
    )
    for path in required:
        assert path.exists(), path

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["schema_version"] == 2
    authority = audit["authority"]
    assert authority["base_commit"] == "651d594e3c9993b2fdc6ca527328887458a7d849"
    assert authority["pcb_authorised"] is False
    assert authority["panel_fabrication_authorised"] is False
    assert authority["purchasing_authorised"] is False

    supplier = audit["supplier_evidence"]
    assert supplier["drawing_model_label"] == "PJ398SM"
    assert (
        supplier["equivalence_scope"]
        == "SUPPLIER_CONTROLLED_CONTACT_AND_FOOTPRINT_EQUIVALENCE_ACCEPTED"
    )
    assert supplier["manufacturer_controlled_wqp518ma_drawing_found"] is False
    assert supplier["hardware_dimensions_published"] is False

    candidate = audit["candidate"]
    assert candidate["exact_orderable_name"] == "WQP518MA"
    assert candidate["status"] == "ACCEPTED_FOR_CONTACT_AND_PCB_FOOTPRINT_GEOMETRY_ONLY"
    assert candidate["contacts"] == {
        "1": "TIP",
        "2": "TIP_NORMAL",
        "3": "SLEEVE",
        "no_plug_state": "contacts 1 and 2 closed",
        "plug_inserted_state": "contacts 1 and 2 open; contact 1 remains plug tip",
    }

    library = LIBRARY.read_text(encoding="utf-8")
    symbol = symbol_definition(library, "WQP518MA_APPLICATION")
    assert_symbol_pin(symbol, "1", "TIP")
    assert_symbol_pin(symbol, "2", "TIP_NORMAL")
    assert_symbol_pin(symbol, "3", "SLEEVE")
    assert '(property "Footprint" ""' in symbol
    assert FOOTPRINT_ID not in library

    rows04 = instances(SHEET04)
    rows07 = instances(SHEET07)
    for row, value in (
        (one(rows04, "J40"), "WQP518MA / THONKICONN INPUT"),
        (one(rows07, "J70"), "WQP518MA / THONKICONN OUTPUT"),
    ):
        assert row["lib_id"] == "MerrinLab_PrototypeA:WQP518MA_APPLICATION", row
        assert row["value"] == value, row
        assert row["footprint"] == "", row
        assert FOOTPRINT_ID not in row["block"]

    assert_generator_contracts(
        INPUT_GENERATOR.read_text(encoding="utf-8"),
        OUTPUT_GENERATOR.read_text(encoding="utf-8"),
    )

    use = audit["schematic_use"]
    assert use["J40"]["normal_contact_required"] is True
    assert use["J40"]["pin_1"] == "INPUT_TIP"
    assert use["J40"]["pin_2"] == use["J40"]["pin_3"] == "GND"
    assert use["J70"]["pin_1"] == "OUTPUT_TIP"
    assert use["J70"]["pin_2"] == "NO_CONNECT"
    assert use["J70"]["pin_3"] == "GND"

    source = audit["official_source_footprint"]
    assert source["source_commit"] == SOURCE_COMMIT
    assert source["source_blob_sha"] == SOURCE_BLOB
    assert source["sha256"] == SOURCE_SHA256 == sha256(SOURCE_FP)
    source_pads, source_npth = parse_pads(SOURCE_FP.read_text(encoding="utf-8"))
    assert source_npth == []
    assert set(source_pads) == {"T", "TN", "S"}
    for identifier in ("T", "TN", "S"):
        assert_pad(source_pads[identifier], source["pads"][identifier])

    numeric = audit["project_numeric_footprint"]
    assert numeric["library_id"] == FOOTPRINT_ID
    assert numeric["sha256"] == NUMERIC_SHA256 == sha256(NUMERIC_FP)
    numeric_pads, numeric_npth = parse_pads(NUMERIC_FP.read_text(encoding="utf-8"))
    assert set(numeric_pads) == {"1", "2", "3"}
    for identifier in ("1", "2", "3"):
        assert_pad(numeric_pads[identifier], numeric["pads"][identifier])
    assert numeric_npth == [("", 0.0, 6.48, 3.0)]

    mapping = {"1": "T", "2": "TN", "3": "S"}
    for numeric_id, source_id in mapping.items():
        assert numeric_pads[numeric_id] == source_pads[source_id]
    assert numeric["mapping"] == {
        "1": "T / TIP",
        "2": "TN / TIP_NORMAL",
        "3": "S / SLEEVE",
    }
    assert numeric["geometry_status"] == "PASS"
    assert numeric["assignment_status"] == "BLOCKED_PENDING_INDEPENDENT_PANEL_STACK_REVIEW"

    fp_table = FP_TABLE.read_text(encoding="utf-8")
    assert '(name "MerrinLab_PrototypeA")' in fp_table
    assert '${KIPRJMOD}/MerrinLab_PrototypeA.pretty' in fp_table

    mechanical = candidate["published_mechanical_mm"]
    panel = audit["panel_and_mounting"]
    bushing_max = mechanical["bushing_diameter"] + mechanical["drawing_general_tolerance"]
    hole_min = panel["panel_hole_mm"]["nominal"] - panel["panel_hole_mm"]["minus"]
    radial_clearance = (hole_min - bushing_max) / 2
    close(radial_clearance, panel["minimum_radial_clearance_before_position_error_mm"])
    assert panel["maximum_total_panel_to_jack_axis_offset_target_mm"] < radial_clearance
    close(panel["panel_thickness_target_mm"], 1.6)
    available_thread = (
        mechanical["threaded_bushing_length_shown"]
        - panel["panel_thickness_target_mm"]
    )
    close(available_thread, panel["available_thread_above_panel_before_nut_mm"])
    close(available_thread, 2.9)
    assert "Hex Nuts" in panel["selected_nut"]
    assert panel["selected_washer"].startswith("NONE")
    assert panel["washer_thickness"].startswith("NOT_APPLICABLE")
    assert panel["hardware_stack_status"] == "USER_ATTESTED_PASS_PENDING_INDEPENDENT_REVIEW"
    assert "PROVISIONAL" in panel["panel_material"]

    attestation = audit["physical_fit_attestation"]
    assert attestation["superseded_attestation_status"] == "WITHDRAWN_WRONG_STACK"
    assert attestation["current_stack"] == "1.60 mm nominal panel plus Thonk hex nut; no washer"
    for key in (
        "bushing_passes_panel_hole_without_forcing",
        "secure_nut_engagement_through_1p60mm_panel",
        "nut_starts_without_cross_threading",
        "nut_clamps_before_bottoming",
        "housing_not_crushed_or_distorted",
        "jack_does_not_rotate_or_wobble",
        "tightening_does_not_lift_or_tilt_soldered_jack",
        "tightening_does_not_load_solder_terminals",
        "pcb_remains_flat",
        "panel_to_pcb_alignment",
        "barrel_relief_3mm_clears_physical_jack",
        "terminal_holes_remain_unobstructed",
    ):
        assert attestation[key] == "PASS", (key, attestation[key])
    assert attestation["exact_sample_measurements_recorded"] is False
    assert attestation["independent_review_status"] == "REQUIRED_BEFORE_FOOTPRINT_ASSIGNMENT"

    measurement_text = MEASUREMENT.read_text(encoding="utf-8")
    for token in (
        "PANEL NOMINAL THICKNESS                  1.60 MM",
        "MOUNTING HARDWARE                        THONK HEX NUT ONLY",
        "WASHER                                   NONE",
        "CORRECT NUT-ONLY PHYSICAL FIT            USER-ATTESTED PASS",
        "exact corrected-stack sample reading     NOT RECORDED",
        "INDEPENDENT REVIEW                       REQUIRED BEFORE FOOTPRINT ASSIGNMENT",
        "PCB placement, routing, panel fabrication and purchasing remain blocked",
    ):
        assert token in measurement_text, token

    validation = audit["validation"]
    assert validation == {
        "validated_head": "d1510cfcb4b85a3e6d17283d795b2a545ed4860a",
        "jack_workflow_run": 29368887533,
        "schematic_erc_run": 29368887574,
        "current_stage_authority_run": 29368887521,
        "jack_validator": "PASS",
        "hierarchical_erc": "PASS — 0 errors / 0 warnings",
        "footprint_assignment_remained_blank": True,
    }

    decision = audit["decision"]
    assert decision == {
        "contact_contract": "PASS",
        "current_schematic_use": "PASS",
        "supplier_controlled_wqp518ma_pj398sm_equivalence": (
            "PASS_FOR_CONTACT_AND_FOOTPRINT_GEOMETRY"
        ),
        "numeric_project_footprint": "PASS",
        "panel_hole_tolerance": "DERIVED_TARGET_RECORDED",
        "mounting_hardware": "HEX_NUT_ONLY_USER_ATTESTED_FIT_PASS",
        "panel_stack": "USER_ATTESTED_PASS_PENDING_INDEPENDENT_REVIEW",
        "panel_release": (
            "BLOCKED_PENDING_MATERIAL_SUPPLIER_FINISHED_THICKNESS_AND_SEATING_DISTANCE"
        ),
        "footprints_assigned": False,
        "overall": (
            "CORRECTED_PHYSICAL_FIT_RECORDED_INDEPENDENT_REVIEW_REQUIRED_BEFORE_ASSIGNMENT"
        ),
    }

    review_text = REVIEW.read_text(encoding="utf-8").lower()
    contract_text = CONTRACT.read_text(encoding="utf-8").lower()
    for token in (
        "supplier-controlled equivalence",
        "numeric project-local footprint",
        "correct nut-only physical fit               user-attested pass",
        "ready for independent review",
        "footprints assigned                         none",
        "pcb / panel fab / purchasing                blocked",
    ):
        assert token in review_text, token
    assert "no footprint assignment before the panel stack passes" in contract_text

    print("J40 switched-input and quiet-no-cable contact contract: PASS")
    print("J70 output contact and unused-normal contract: PASS")
    print("Thonk supplier-controlled WQP518MA/PJ398SM equivalence: PASS")
    print("Pinned official KiCad WQP/PJ398SM source geometry and hash: PASS")
    print("Numeric 1/2/3 project-local footprint geometry and hash: PASS")
    print("3 mm barrel-relief NPTH geometry: PASS")
    print("Derived 6.50 +0.10/-0.00 mm panel-hole target: PASS AS NON-FABRICATION TARGET")
    print("Corrected 1.60 mm nut-only physical fit: USER-ATTESTED PASS")
    print("Independent mechanical review before assignment: REQUIRED")
    print("J40/J70 footprint assignment remains blank: PASS")
    print("Panel material, supplier, finished thickness and exact seating: BLOCKED")
    print("PCB placement, routing, panel fabrication and purchasing remain blocked.")


if __name__ == "__main__":
    main()
