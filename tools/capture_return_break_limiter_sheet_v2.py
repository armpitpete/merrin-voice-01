#!/usr/bin/env python3
"""Run the reviewed sheet-06 generator with collision-free capacitor references.

The base generator intentionally retains the accepted electrical design. Its
first OPA1679 decoupling loop uses C610/C611, and the later Break/Return
feedback capacitors accidentally reused those references. This wrapper changes
only the second occurrence of each duplicate:

- second C610 -> C640 (Break feedback/bandwidth capacitor)
- second C611 -> C641 (Return shaping/bandwidth capacitor)

No values, nets, topology, safety boundary, footprints, or mechanics change.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_return_break_limiter_sheet.py")
SPEC = importlib.util.spec_from_file_location("return_break_limiter_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load Return capture generator: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)

original_add_two_pin = base.add_two_pin
seen: dict[str, int] = {}


def collision_free_add_two_pin(
    sch,
    lib_id,
    reference,
    value,
    position,
    net1,
    net2,
    footprint="",
):
    seen[reference] = seen.get(reference, 0) + 1

    replacement = reference
    if reference == "C610" and seen[reference] == 2:
        replacement = "C640"
    elif reference == "C611" and seen[reference] == 2:
        replacement = "C641"

    return original_add_two_pin(
        sch,
        lib_id,
        replacement,
        value,
        position,
        net1,
        net2,
        footprint,
    )


def main() -> None:
    base.add_two_pin = collision_free_add_two_pin
    base.build()

    if seen.get("C610") != 2 or seen.get("C611") != 2:
        raise RuntimeError(
            "Expected exactly two attempted uses each of C610 and C611; "
            f"observed C610={seen.get('C610')} C611={seen.get('C611')}"
        )

    print("Return reference repair applied: second C610->C640, second C611->C641")


if __name__ == "__main__":
    main()
