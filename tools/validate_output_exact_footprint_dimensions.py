#!/usr/bin/env python3
"""Audit immutable official KiCad footprint geometry against each exact package."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
AUDIT = ROOT / "OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json"
REVIEW = ROOT / "OUTPUT_MUTE_FAULT_PATH_EXACT_PART_REVIEW.md"
VALIDATION = ROOT / "07_OUTPUT_MUTE_PROTECTION_VALIDATION.md"


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
                return text[start:index + 1]
    raise AssertionError(f"Unterminated S-expression at {start}")


def blocks(text: str, token: str) -> list[str]:
    result: list[str] = []
    offset = 0
    while True:
        start = text.find(token, offset)
        if start == -1:
            return result
        block = balanced_block(text, start)
        result.append(block)
        offset = start + len(block)


def pads(text: str) -> dict[int, tuple[float, float, float, float]]:
    result: dict[int, tuple[float, float, float, float]] = {}
    for block in blocks(text, "(pad "):
        number = re.match(r'\(pad\s+"?(\d+)"?', block)
        if not number or " smd " not in block:
            continue
        at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
        size = re.search(r'\(size\s+([-\d.]+)\s+([-\d.]+)', block)
        assert at and size, block[:160]
        result[int(number.group(1))] = tuple(
            float(value) for value in (*at.groups(), *size.groups())
        )
    return result


def courtyard(text: str) -> tuple[float, float]:
    points: list[tuple[float, float]] = []
    for token in ("(fp_line", "(fp_rect", "(fp_arc"):
        for block in blocks(text, token):
            if "F.CrtYd" not in block:
                continue
            points.extend(
                (float(x), float(y))
                for x, y in re.findall(
                    r'\((?:start|end|mid|center)\s+([-\d.]+)\s+([-\d.]+)',
                    block,
                )
            )
    assert points, "No F.CrtYd geometry found"
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return max(xs) - min(xs), max(ys) - min(ys)


def close(actual: float, expected: float, tolerance: float = 0.001) -> None:
    assert math.isclose(actual, expected, abs_tol=tolerance), (actual, expected)


def locked_text(snapshot: dict[str, object], source_commit: str) -> str:
    path = Path(str(snapshot["path"]))
    assert path.exists(), path
    assert snapshot["source_commit"] == source_commit
    assert source_commit in str(snapshot["source_url"])
    assert re.fullmatch(r"[0-9a-f]{40}", str(snapshot["github_blob_sha"]))
    raw = path.read_bytes()
    actual_hash = hashlib.sha256(raw).hexdigest()
    assert actual_hash == snapshot["sha256"], (
        path,
        actual_hash,
        snapshot["sha256"],
    )
    return raw.decode("utf-8")


def assert_exact_pad(
    actual: tuple[float, float, float, float], expected: list[float]
) -> None:
    assert len(expected) == 4
    for found, required in zip(actual, expected, strict=True):
        close(found, float(required))


def validate_sot23_snapshot(
    text: str, snapshot: dict[str, object]
) -> tuple[dict[int, tuple[float, float, float, float]], tuple[float, float]]:
    geometry = snapshot["geometry_mm"]
    p = pads(text)
    assert set(p) == {1, 2, 3}, p
    for number in (1, 2, 3):
        assert_exact_pad(p[number], geometry[f"pad_{number}"])

    close(p[1][0], p[2][0])
    close(abs(p[1][1] - p[2][1]), 1.9)
    assert p[3][0] > p[1][0]
    close(p[3][1], (p[1][1] + p[2][1]) / 2)

    cx, cy = courtyard(text)
    close(cx, geometry["courtyard"][0])
    close(cy, geometry["courtyard"][1])
    return p, (cx, cy)


def validate_q70_case318(
    p: dict[int, tuple[float, float, float, float]],
    courtyard_size: tuple[float, float],
    q70: dict[str, object],
) -> None:
    dims = q70["dimensions_mm"]
    pitch = abs(p[1][1] - p[2][1])
    assert dims["outer_lead_pitch_min"] <= pitch <= dims["outer_lead_pitch_max"]
    close(dims["lead_pitch_nominal"], 0.95)
    cx, cy = courtyard_size
    assert max(cx, cy) > dims["body_length_max"]
    assert min(cx, cy) > dims["overall_width_max"]
    assert p[1][2] > dims["lead_length_max"]
    assert p[1][3] > dims["lead_width_max"]
    assert "CASE 318-08" in q70["manufacturer_package"]
    assert "TO-236" in q70["equivalence_basis"]
    print(
        "Q70 CASE 318-08 independent dimensional audit: PASS — "
        f"lead pitch {pitch:.2f} mm, pad {p[1][2]:.2f} x {p[1][3]:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def validate_q71_to236ab(
    p: dict[int, tuple[float, float, float, float]],
    courtyard_size: tuple[float, float],
    q71: dict[str, object],
) -> None:
    dims = q71["dimensions_mm"]
    close(abs(p[1][1] - p[2][1]), dims["outer_lead_pitch"])
    cx, cy = courtyard_size
    assert max(cx, cy) > dims["body_length_max"]
    assert min(cx, cy) > dims["overall_width_max"]
    assert p[1][2] > dims["lead_length_max"]
    assert p[1][3] > dims["lead_width_max"]
    print(
        "Q71 TO-236AB independent dimensional audit: PASS — "
        f"pad {p[1][2]:.2f} x {p[1][3]:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def validate_smdip4(
    text: str, snapshot: dict[str, object], u70: dict[str, object]
) -> None:
    geometry = snapshot["geometry_mm"]
    p = pads(text)
    assert set(p) == {1, 2, 3, 4}, p
    for number in (1, 2, 3, 4):
        assert_exact_pad(p[number], geometry[f"pad_{number}"])

    left_x = (p[1][0] + p[2][0]) / 2
    right_x = (p[3][0] + p[4][0]) / 2
    close(abs(right_x - left_x), u70["dimensions_mm"]["lead_row_spacing_nominal"])
    close(abs(p[1][1] - p[2][1]), u70["dimensions_mm"]["lead_pitch_nominal"])
    close(abs(p[3][1] - p[4][1]), u70["dimensions_mm"]["lead_pitch_nominal"])
    assert p[1][0] == p[2][0] < p[3][0] == p[4][0]
    assert p[1][1] == p[4][1] < p[2][1] == p[3][1]

    cx, cy = courtyard(text)
    close(cx, geometry["courtyard"][0])
    close(cy, geometry["courtyard"][1])
    assert cx > u70["dimensions_mm"]["overall_span_max"]
    assert cy > u70["dimensions_mm"]["body_width_max"]
    assert p[1][2] > u70["dimensions_mm"]["terminal_length_max"]
    assert p[1][3] > u70["dimensions_mm"]["lead_width_max"]

    print(
        "U70 option-7 SMD-4 dimensional audit: PASS — "
        f"row {abs(right_x-left_x):.2f} mm, "
        f"pitch {abs(p[1][1]-p[2][1]):.2f} mm, "
        f"pads {p[1][2]:.2f} x {p[1][3]:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def main() -> None:
    assert AUDIT.exists(), AUDIT
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["schema_version"] == 3
    authority = data["authority"]
    assert authority["pcb_authorised"] is False
    assert authority["accepted_geometry_is_project_local"] is True
    assert authority["source_repository"] == "KiCad/kicad-footprints"
    source_commit = authority["source_commit"]
    assert re.fullmatch(r"[0-9a-f]{40}", source_commit)
    assert source_commit in authority["source_commit_url"]

    q70 = data["parts"]["Q70"]
    q71 = data["parts"]["Q71"]
    u70 = data["parts"]["U70"]
    snapshots = data["footprint_snapshots"]

    assert q70["footprint"] == q71["footprint"] == "Package_TO_SOT_SMD:SOT-23"
    assert q70["snapshot"] == q71["snapshot"] == "sot23"
    assert u70["footprint"] == "Package_DIP:SMDIP-4_W7.62mm"
    assert u70["snapshot"] == "smdip4"

    sot_text = locked_text(snapshots["sot23"], source_commit)
    sot_pads, sot_courtyard = validate_sot23_snapshot(
        sot_text, snapshots["sot23"]
    )
    validate_q70_case318(sot_pads, sot_courtyard, q70)
    validate_q71_to236ab(sot_pads, sot_courtyard, q71)

    validate_smdip4(
        locked_text(snapshots["smdip4"], source_commit),
        snapshots["smdip4"],
        u70,
    )

    for authority_path in (REVIEW, VALIDATION):
        text = authority_path.read_text(encoding="utf-8")
        assert "U70 25 C datasheet-bound saturation proof" in text
        assert "full-temperature release behaviour remains Gate C" in text

    print("U70 25 C temperature-bound authority: PASS")
    print("Immutable official KiCad source revision: PASS")
    print("Q70/Q71/U70 package-to-footprint dimensional compatibility: PASS")
    print("PCB placement, neighbour clearances and assembly process remain blocked.")


if __name__ == "__main__":
    main()
