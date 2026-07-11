#!/usr/bin/env python3
"""Run the reviewed sheet-05 generator with explicit KiCad label directions.

The pinned kicad-sch-api text manager accepts direction strings. Passing the
HierarchicalLabelShape enum object makes it fall back to ``input``. This wrapper
preserves the reviewed electrical design and normalises only that API boundary.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_memory_ghost_wet_sheet.py")
SPEC = importlib.util.spec_from_file_location("memory_ghost_wet_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load Memory/Ghost/wet capture: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)


def direction_safe_add_hier(sch, name, position, shape, end):
    direction = shape.value if hasattr(shape, "value") else str(shape)
    sch.add_hierarchical_label(name, position=position, shape=direction, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def main() -> None:
    base.add_hier = direction_safe_add_hier
    base.build()
    print("Sheet-05 hierarchical label directions emitted as explicit strings")


if __name__ == "__main__":
    main()
