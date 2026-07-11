#!/usr/bin/env python3
"""Run sheet 06 and repair exact output directions in the native file.

This layers the accepted collision-free reference repair from v2 with the
pinned kicad-sch-api workaround. Its public hierarchical-label method ignores
``shape``; this wrapper changes only the three locked sheet-06 exports from the
default ``input`` serialisation to ``output``. Electrical topology is unchanged.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_return_break_limiter_sheet_v2.py")
SPEC = importlib.util.spec_from_file_location("return_break_limiter_capture_v2", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load Return capture wrapper: {BASE_PATH}")

reviewed = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reviewed
SPEC.loader.exec_module(reviewed)


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
    reviewed.main()
    repair_output_directions(reviewed.base.SHEET_FILE, reviewed.base.HIER_OUTPUTS)
    print(
        "Sheet-06 native output directions repaired: "
        "RETURN_LIMITED/RETURN_FEED/ABSENCE_INFLUENCE=output"
    )


if __name__ == "__main__":
    main()
