#!/usr/bin/env python3
"""Capture the first component-level native sheet for Prototype A.

The script replaces the temporary 01_POWER_PROTECTION interface harness with
an actual power, reset and independent watchdog circuit. It also emits a small
project-local symbol library for the selected TI devices because those exact
parts are not present in KiCad's stock symbol libraries.

Active-device footprints remain deliberately blank. Pin maps are verified for
schematic capture; footprints remain blocked until independent review.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import kicad_sch_api as ksa
from kicad_sch_api.core.types import HierarchicalLabelShape

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP = ROOT / f"{PROJECT}.kicad_sch"
POWER_SHEET = ROOT / "01_POWER_PROTECTION.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
SYMBOL_TABLE = ROOT / "sym-lib-table"
MARKER = ROOT / "01_POWER_PROTECTION_CAPTURED"

PinType = Literal[
    "input",
    "output",
    "bidirectional",
    "tri_state",
    "passive",
    "power_in",
    "power_out",
    "open_collector",
    "no_connect",
]
Side = Literal["left", "right"]


@dataclass(frozen=True)
class SymbolPin:
    number: str
    name: str
    pin_type: PinType
    side: Side
    row: int


@dataclass(frozen=True)
class SymbolDefinition:
    name: str
    description: str
    datasheet: str
    pins: tuple[SymbolPin, ...]


SYMBOLS = (
    SymbolDefinition(
        "TPS62160DGK",
        "1 A adjustable synchronous step-down converter, VSSOP-8 verified pin map",
        "https://www.ti.com/lit/ds/symlink/tps62160.pdf",
        (
            SymbolPin("2", "VIN", "power_in", "left", 1),
            SymbolPin("3", "EN", "input", "left", 2),
            SymbolPin("5", "FB", "input", "left", 3),
            SymbolPin("6", "VOS", "input", "left", 4),
            SymbolPin("1", "PGND", "power_in", "left", 5),
            SymbolPin("4", "AGND", "power_in", "left", 6),
            SymbolPin("8", "PG", "open_collector", "right", 1),
            SymbolPin("7", "SW", "power_out", "right", 3),
        ),
    ),
    SymbolDefinition(
        "TPS7A2050PDBV",
        "300 mA low-noise 5 V LDO, SOT-23-5 verified pin map",
        "https://www.ti.com/lit/ds/symlink/tps7a20.pdf",
        (
            SymbolPin("1", "IN", "power_in", "left", 1),
            SymbolPin("3", "EN", "input", "left", 2),
            SymbolPin("2", "GND", "power_in", "left", 4),
            SymbolPin("5", "OUT", "power_out", "right", 1),
            SymbolPin("4", "NC", "no_connect", "right", 4),
        ),
    ),
    SymbolDefinition(
        "TPS3808G33DBV",
        "3.3 V supervisor with programmable delay, SOT-23-6 verified pin map",
        "https://www.ti.com/lit/ds/symlink/tps3808.pdf",
        (
            SymbolPin("6", "VDD", "power_in", "left", 1),
            SymbolPin("5", "SENSE", "input", "left", 2),
            SymbolPin("3", "MR_N", "input", "left", 3),
            SymbolPin("4", "CT", "passive", "left", 4),
            SymbolPin("2", "GND", "power_in", "left", 5),
            SymbolPin("1", "RESET_N", "open_collector", "right", 2),
        ),
    ),
    SymbolDefinition(
        "TPS3431DRB",
        "Independent programmable watchdog, VSON-8 plus exposed pad verified pin map",
        "https://www.ti.com/lit/ds/symlink/tps3431.pdf",
        (
            SymbolPin("1", "VDD", "power_in", "left", 1),
            SymbolPin("2", "CWD", "passive", "left", 2),
            SymbolPin("3", "EN", "input", "left", 3),
            SymbolPin("4", "GND", "power_in", "left", 4),
            SymbolPin("9", "EP", "power_in", "left", 5),
            SymbolPin("5", "SET1", "input", "right", 1),
            SymbolPin("6", "WDI", "input", "right", 2),
            SymbolPin("7", "WDO_N", "open_collector", "right", 3),
            SymbolPin("8", "ENOUT_N", "open_collector", "right", 4),
        ),
    ),
)


def effects(hidden: bool = False) -> str:
    hide = " hide" if hidden else ""
    return (
        "\t\t\t(effects\n"
        "\t\t\t\t(font\n"
        "\t\t\t\t\t(size 1.27 1.27)\n"
        "\t\t\t\t)"
        f"{hide}\n"
        "\t\t\t)\n"
    )


def property_block(name: str, value: str, y: float, hidden: bool = False) -> str:
    return (
        f'\t\t(property "{name}" "{value}"\n'
        f"\t\t\t(at 0 {y} 0)\n"
        f"{effects(hidden)}"
        "\t\t)\n"
    )


def render_symbol(definition: SymbolDefinition) -> str:
    rows = max(pin.row for pin in definition.pins)
    half_height = max(7.62, rows * 1.27 + 1.27)
    left_x = -10.16
    right_x = 10.16
    pin_length = 3.81

    out = [
        f'\t(symbol "{definition.name}"\n',
        "\t\t(exclude_from_sim no)\n",
        "\t\t(in_bom yes)\n",
        "\t\t(on_board yes)\n",
        property_block("Reference", "U", half_height + 2.54),
        property_block("Value", definition.name, -(half_height + 2.54)),
        property_block("Footprint", "", 0, True),
        property_block("Datasheet", definition.datasheet, 0, True),
        property_block("Description", definition.description, 0, True),
        f'\t\t(symbol "{definition.name}_1_1"\n',
        "\t\t\t(rectangle\n",
        f"\t\t\t\t(start -6.35 {half_height})\n",
        f"\t\t\t\t(end 6.35 {-half_height})\n",
        "\t\t\t\t(stroke (width 0.254) (type default))\n",
        "\t\t\t\t(fill (type background))\n",
        "\t\t\t)\n",
    ]

    for pin in definition.pins:
        y = half_height - 2.54 * pin.row
        x = left_x if pin.side == "left" else right_x
        rotation = 0 if pin.side == "left" else 180
        out.extend(
            [
                f"\t\t\t(pin {pin.pin_type} line\n",
                f"\t\t\t\t(at {x} {y} {rotation})\n",
                f"\t\t\t\t(length {pin_length})\n",
                f'\t\t\t\t(name "{pin.name}"\n',
                "\t\t\t\t\t(effects (font (size 0.762 0.762)))\n",
                "\t\t\t\t)\n",
                f'\t\t\t\t(number "{pin.number}"\n',
                "\t\t\t\t\t(effects (font (size 1.016 1.016)))\n",
                "\t\t\t\t)\n",
                "\t\t\t)\n",
            ]
        )

    out.extend(["\t\t)\n", "\t)\n"])
    return "".join(out)


def write_symbol_library() -> None:
    content = [
        "(kicad_symbol_lib\n",
        "\t(version 20241209)\n",
        '\t(generator "capture_power_protection_sheet.py")\n',
        '\t(generator_version "1.0")\n',
    ]
    content.extend(render_symbol(symbol) for symbol in SYMBOLS)
    content.append(")\n")
    SYMBOL_LIBRARY.write_text("".join(content), encoding="utf-8")

    SYMBOL_TABLE.write_text(
        "(sym_lib_table\n"
        "  (version 7)\n"
        "  (lib (name \"MerrinLab_PrototypeA\")"
        " (type \"KiCad\")"
        " (uri \"${KIPRJMOD}/MerrinLab_PrototypeA.kicad_sym\")"
        " (options \"\")"
        " (descr \"Verified Prototype A schematic symbols; footprints pending\"))\n"
        ")\n",
        encoding="utf-8",
    )


def find_power_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == POWER_SHEET.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("01_POWER_PROTECTION sheet was not found in the top schematic")


def add_part(
    sch: ksa.Schematic,
    lib_id: str,
    reference: str,
    value: str,
    position: tuple[float, float],
    footprint: str = "",
):
    return sch.components.add(
        lib_id=lib_id,
        reference=reference,
        value=value,
        position=position,
        footprint=footprint,
    )


def pin_position(sch: ksa.Schematic, reference: str, pin: str) -> tuple[float, float]:
    point = sch.get_component_pin_position(reference, pin)
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def label_pin(sch: ksa.Schematic, reference: str, pin: str, net: str) -> None:
    sch.add_label(net, position=pin_position(sch, reference, pin))


def no_connect_pin(sch: ksa.Schematic, reference: str, pin: str) -> None:
    sch.no_connects.add(position=pin_position(sch, reference, pin))


def hier_net(
    sch: ksa.Schematic,
    name: str,
    position: tuple[float, float],
    shape: HierarchicalLabelShape,
    end: tuple[float, float],
) -> None:
    sch.add_hierarchical_label(name, position=position, shape=shape, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def add_two_pin(
    sch: ksa.Schematic,
    lib_id: str,
    reference: str,
    value: str,
    position: tuple[float, float],
    net_1: str,
    net_2: str,
    footprint: str = "",
) -> None:
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net_1)
    label_pin(sch, reference, "2", net_2)


def build_power_sheet() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    write_symbol_library()

    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))

    top = ksa.load_schematic(str(TOP))
    parent_uuid, sheet_uuid = find_power_sheet_context(top)

    sch = ksa.create_schematic(PROJECT)
    sch.set_hierarchy_context(parent_uuid, sheet_uuid)
    sch.set_paper_size("A3")
    sch.set_title_block(
        title="Memory Core Prototype A — Power / Protection",
        rev="V5.2 component capture 01",
        company="MerrinLab",
        comments={
            1: "Verified IC pin maps; active-device footprints remain blocked.",
            2: "PCB placement, routing, fabrication and purchasing remain forbidden.",
        },
    )

    sch.add_text("01 — POWER / PROTECTION", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "PROTECTED ±12 V • 3.3 V DIGITAL • 5.453 V PRE-RAIL • QUIET 5 V • HARDWARE FAULT",
        position=(20.32, 17.78),
        size=1.27,
    )
    sch.add_text(
        "Active-device footprints intentionally blank pending independent footprint review.",
        position=(20.32, 22.86),
        size=1.27,
    )

    # Hierarchical interfaces.
    hier_net(sch, "WATCHDOG_HEARTBEAT", (20.32, 43.18), HierarchicalLabelShape.INPUT, (35.56, 43.18))
    hier_net(sch, "RAIL_P12", (391.16, 43.18), HierarchicalLabelShape.OUTPUT, (375.92, 43.18))
    hier_net(sch, "RAIL_N12", (391.16, 50.80), HierarchicalLabelShape.OUTPUT, (375.92, 50.80))
    hier_net(sch, "RAIL_3V3", (391.16, 58.42), HierarchicalLabelShape.OUTPUT, (375.92, 58.42))
    hier_net(sch, "RAIL_5V_CODEC", (391.16, 66.04), HierarchicalLabelShape.OUTPUT, (375.92, 66.04))
    hier_net(sch, "HARDWARE_FAULT_N", (391.16, 73.66), HierarchicalLabelShape.OUTPUT, (375.92, 73.66))

    # Power entry. Final connector/footprint remains open.
    add_part(sch, "Connector_Generic:Conn_01x03", "J1", "PROTECTED ±12 V INPUT", (35.56, 91.44))
    label_pin(sch, "J1", "1", "RAW_P12")
    label_pin(sch, "J1", "2", "GND")
    label_pin(sch, "J1", "3", "RAW_N12")

    for reference, net, position in (
        ("#FLG01", "RAW_P12", (20.32, 83.82)),
        ("#FLG02", "RAW_N12", (20.32, 91.44)),
        ("#FLG03", "GND", (20.32, 99.06)),
    ):
        add_part(sch, "power:PWR_FLAG", reference, "PWR_FLAG", position)
        label_pin(sch, reference, "1", net)

    add_two_pin(sch, "Device:Polyfuse", "F1", "750mA hold — provisional", (58.42, 83.82), "RAW_P12", "P12_FUSED")
    add_two_pin(sch, "Device:D_Schottky", "D1", "SS34 — provisional", (76.20, 83.82), "P12_PROTECTED_DIODE", "P12_FUSED")
    add_two_pin(sch, "Device:Ferrite_Bead", "FB1", "≥1A low-DCR", (93.98, 83.82), "P12_PROTECTED_DIODE", "RAIL_P12")

    add_two_pin(sch, "Device:Polyfuse", "F2", "250mA hold — provisional", (58.42, 99.06), "RAW_N12", "N12_FUSED")
    add_two_pin(sch, "Device:D_Schottky", "D2", "SS34 — provisional", (76.20, 99.06), "N12_FUSED", "N12_PROTECTED_DIODE")
    add_two_pin(sch, "Device:Ferrite_Bead", "FB2", "≥0.5A low-DCR", (93.98, 99.06), "N12_PROTECTED_DIODE", "RAIL_N12")

    add_two_pin(sch, "Device:C_Polarized", "C1", "47µF 25V", (111.76, 83.82), "RAIL_P12", "GND", "Capacitor_SMD:C_1210_3225Metric")
    add_two_pin(sch, "Device:C", "C2", "100nF 50V", (124.46, 83.82), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C_Polarized", "C3", "47µF 25V", (111.76, 99.06), "GND", "RAIL_N12", "Capacitor_SMD:C_1210_3225Metric")
    add_two_pin(sch, "Device:C", "C4", "100nF 50V", (124.46, 99.06), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U1 — 3.3 V buck.
    add_part(sch, "MerrinLab_PrototypeA:TPS62160DGK", "U1", "TPS62160 — 3.3V", (177.80, 73.66))
    for pin, net in {
        "2": "RAIL_P12",
        "3": "RAIL_P12",
        "1": "GND",
        "4": "GND",
        "7": "BUCK3V3_SW",
        "8": "HARDWARE_FAULT_N",
        "6": "RAIL_3V3",
        "5": "BUCK3V3_FB",
    }.items():
        label_pin(sch, "U1", pin, net)

    add_two_pin(sch, "Device:L", "L1", "2.2µH; Isat ≥1.3A", (205.74, 73.66), "BUCK3V3_SW", "RAIL_3V3")
    add_two_pin(sch, "Device:R", "R1", "374k 1%", (205.74, 83.82), "RAIL_3V3", "BUCK3V3_FB", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R2", "120k 1%", (205.74, 91.44), "BUCK3V3_FB", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C5", "10µF 25V X7R", (154.94, 73.66), "RAIL_P12", "GND", "Capacitor_SMD:C_1206_3216Metric")
    add_two_pin(sch, "Device:C", "C6", "22µF 10V X7R", (223.52, 73.66), "RAIL_3V3", "GND", "Capacitor_SMD:C_1206_3216Metric")
    add_two_pin(sch, "Device:C", "C7", "22µF 10V X7R", (236.22, 73.66), "RAIL_3V3", "GND", "Capacitor_SMD:C_1206_3216Metric")

    # U2 — 5.453 V pre-regulator.
    add_part(sch, "MerrinLab_PrototypeA:TPS62160DGK", "U2", "TPS62160 — 5.453V PRE", (177.80, 124.46))
    for pin, net in {
        "2": "RAIL_P12",
        "3": "RAIL_P12",
        "1": "GND",
        "4": "GND",
        "7": "BUCK5V45_SW",
        "8": "HARDWARE_FAULT_N",
        "6": "RAIL_5V45_PRE",
        "5": "BUCK5V45_FB",
    }.items():
        label_pin(sch, "U2", pin, net)

    add_two_pin(sch, "Device:L", "L2", "3.3µH; Isat ≥1.3A", (205.74, 124.46), "BUCK5V45_SW", "RAIL_5V45_PRE")
    add_two_pin(sch, "Device:R", "R3", "698k 1%", (205.74, 134.62), "RAIL_5V45_PRE", "BUCK5V45_FB", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R4", "120k 1%", (205.74, 142.24), "BUCK5V45_FB", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C8", "10µF 25V X7R", (154.94, 124.46), "RAIL_P12", "GND", "Capacitor_SMD:C_1206_3216Metric")
    add_two_pin(sch, "Device:C", "C9", "22µF 10V X7R", (223.52, 124.46), "RAIL_5V45_PRE", "GND", "Capacitor_SMD:C_1206_3216Metric")
    add_two_pin(sch, "Device:C", "C10", "22µF 10V X7R", (236.22, 124.46), "RAIL_5V45_PRE", "GND", "Capacitor_SMD:C_1206_3216Metric")

    # U3 — quiet 5 V LDO. EN follows the valid pre-rail directly; U2 PG remains on the hardware fault net.
    add_part(sch, "MerrinLab_PrototypeA:TPS7A2050PDBV", "U3", "TPS7A2050 — QUIET 5V", (284.48, 124.46))
    for pin, net in {"1": "RAIL_5V45_PRE", "3": "RAIL_5V45_PRE", "2": "GND", "5": "RAIL_5V_CODEC"}.items():
        label_pin(sch, "U3", pin, net)
    no_connect_pin(sch, "U3", "4")
    add_two_pin(sch, "Device:C", "C11", "2.2µF 10V X7R", (266.70, 124.46), "RAIL_5V45_PRE", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C12", "4.7µF 10V X7R", (304.80, 124.46), "RAIL_5V_CODEC", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U4 — 3.3 V supervisor and manual reset.
    add_part(sch, "MerrinLab_PrototypeA:TPS3808G33DBV", "U4", "TPS3808G33", (284.48, 73.66))
    for pin, net in {"6": "RAIL_3V3", "5": "RAIL_3V3", "2": "GND", "1": "HARDWARE_FAULT_N", "3": "MANUAL_RESET_N", "4": "SUPERVISOR_CT"}.items():
        label_pin(sch, "U4", pin, net)
    add_two_pin(sch, "Device:R", "R5", "50k 1% — 300ms nominal", (266.70, 83.82), "RAIL_3V3", "SUPERVISOR_CT", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R6", "10k", (266.70, 91.44), "RAIL_3V3", "MANUAL_RESET_N", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Switch:SW_Push", "SW1", "RESET / CLEAR", (284.48, 91.44), "MANUAL_RESET_N", "GND")
    add_two_pin(sch, "Device:C", "C13", "100nF", (304.80, 73.66), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U5 — independent watchdog.
    add_part(sch, "MerrinLab_PrototypeA:TPS3431DRB", "U5", "TPS3431 — 200ms watchdog", (335.28, 91.44))
    for pin, net in {
        "1": "RAIL_3V3",
        "2": "WATCHDOG_CWD",
        "3": "WATCHDOG_EN",
        "4": "GND",
        "9": "GND",
        "5": "WATCHDOG_SET1",
        "6": "WATCHDOG_HEARTBEAT",
        "7": "HARDWARE_FAULT_N",
    }.items():
        label_pin(sch, "U5", pin, net)
    no_connect_pin(sch, "U5", "8")
    add_two_pin(sch, "Device:R", "R7", "10k — CWD", (317.50, 106.68), "RAIL_3V3", "WATCHDOG_CWD", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R8", "100k — EN high", (330.20, 106.68), "RAIL_3V3", "WATCHDOG_EN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R9", "10k — SET1 high", (342.90, 106.68), "RAIL_3V3", "WATCHDOG_SET1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C14", "100nF", (355.60, 106.68), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Shared active-low hardware fault pull-up. Any open-drain device can assert it.
    add_two_pin(sch, "Device:R", "R10", "10k fault pull-up", (355.60, 73.66), "RAIL_3V3", "HARDWARE_FAULT_N", "Resistor_SMD:R_0805_2012Metric")

    # Test points required by the accepted bring-up contract.
    test_points = (
        ("TP1", "P12_PROTECTED", "RAIL_P12", (137.16, 83.82)),
        ("TP2", "N12_PROTECTED", "RAIL_N12", (137.16, 99.06)),
        ("TP3", "DIGITAL_3V3", "RAIL_3V3", (248.92, 73.66)),
        ("TP4", "PRE_5V453", "RAIL_5V45_PRE", (248.92, 124.46)),
        ("TP5", "QUIET_5V", "RAIL_5V_CODEC", (320.04, 124.46)),
        ("TP6", "FAULT_N", "HARDWARE_FAULT_N", (375.92, 83.82)),
        ("TP7", "WDI", "WATCHDOG_HEARTBEAT", (317.50, 83.82)),
        ("TP8", "WDO_N", "HARDWARE_FAULT_N", (355.60, 83.82)),
    )
    for reference, value, net, position in test_points:
        add_part(sch, "Connector:TestPoint", reference, value, position)
        label_pin(sch, reference, "1", net)

    sch.add_text(
        "FAULT_N wired-AND sources: U1 PG, U2 PG, U4 RESET_N, U5 WDO_N.\n"
        "Fault release requires all sources high; no firmware path can force a held-low net high.",
        position=(251.46, 157.48),
        size=1.27,
    )
    sch.add_text(
        "Provisional power-entry fuses, Schottky diodes, ferrite beads and connector remain subject to exact part selection.\n"
        "The topology is captured; footprints and physical power format remain blocked.",
        position=(20.32, 157.48),
        size=1.27,
    )

    sch.save(str(POWER_SHEET))
    MARKER.write_text(
        "01_POWER_PROTECTION component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )

    print(f"Captured {POWER_SHEET}")
    print(f"Generated {SYMBOL_LIBRARY}")
    print(f"Generated {SYMBOL_TABLE}")


if __name__ == "__main__":
    build_power_sheet()
