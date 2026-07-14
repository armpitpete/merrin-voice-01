#!/usr/bin/env python3
"""Audit actual KiCad 10 footprint geometry against sheet-07 package drawings."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
AUDIT = ROOT / "OUTPUT_MUTE_FOOTPRINT_DIMENSION_AUDIT.json"
BUILD = Path("build/footprints")
SOT23_FILE = BUILD / "SOT-23.kicad_mod"
SMDIP4_FILE = BUILD / "SMDIP-4_W7.62mm.kicad_mod"


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
        result.append(balanced_block(text, start))
        offset = start + len(result[-1])


def pads(text: str) -> dict[int, dict[str, float]]:
    result: dict[int, dict[str, float]] = {}
    for block in blocks(text, "(pad "):
        match_number = re.match(r'\(pad\s+"?(\d+)"?', block)
        if not match_number or " smd " not in block:
            continue
        at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
        size = re.search(r'\(size\s+([-\d.]+)\s+([-\d.]+)', block)
        assert at and size, block[:120]
        result[int(match_number.group(1))] = {
            "x": float(at.group(1)),
            "y": float(at.group(2)),
            "sx": float(size.group(1)),
            "sy": float(size.group(2)),
        }
    return result


def courtyard(text: str) -> tuple[float, float]:
    points: list[tuple[float, float]] = []
    for token in ("(fp_line", "(fp_rect", "(fp_arc"):
        for block in blocks(text, token):
            if "F.CrtYd" not in block:
                continue
            for x, y in re.findall(
                r'\((?:start|end|mid|center)\s+([-\d.]+)\s+([-\d.]+)', block
            ):
                points.append((float(x), float(y)))
    assert points, "No F.CrtYd geometry found"
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return max(xs) - min(xs), max(ys) - min(ys)


def close(actual: float, expected: float, tolerance: float = 0.01) -> None:
    assert math.isclose(actual, expected, abs_tol=tolerance), (actual, expected)


def validate_sot23(text: str, rules: dict[str, float]) -> None:
    p = pads(text)
    assert set(p) == {1, 2, 3}, p
    close(p[1]["x"], p[2]["x"])
    close(abs(p[1]["y"] - p[2]["y"]), rules["pad_1_2_pitch"])
    assert p[3]["x"] > p[1]["x"]
    close(p[3]["y"], (p[1]["y"] + p[2]["y"]) / 2)
    for pad in p.values():
        assert pad["sx"] >= rules["minimum_pad_x"]
        assert pad["sy"] >= rules["minimum_pad_y"]
    cx, cy = courtyard(text)
    assert max(cx, cy) >= rules["minimum_courtyard_x"]
    assert min(cx, cy) >= rules["minimum_courtyard_y"]
    print(
        "SOT-23 dimensional audit: PASS — "
        f"1/2 pitch {abs(p[1]['y'] - p[2]['y']):.2f} mm, "
        f"pad {p[1]['sx']:.2f} x {p[1]['sy']:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def validate_smdip4(text: str, rules: dict[str, float]) -> None:
    p = pads(text)
    assert set(p) == {1, 2, 3, 4}, p
    left_x = (p[1]["x"] + p[2]["x"]) / 2
    right_x = (p[3]["x"] + p[4]["x"]) / 2
    close(abs(right_x - left_x), rules["row_spacing"])
    close(abs(p[1]["y"] - p[2]["y"]), rules["pin_pitch"])
    close(abs(p[3]["y"] - p[4]["y"]), rules["pin_pitch"])
    assert p[1]["x"] < p[4]["x"] and p[1]["y"] < p[2]["y"]
    for pad in p.values():
        assert pad["sx"] >= rules["minimum_pad_x"]
        assert pad["sy"] >= rules["minimum_pad_y"]
    cx, cy = courtyard(text)
    assert max(cx, cy) >= rules["minimum_courtyard_x"]
    assert min(cx, cy) >= rules["minimum_courtyard_y"]
    print(
        "Option-7 SMD-4 dimensional audit: PASS — "
        f"row {abs(right_x-left_x):.2f} mm, "
        f"pitch {abs(p[1]['y']-p[2]['y']):.2f} mm, "
        f"pad {p[1]['sx']:.2f} x {p[1]['sy']:.2f} mm, "
        f"courtyard {cx:.2f} x {cy:.2f} mm"
    )


def main() -> None:
    for required in (AUDIT, SOT23_FILE, SMDIP4_FILE):
        assert required.exists(), required
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["authority"]["pcb_authorised"] is False

    q70 = data["parts"]["Q70"]
    q71 = data["parts"]["Q71"]
    u70 = data["parts"]["U70"]
    assert q70["footprint"] == q71["footprint"] == "Package_TO_SOT_SMD:SOT-23"
    assert q70["manufacturer_package"] == "SOT-23 / TO-236, CASE 318-08"
    assert q71["dimensions_mm"]["outer_lead_pitch"] == 1.9
    assert q71["dimensions_mm"]["body_length_max"] == 3.0
    assert q71["dimensions_mm"]["overall_width_max"] == 2.5
    assert u70["dimensions_mm"]["lead_row_spacing_nominal"] == 7.62
    assert u70["dimensions_mm"]["lead_pitch_nominal"] == 2.54
    assert u70["dimensions_mm"]["overall_span_max"] == 9.98

    validate_sot23(
        SOT23_FILE.read_text(encoding="utf-8"),
        data["acceptance_rules"]["sot23"],
    )
    validate_smdip4(
        SMDIP4_FILE.read_text(encoding="utf-8"),
        data["acceptance_rules"]["smdip4_option7"],
    )
    print("Q70/Q71/U70 package-to-footprint dimensional compatibility: PASS")
    print("PCB placement, courtyard interaction and assembly process remain blocked.")


if __name__ == "__main__":
    main()
