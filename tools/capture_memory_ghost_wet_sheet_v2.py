#!/usr/bin/env python3
"""Run sheet 05, repair SSI pins, and set the exact native output direction."""

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


base = load(
    "memory_ghost_wet_capture_base",
    Path(__file__).with_name("capture_memory_ghost_wet_sheet.py"),
)
physical = load(
    "memory_ghost_wet_ssi_repair",
    Path(__file__).with_name("repair_memory_ghost_wet_ssi_units.py"),
)
buffer = load(
    "memory_ghost_wet_opa4196_repair",
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
    base.build()
    physical.main()
    buffer.repair_sheet05()
    repair_output_directions(base.SHEET_FILE, base.HIER_OUTPUTS)
    print("Sheet-05 native output direction repaired: WET_MIX=output")


if __name__ == "__main__":
    main()
