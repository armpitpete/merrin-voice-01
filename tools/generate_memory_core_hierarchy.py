#!/usr/bin/env python3
"""Generate the first native KiCad hierarchy for Memory Core Prototype A.

This generator intentionally creates the hierarchy-and-interface capture only.
Each child sheet contains a non-BOM/non-board interface harness so KiCad ERC can
validate hierarchical labels and top-level connectivity before detailed circuit
capture begins.

The harness symbols are temporary schematic scaffolding. They are not physical
connectors and must be removed as actual sheet circuitry is captured.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import kicad_sch_api as ksa
from kicad_sch_api.core.types import HierarchicalLabelShape

PROJECT = "MerrinGriefSynthMemoryCoreA"
OUTPUT_DIR = Path("hardware/memory-core-prototype-a")
TOP_FILE = OUTPUT_DIR / f"{PROJECT}.kicad_sch"

Direction = Literal["input", "output", "bidirectional", "passive"]


@dataclass(frozen=True)
class InterfacePin:
    name: str
    direction: Direction


@dataclass(frozen=True)
class SheetDefinition:
    code: str
    title: str
    filename: str
    pins: tuple[InterfacePin, ...]


SHEETS: tuple[SheetDefinition, ...] = (
    SheetDefinition(
        "01",
        "POWER / PROTECTION",
        "01_POWER_PROTECTION.kicad_sch",
        (
            InterfacePin("RAIL_P12", "output"),
            InterfacePin("RAIL_N12", "output"),
            InterfacePin("RAIL_3V3", "output"),
            InterfacePin("RAIL_5V_CODEC", "output"),
            InterfacePin("HARDWARE_FAULT_N", "output"),
        ),
    ),
    SheetDefinition(
        "02",
        "MCU / CLOCK / DEBUG",
        "02_MCU_CLOCK_DEBUG.kicad_sch",
        (
            InterfacePin("RAIL_3V3", "input"),
            InterfacePin("HARDWARE_FAULT_N", "input"),
            InterfacePin("CODEC_DOUT", "input"),
            InterfacePin("CTRL_I2C_SDA", "bidirectional"),
            InterfacePin("CODEC_MCLK", "output"),
            InterfacePin("CODEC_BCLK", "output"),
            InterfacePin("CODEC_LRCLK", "output"),
            InterfacePin("CODEC_DIN", "output"),
            InterfacePin("CTRL_I2C_SCL", "output"),
            InterfacePin("CODEC_RESET_N", "output"),
            InterfacePin("CODEC_MUTE_N", "output"),
            InterfacePin("SAFE_CONTROL_RELEASE", "output"),
            InterfacePin("WATCHDOG_HEARTBEAT", "output"),
            InterfacePin("STATE_LED_R", "output"),
            InterfacePin("STATE_LED_G", "output"),
            InterfacePin("STATE_LED_B", "output"),
            InterfacePin("STATE_LED_AUX", "output"),
        ),
    ),
    SheetDefinition(
        "03",
        "CODEC / CONVERSION",
        "03_CODEC_CONVERSION.kicad_sch",
        (
            InterfacePin("RAIL_3V3", "input"),
            InterfacePin("RAIL_5V_CODEC", "input"),
            InterfacePin("CODEC_MCLK", "input"),
            InterfacePin("CODEC_BCLK", "input"),
            InterfacePin("CODEC_LRCLK", "input"),
            InterfacePin("CODEC_DIN", "input"),
            InterfacePin("CTRL_I2C_SCL", "input"),
            InterfacePin("CTRL_I2C_SDA", "bidirectional"),
            InterfacePin("CODEC_RESET_N", "input"),
            InterfacePin("CODEC_MUTE_N", "input"),
            InterfacePin("ADC_ANALOG_IN", "input"),
            InterfacePin("CODEC_DOUT", "output"),
            InterfacePin("MEMORY_DAC", "output"),
            InterfacePin("GHOST_DAC", "output"),
            InterfacePin("RETURN_DAC", "output"),
        ),
    ),
    SheetDefinition(
        "04",
        "INPUT / PRESSURE / ABSENCE",
        "04_INPUT_PRESSURE_ABSENCE.kicad_sch",
        (
            InterfacePin("RAIL_P12", "input"),
            InterfacePin("RAIL_N12", "input"),
            InterfacePin("RETURN_FEED", "input"),
            InterfacePin("ABSENCE_INFLUENCE", "input"),
            InterfacePin("DIRECT_PRESENT", "output"),
            InterfacePin("SHAPED_PRESENT", "output"),
            InterfacePin("ADC_ANALOG_IN", "output"),
        ),
    ),
    SheetDefinition(
        "05",
        "MEMORY / GHOST / WET",
        "05_MEMORY_GHOST_WET.kicad_sch",
        (
            InterfacePin("RAIL_P12", "input"),
            InterfacePin("RAIL_N12", "input"),
            InterfacePin("MEMORY_DAC", "input"),
            InterfacePin("GHOST_DAC", "input"),
            InterfacePin("VCA_MEMORY_CTRL", "input"),
            InterfacePin("VCA_GHOST_CTRL", "input"),
            InterfacePin("VCA_WET_CTRL", "input"),
            InterfacePin("WET_MIX", "output"),
        ),
    ),
    SheetDefinition(
        "06",
        "RETURN / BREAK / LIMITER",
        "06_RETURN_BREAK_LIMITER.kicad_sch",
        (
            InterfacePin("RAIL_P12", "input"),
            InterfacePin("RAIL_N12", "input"),
            InterfacePin("RETURN_DAC", "input"),
            InterfacePin("VCA_RETURN_CTRL", "input"),
            InterfacePin("RETURN_LIMITED", "output"),
            InterfacePin("RETURN_FEED", "output"),
            InterfacePin("ABSENCE_INFLUENCE", "output"),
        ),
    ),
    SheetDefinition(
        "07",
        "OUTPUT / MUTE / PROTECTION",
        "07_OUTPUT_MUTE_PROTECTION.kicad_sch",
        (
            InterfacePin("RAIL_P12", "input"),
            InterfacePin("RAIL_N12", "input"),
            InterfacePin("DIRECT_PRESENT", "input"),
            InterfacePin("WET_MIX", "input"),
            InterfacePin("HARDWARE_FAULT_N", "input"),
        ),
    ),
    SheetDefinition(
        "08",
        "CONTROLS / STATE / SAFE SELECTOR",
        "08_CONTROLS_STATE.kicad_sch",
        (
            InterfacePin("RAIL_3V3", "input"),
            InterfacePin("CTRL_I2C_SCL", "input"),
            InterfacePin("CTRL_I2C_SDA", "bidirectional"),
            InterfacePin("SAFE_CONTROL_RELEASE", "input"),
            InterfacePin("HARDWARE_FAULT_N", "input"),
            InterfacePin("STATE_LED_R", "input"),
            InterfacePin("STATE_LED_G", "input"),
            InterfacePin("STATE_LED_B", "input"),
            InterfacePin("STATE_LED_AUX", "input"),
            InterfacePin("VCA_MEMORY_CTRL", "output"),
            InterfacePin("VCA_GHOST_CTRL", "output"),
            InterfacePin("VCA_RETURN_CTRL", "output"),
            InterfacePin("VCA_WET_CTRL", "output"),
        ),
    ),
    SheetDefinition(
        "09",
        "TEST / SERVICE",
        "09_TEST_SERVICE.kicad_sch",
        (
            InterfacePin("RAIL_3V3", "input"),
            InterfacePin("HARDWARE_FAULT_N", "input"),
            InterfacePin("SHAPED_PRESENT", "input"),
            InterfacePin("ADC_ANALOG_IN", "input"),
            InterfacePin("RETURN_LIMITED", "input"),
            InterfacePin("RETURN_FEED", "input"),
            InterfacePin("ABSENCE_INFLUENCE", "input"),
            InterfacePin("WET_MIX", "input"),
        ),
    ),
)


SHAPE = {
    "input": HierarchicalLabelShape.INPUT,
    "output": HierarchicalLabelShape.OUTPUT,
    "bidirectional": HierarchicalLabelShape.BIDIRECTIONAL,
    "passive": HierarchicalLabelShape.PASSIVE,
}

# A3 positions in millimetres, all aligned to KiCad's 1.27 mm grid.
POSITIONS = (
    (20.32, 20.32),
    (152.40, 20.32),
    (284.48, 20.32),
    (20.32, 101.60),
    (152.40, 101.60),
    (284.48, 101.60),
    (20.32, 182.88),
    (152.40, 182.88),
    (284.48, 182.88),
)
SHEET_SIZE = (106.68, 55.88)


def pin_side(direction: Direction) -> str:
    if direction == "output":
        return "right"
    return "left"


def pin_position(
    sheet_position: tuple[float, float],
    sheet_size: tuple[float, float],
    side: str,
    offset: float,
) -> tuple[float, float]:
    x, y = sheet_position
    width, height = sheet_size
    if side == "left":
        return (x, y + offset)
    if side == "right":
        return (x + width, y + offset)
    if side == "top":
        return (x + offset, y)
    return (x + offset, y + height)


def connector_symbol(pin_count: int) -> str:
    return f"Connector_Generic:Conn_01x{pin_count:02d}"


def build_child(
    parent_uuid: str,
    sheet_uuid: str,
    definition: SheetDefinition,
    index: int,
) -> None:
    child = ksa.create_schematic(PROJECT)
    child.set_hierarchy_context(parent_uuid, sheet_uuid)
    child.set_paper_size("A4")
    child.set_title_block(
        title=f"Memory Core Prototype A — {definition.title}",
        rev="V5.2 hierarchy capture",
        company="MerrinLab",
        comments={1: "Interface harness is temporary and excluded from BOM/board."},
    )

    child.add_text(
        f"{definition.code} — {definition.title}",
        position=(38.10, 25.40),
        size=2.54,
    )
    child.add_text(
        "HIERARCHY / INTERFACE CAPTURE ONLY — CIRCUIT CONTENT NOT YET ACCEPTED",
        position=(38.10, 33.02),
        size=1.27,
    )

    reference = f"J9{index:02d}"
    harness = child.components.add(
        connector_symbol(len(definition.pins)),
        reference,
        "SHEET_INTERFACE_NOT_FITTED",
        position=(170.18, 101.60),
    )
    harness.in_bom = False
    harness.on_board = False
    harness.footprint = ""
    harness.add_property("Purpose", "Temporary hierarchy/ERC harness", hidden=True)

    for number, interface in enumerate(definition.pins, start=1):
        pin = child.get_component_pin_position(reference, str(number))
        if pin is None:
            raise RuntimeError(
                f"Could not resolve pin {number} on {reference} for {definition.filename}"
            )
        label_position = (pin.x - 20.32, pin.y)
        child.add_wire(start=(pin.x, pin.y), end=label_position)
        child.add_hierarchical_label(
            text=interface.name,
            position=label_position,
            shape=SHAPE[interface.direction],
            rotation=0,
            size=1.27,
        )

    child.add_rectangle(start=(33.02, 20.32), end=(271.78, 187.96))
    child.save(str(OUTPUT_DIR / definition.filename))


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    main = ksa.create_schematic(PROJECT)
    main.set_paper_size("A3")
    main.set_title_block(
        title="Merrin Grief Synth — Memory Core Prototype A",
        rev="V5.2 native hierarchy capture",
        company="MerrinLab",
        comments={
            1: "Browser voice is the reference; circuit-board synth is the destination.",
            2: "PCB placement, routing, fabrication and purchasing remain blocked.",
        },
    )
    main.add_text(
        "MEMORY CORE PROTOTYPE A — NATIVE HIERARCHICAL SCHEMATIC",
        position=(20.32, 10.16),
        size=2.54,
    )
    main.add_text(
        "Hierarchy/interface capture. Detailed circuits replace temporary harnesses sheet by sheet.",
        position=(20.32, 15.24),
        size=1.27,
    )

    parent_uuid = main.uuid
    sheet_records: list[tuple[SheetDefinition, str]] = []

    for definition, position in zip(SHEETS, POSITIONS, strict=True):
        sheet_uuid = main.sheets.add_sheet(
            name=f"{definition.code} {definition.title}",
            filename=definition.filename,
            position=position,
            size=SHEET_SIZE,
            project_name=PROJECT,
        )

        left_offset = 5.08
        right_offset = 5.08
        for interface in definition.pins:
            side = pin_side(interface.direction)
            if side == "left":
                offset = left_offset
                left_offset += 2.54
            else:
                offset = right_offset
                right_offset += 2.54

            main.sheets.add_sheet_pin(
                sheet_uuid,
                interface.name,
                interface.direction,
                side,
                offset,
            )

            # A same-name local label on every sheet pin creates the top-level net.
            label_at = pin_position(position, SHEET_SIZE, side, offset)
            main.add_label(interface.name, position=label_at)

        sheet_records.append((definition, sheet_uuid))

    main.save(str(TOP_FILE))

    for index, (definition, sheet_uuid) in enumerate(sheet_records, start=1):
        build_child(parent_uuid, sheet_uuid, definition, index)

    return_definition = next(sheet for sheet in SHEETS if sheet.code == "06")
    return_exports = {
        pin.name for pin in return_definition.pins if pin.direction == "output"
    }
    allowed_return_exports = {
        "RETURN_LIMITED",
        "RETURN_FEED",
        "ABSENCE_INFLUENCE",
    }
    if return_exports != allowed_return_exports:
        raise RuntimeError(
            "Return sheet export boundary changed: "
            f"expected {sorted(allowed_return_exports)}, got {sorted(return_exports)}"
        )

    manifest = {
        "project": PROJECT,
        "stage": "hierarchy-and-interface-capture",
        "temporary_interface_harnesses": True,
        "top_schematic": TOP_FILE.name,
        "return_sheet_allowed_outputs": sorted(allowed_return_exports),
        "sheets": [
            {
                "code": sheet.code,
                "title": sheet.title,
                "filename": sheet.filename,
                "pins": [
                    {"name": pin.name, "direction": pin.direction}
                    for pin in sheet.pins
                ],
            }
            for sheet in SHEETS
        ],
        "blocked": [
            "PCB placement",
            "PCB routing",
            "fabrication outputs",
            "purchasing",
            "oscillator expansion",
            "MIDI/CV expansion",
            "demo media",
        ],
    }
    (OUTPUT_DIR / "hierarchy-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    # A minimal project file lets KiCad open the schematic as a project while
    # keeping project preferences at defaults.
    (OUTPUT_DIR / f"{PROJECT}.kicad_pro").write_text("{}\n", encoding="utf-8")

    print(f"Generated {TOP_FILE}")
    for definition in SHEETS:
        print(f"Generated {OUTPUT_DIR / definition.filename}")


if __name__ == "__main__":
    build()
