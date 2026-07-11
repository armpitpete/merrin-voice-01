#!/usr/bin/env python3
"""Run sheet 05 and repair exact output directions in the native file.

The pinned kicad-sch-api public ``add_hierarchical_label`` method accepts a
``shape`` argument but does not forward it to the created label. Every new
label therefore serialises as ``input``. This wrapper preserves the reviewed
electrical capture, then changes only the named sheet-05 output to ``output``.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_memory_ghost_wet_sheet.py")
SPEC = importlib.util.spec_from_file_location("memory_ghost_wet_capture_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load Memory/Ghost/wet capture: {BASE_PATH}")

base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)


def repair_output_directions(path: Path, output_names: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for name in output_names:
        pattern = re.compile(
            rf'(\(hierarchical_label "{re.escape(name)}"\s+\(shape )([^)]+)(\))',
            re.MULTILINE,
        )
        text, count = pattern.subn(
            lambda match: match.group(1) + "output" + match.group(3),
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"Expected exactly one hierarchical label for {name}, found {count}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    base.build()
    repair_output_directions(base.SHEET_FILE, base.HIER_OUTPUTS)
    print("Sheet-05 native output direction repaired: WET_MIX=output")


if __name__ == "__main__":
    main()
