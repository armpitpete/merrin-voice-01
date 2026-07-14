#!/usr/bin/env python3
"""Audit SHA-locked official KiCad footprint geometry against package records."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
AUDIT = ROOT / "OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json"


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
            if 'F.CrtYd' not in block:
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


def locked_text(snapshot: dict[str, object]) -> str:
    path = Path(str(snapshot["path"]))
    assert path.exists(), path
    raw = path.read_bytes()
    actual_hash = hashlib.sha256(raw).hexdigest()
    assert actual_hash == snapshot["sha256"], (path, actual_hash, snapshot["sha256"])
    return raw.decode("utf-8")


def assert_exact_pad(
    actual: tuple[float, float, float, float], expected: list[float]
) -> None:
    assert len(expected) == 4
    for found, required in zip(actual, expected, strict=True):
        close(found, float(required))


def validate_sot23(text: str, snapshot: dict[str, object], q71: dict[str, object]) -> None:
    geometry = snapshot["geometry_mm"]
    p = pads(text)
    assert set(p) == {1, 2, 3}, p
    for number in (1, 2, 3):
        assert_exact_pad(p[number], geometry[f"pad_{number}"])

    # Manufacturer orientation: pins 1/2 on one side, pin 3 opposite.
    close(p[1][0], p[2][0])
    close(abs(p[1][1] - p[2][1]), q71["dimensions_mm"]["outer_lead_pitch"])
    assert p[3][0] > p[1][0]
    close(p[3][1], (p[1][1] + p[2][1]) / 2)

    cx, cy = courtyard(text)
    close(cx, geometry["courtyard"][0])
    close(cy, geometry["courtyard"][1])
    assert cx > q71["dimensions_mm"]["overall_width_max"]
    assert cy > q71["dimensions_mm"]["body_length_max"]
    assert p[1][2] > q71["dimensions_mm"]["lead_length_max"]
    assert p[1][3] > q71["dimensions_mm"]["lead_width_max"]

    print(
        "SOT-23 snapshot audit: PASS — "
        f"pads {p[1][2]:.3f} x {p[1][3]:.3f} mm, "
        f"1/2 pitch {abs(p[1][1] - p[2][1]):.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def validate_smdip4(text: str, snapshot: dict[str, object], u70: dict[str, object]) -> None:
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

    # Manufacturer orientation: 1/2 left, 4/3 right, pin 1 at notched end.
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
        "Option-7 SMD-4 snapshot audit: PASS — "
        f"row {abs(right_x-left_x):.2f} mm, "
        f"pitch {abs(p[1][1]-p[2][1]):.2f} mm, "
        f"pads {p[1][2]:.2f} x {p[1][3]:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def main() -> None:
    assert AUDIT.exists(), AUDIT
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["schema_version"] == 2
    assert data["authority"]["pcb_authorised"] is False
    assert data["authority"]["source"].startswith("SHA-256-locked snapshots")

    q70 = data["parts"]["Q70"]
    q71 = data["parts"]["Q71"]
    u70 = data["parts"]["U70"]
    snapshots = data["footprint_snapshots"]

    assert q70["footprint"] == q71["footprint"] == "Package_TO_SOT_SMD:SOT-23"
    assert q70["snapshot"] == q71["snapshot"] == "sot23"
    assert u70["footprint"] == "Package_DIP:SMDIP-4_W7.62mm"
    assert u70["snapshot"] == "smdip4"
    assert q70["manufacturer_package"] == "SOT-23 / TO-236, CASE 318-08"

    validate_sot23(locked_text(snapshots["sot23"]), snapshots["sot23"], q71)
    validate_smdip4(locked_text(snapshots["smdip4"]), snapshots["smdip4"], u70)

    print("Q70/Q71/U70 package-to-footprint dimensional compatibility: PASS")
    print("Official KiCad snapshot hashes: PASS")
    print("PCB placement, neighbour clearances and assembly process remain blocked.")


if __name__ == "__main__":
    main()
