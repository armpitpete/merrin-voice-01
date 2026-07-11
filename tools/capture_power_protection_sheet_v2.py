#!/usr/bin/env python3
"""Current entrypoint for 01_POWER_PROTECTION native capture.

The implementation lives in `capture_power_protection_sheet_v3.py`, which
includes the stock-symbol correction plus the first KiCad 10 ERC repairs.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


IMPLEMENTATION = Path(__file__).with_name("capture_power_protection_sheet_v3.py")
SPEC = importlib.util.spec_from_file_location("power_protection_capture_current", IMPLEMENTATION)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load current capture implementation: {IMPLEMENTATION}")

module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


if __name__ == "__main__":
    module.main()
