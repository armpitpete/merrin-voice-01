#!/usr/bin/env python3
"""Run sheet 06, restore SSI pin attachments, and set native outputs."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reviewed = load(
    "return_break_limiter_capture_v2",
    Path(__file__).with_name("capture_return_break_limiter_sheet_v2.py"),
)
physical = load(
    "return_ssi_physical_repair",
    Path(__file__).with_name("repair_return_ssi_units.py"),
)
buffer = load(
    "return_opa4196_physical_repair",
    Path(__file__).with_name("repair_ssi2164_buffer_opa4196_units.py"),
)


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
    physical.main()
    buffer.repair_sheet06()
    repair_output_directions(reviewed.base.SHEET_FILE, reviewed.base.HIER_OUTPUTS)
    print(
        "Sheet-06 native output directions repaired: "
        "RETURN_LIMITED/RETURN_FEED/ABSENCE_INFLUENCE=output"
    )


if __name__ == "__main__":
    main()
