#!/usr/bin/env python3
"""Corrected hierarchy generator wrapper for Memory Core Prototype A.

This keeps the accepted V5.2 hierarchy definition in the original generator,
while correcting two findings from the first native KiCad 10 ERC run:

1. KiCad's left-edge sheet-pin offset is measured upward from the lower edge.
2. WATCHDOG_HEARTBEAT must enter the power/protection sheet.

The wrapper can be removed once the hierarchy is promoted into the committed
native schematic and the base generator is consolidated.
"""

from __future__ import annotations

from dataclasses import replace

from tools import generate_memory_core_hierarchy as base


def corrected_pin_position(
    sheet_position: tuple[float, float],
    sheet_size: tuple[float, float],
    side: str,
    offset: float,
) -> tuple[float, float]:
    """Return the actual native KiCad sheet-pin coordinate."""

    x, y = sheet_position
    width, height = sheet_size

    if side == "left":
        # kicad-sch-api places left pins from the lower edge upward.
        return (x, y + height - offset)
    if side == "right":
        return (x + width, y + offset)
    if side == "top":
        return (x + offset, y)
    return (x + offset, y + height)


def corrected_sheets() -> tuple[base.SheetDefinition, ...]:
    sheets = list(base.SHEETS)
    power = sheets[0]

    if not any(pin.name == "WATCHDOG_HEARTBEAT" for pin in power.pins):
        sheets[0] = replace(
            power,
            pins=power.pins
            + (base.InterfacePin("WATCHDOG_HEARTBEAT", "input"),),
        )

    return tuple(sheets)


def main() -> None:
    base.pin_position = corrected_pin_position
    base.SHEETS = corrected_sheets()
    base.build()


if __name__ == "__main__":
    main()
