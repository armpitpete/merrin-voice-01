#!/usr/bin/env python3
"""Run the reviewed sheet-06 generator with explicit label directions.

This layers the accepted collision-free reference repair from v2 with one API
boundary correction: kicad-sch-api expects hierarchy directions as strings,
not HierarchicalLabelShape enum objects. Electrical topology is unchanged.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_return_break_limiter_sheet_v2.py")
SPEC = importlib.util.spec_from_file_location("return_break_limiter_capture_v2", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load Return capture wrapper: {BASE_PATH}")

reviewed = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reviewed
SPEC.loader.exec_module(reviewed)


def direction_safe_add_hier(sch, name, position, shape, end):
    direction = shape.value if hasattr(shape, "value") else str(shape)
    sch.add_hierarchical_label(name, position=position, shape=direction, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def main() -> None:
    reviewed.base.add_hier = direction_safe_add_hier
    reviewed.main()
    print("Sheet-06 hierarchical label directions emitted as explicit strings")


if __name__ == "__main__":
    main()
