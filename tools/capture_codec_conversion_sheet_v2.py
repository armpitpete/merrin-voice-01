#!/usr/bin/env python3
"""Regenerate sheet 03 with U32 represented as the shared OPA1679 device.

U32 unit A and the common power unit remain on sheet 03. Units B/C/D are left
for sheet 07, preserving the locked seven-package / 28-channel OPA1679 budget.
This wrapper also repairs the pinned API's hierarchy-direction serialisation defect.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BASE_PATH = Path(__file__).with_name("capture_codec_conversion_sheet.py")
SUPPORT_PATH = Path(__file__).with_name("opa1679_multi_support.py")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


base = load("codec_capture_base", BASE_PATH)
support = load("opa1679_multi_support", SUPPORT_PATH)

ORIGINAL_APPEND = base.append_symbols
ORIGINAL_ADD_PART = base.add_part
ORIGINAL_LABEL_PIN = base.label_pin
U32_COMPONENTS = {}
U32_A_POSITION = (326.0, 251.0)
U32_POWER_POSITION = (361.56, 251.0)


def append_symbols() -> None:
    ORIGINAL_APPEND()
    support.append_symbol_library(base.SYMBOL_LIBRARY)


def add_part(sch, lib_id, reference, value, position, footprint=""):
    if reference == "U32" and lib_id.endswith("OPA1679_PW_APPLICATION"):
        unit_a = sch.components.add(
            lib_id=support.LIB_ID,
            reference=support.REFERENCE,
            value=support.VALUE,
            position=U32_A_POSITION,
            footprint="",
            unit=1,
        )
        power = sch.components.add(
            lib_id=support.LIB_ID,
            reference=support.REFERENCE,
            value=support.VALUE,
            position=U32_POWER_POSITION,
            footprint="",
            unit=5,
        )
        U32_COMPONENTS[1] = unit_a
        U32_COMPONENTS[5] = power
        return unit_a
    return ORIGINAL_ADD_PART(sch, lib_id, reference, value, position, footprint)


def label_pin(sch, reference, pin, net):
    pin = str(pin)
    if reference != "U32":
        return ORIGINAL_LABEL_PIN(sch, reference, pin, net)
    if pin in {"1", "2", "3"}:
        component = U32_COMPONENTS[1]
    elif pin in {"4", "11"}:
        component = U32_COMPONENTS[5]
    else:
        # The base generator terminated B/C/D as spares. Those physical units now
        # belong to sheet 07, so the old spare labels are intentionally omitted.
        return None
    point = component.get_pin_position(pin)
    if point is None:
        raise RuntimeError(f"Missing U32 unit {component._data.unit} pin {pin}")
    sch.add_label(net, position=(point.x, point.y))
    return None


def repair_native_file() -> None:
    path = base.SHEET_FILE
    text = path.read_text(encoding="utf-8")
    for name in base.HIER_OUTPUTS:
        text = support.repair_hierarchical_output(text, name)
    text = support.repair_hierarchical_shape(
        text, "CTRL_I2C_SDA", "input", "bidirectional"
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    base.append_symbols = append_symbols
    base.add_part = add_part
    base.label_pin = label_pin
    base.build()
    repair_native_file()
    print("Sheet 03 regenerated with shared U32 units 1/5 and corrected hierarchy labels")
    print("U32 units 2/3/4 remain available for sheet 07")


if __name__ == "__main__":
    main()
