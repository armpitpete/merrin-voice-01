#!/usr/bin/env python3
"""Capture 08_CONTROLS_STATE for Memory Core Prototype A.

The sheet implements:
- MCP4728 normal VCA control voltages;
- TMUX1574 four-channel fail-safe selection;
- hardware-fault clamp of selector release;
- eight panel-potentiometer ADC signals;
- RESET_CLEAR, SAFE_MUTE and SERVICE_TEST operating inputs;
- four low-current SLS-1 state-light drivers.

Footprints for active devices and panel hardware remain blank pending the
independent footprint/mechanical gate.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import kicad_sch_api as ksa
from kicad_sch_api.core.types import HierarchicalLabelShape

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP = ROOT / f"{PROJECT}.kicad_sch"
SHEET_FILE = ROOT / "08_CONTROLS_STATE.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "08_CONTROLS_STATE_CAPTURED"

POWER_CAPTURE_PATH = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_symbol_helpers", POWER_CAPTURE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_CAPTURE_PATH}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

MCP4728 = helpers.SymbolDefinition(
    "MCP4728_UN",
    "12-bit quad DAC with EEPROM; verified 10-pin MSOP pin map",
    "https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/22187E.pdf",
    (
        helpers.SymbolPin("1", "VDD", "power_in", "left", 1),
        helpers.SymbolPin("2", "SCL", "input", "left", 2),
        helpers.SymbolPin("3", "SDA", "bidirectional", "left", 3),
        helpers.SymbolPin("4", "LDAC", "input", "left", 4),
        helpers.SymbolPin("5", "RDY_BSY_N", "open_collector", "left", 5),
        helpers.SymbolPin("10", "VSS", "power_in", "left", 6),
        helpers.SymbolPin("6", "VOUT_A", "output", "right", 1),
        helpers.SymbolPin("7", "VOUT_B", "output", "right", 2),
        helpers.SymbolPin("8", "VOUT_C", "output", "right", 3),
        helpers.SymbolPin("9", "VOUT_D", "output", "right", 4),
    ),
)

TMUX1574 = helpers.SymbolDefinition(
    "TMUX1574PW",
    "Four-channel 2:1 fail-safe analogue switch; verified TSSOP-16 pin map",
    "https://www.ti.com/lit/ds/symlink/tmux1574.pdf",
    (
        helpers.SymbolPin("16", "VDD", "power_in", "left", 1),
        helpers.SymbolPin("15", "EN_N", "input", "left", 2),
        helpers.SymbolPin("1", "SEL", "input", "left", 3),
        helpers.SymbolPin("8", "GND", "power_in", "left", 4),
        helpers.SymbolPin("2", "S1A", "bidirectional", "left", 6),
        helpers.SymbolPin("3", "S1B", "bidirectional", "left", 7),
        helpers.SymbolPin("5", "S2A", "bidirectional", "left", 8),
        helpers.SymbolPin("6", "S2B", "bidirectional", "left", 9),
        helpers.SymbolPin("11", "S3A", "bidirectional", "left", 10),
        helpers.SymbolPin("10", "S3B", "bidirectional", "left", 11),
        helpers.SymbolPin("14", "S4A", "bidirectional", "left", 12),
        helpers.SymbolPin("13", "S4B", "bidirectional", "left", 13),
        helpers.SymbolPin("4", "D1", "bidirectional", "right", 6),
        helpers.SymbolPin("7", "D2", "bidirectional", "right", 8),
        helpers.SymbolPin("9", "D3", "bidirectional", "right", 10),
        helpers.SymbolPin("12", "D4", "bidirectional", "right", 12),
    ),
)

PANEL_CONTROLS = (
    ("RV1", "MEMORY TIME", "PANEL_MEMORY_TIME"),
    ("RV2", "MEMORY FADE", "PANEL_MEMORY_FADE"),
    ("RV3", "MEMORY BLUR", "PANEL_MEMORY_BLUR"),
    ("RV4", "GHOST DISTANCE", "PANEL_GHOST_DISTANCE"),
    ("RV5", "GHOST DRIFT", "PANEL_GHOST_DRIFT"),
    ("RV6", "GHOST PRESENCE", "PANEL_GHOST_PRESENCE"),
    ("RV7", "RETURN AMOUNT", "PANEL_RETURN_AMOUNT"),
    ("RV8", "PRESENT / WET", "PANEL_PRESENT_WET"),
)

OPERATING_INPUTS = (
    ("SW2", "SERVICE TEST", "SERVICE_TEST"),
    ("SW3", "RESET / CLEAR", "RESET_CLEAR"),
    ("SW4", "SAFE MUTE", "SAFE_MUTE"),
)

STATE_LIGHTS = (
    ("R", "STATE_LED_R", "D21", "Q1"),
    ("G", "STATE_LED_G", "D22", "Q2"),
    ("B", "STATE_LED_B", "D23", "Q3"),
    ("AUX", "STATE_LED_AUX", "D24", "Q4"),
)


def append_project_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    for definition in (MCP4728, TMUX1574):
        if f'(symbol "{definition.name}"' not in text:
            additions.append(helpers.render_symbol(definition))

    if not additions:
        return

    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end with a closing parenthesis")
    updated = stripped[:-1] + "".join(additions) + ")\n"
    SYMBOL_LIBRARY.write_text(updated, encoding="utf-8")


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("08_CONTROLS_STATE sheet not found")


def add_part(sch, lib_id, reference, value, position, footprint=""):
    return sch.components.add(
        lib_id=lib_id,
        reference=reference,
        value=value,
        position=position,
        footprint=footprint,
    )


def pin_position(sch, reference, pin):
    point = sch.get_component_pin_position(reference, pin)
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_hier(sch, name, position, shape, end):
    sch.add_hierarchical_label(name, position=position, shape=shape, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def add_upper_clamp(sch, reference, signal, position):
    # Device diode pin 1 is cathode; pin 2 is anode.
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class", position, "RAIL_3V3", signal)


def add_lower_clamp(sch, reference, signal, position):
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class", position, signal, "GND")


def build() -> None:
    append_project_symbols()
    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))

    top = ksa.load_schematic(str(TOP))
    parent_uuid, sheet_uuid = find_sheet_context(top)

    sch = ksa.create_schematic(PROJECT)
    sch.set_hierarchy_context(parent_uuid, sheet_uuid)
    sch.set_paper_size("A3")
    sch.set_title_block(
        title="Memory Core Prototype A — Controls / State / Safe Selector",
        rev="V5.2 component capture 08",
        company="MerrinLab",
        comments={
            1: "MCP4728 normal control; TMUX1574 defaults to attenuation.",
            2: "Active and panel footprints remain blocked pending review.",
        },
    )

    sch.add_text("08 — CONTROLS / STATE / SAFE SELECTOR", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "NORMAL CONTROL CANNOT OVERRIDE HARDWARE FAULT • +3.3 V = SSI2164 ATTENUATION",
        position=(20.32, 17.78),
        size=1.27,
    )

    # Hierarchical inputs.
    input_signals = (
        "RAIL_3V3",
        "CTRL_I2C_SCL",
        "CTRL_I2C_SDA",
        "SAFE_CONTROL_RELEASE",
        "HARDWARE_FAULT_N",
        "STATE_LED_R",
        "STATE_LED_G",
        "STATE_LED_B",
        "STATE_LED_AUX",
    )
    y = 35.56
    for signal in input_signals:
        shape = HierarchicalLabelShape.BIDIRECTIONAL if signal == "CTRL_I2C_SDA" else HierarchicalLabelShape.INPUT
        add_hier(sch, signal, (20.32, y), shape, (35.56, y))
        y += 6.35

    # Hierarchical outputs.
    output_signals = (
        "VCA_MEMORY_CTRL",
        "VCA_GHOST_CTRL",
        "VCA_RETURN_CTRL",
        "VCA_WET_CTRL",
        *(signal for _, _, signal in PANEL_CONTROLS),
        *(signal for _, _, signal in OPERATING_INPUTS),
    )
    y = 35.56
    for signal in output_signals:
        add_hier(sch, signal, (391.16, y), HierarchicalLabelShape.OUTPUT, (375.92, y))
        y += 6.35

    # Shared I2C pull-ups.
    add_two_pin(sch, "Device:R", "R81", "4.7k", (55.88, 43.18), "RAIL_3V3", "CTRL_I2C_SCL", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R82", "4.7k", (68.58, 43.18), "RAIL_3V3", "CTRL_I2C_SDA", "Resistor_SMD:R_0805_2012Metric")

    # MCP4728 normal-operation DAC.
    add_part(sch, "MerrinLab_PrototypeA:MCP4728_UN", "U6", "MCP4728 — VCA CONTROL", (101.60, 73.66))
    for pin, net in {
        "1": "RAIL_3V3",
        "2": "CTRL_I2C_SCL",
        "3": "CTRL_I2C_SDA",
        "4": "GND",
        "5": "MCP4728_RDY_N",
        "10": "GND",
        "6": "DAC_MEMORY_CTRL",
        "7": "DAC_GHOST_CTRL",
        "8": "DAC_RETURN_CTRL",
        "9": "DAC_WET_CTRL",
    }.items():
        label_pin(sch, "U6", pin, net)

    add_two_pin(sch, "Device:R", "R83", "100k RDY pull-up", (76.20, 88.90), "RAIL_3V3", "MCP4728_RDY_N", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C81", "100nF", (76.20, 73.66), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C82", "10µF", (88.90, 73.66), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_part(sch, "Connector:TestPoint", "TP81", "MCP4728_RDY_N", (76.20, 96.52))
    label_pin(sch, "TP81", "1", "MCP4728_RDY_N")

    # TMUX1574 fail-safe selector.
    add_part(sch, "MerrinLab_PrototypeA:TMUX1574PW", "U7", "TMUX1574 — SAFE SELECTOR", (175.26, 83.82))
    for pin, net in {
        "16": "RAIL_3V3",
        "15": "GND",
        "1": "SAFE_SELECTOR_SEL",
        "8": "GND",
        "2": "RAIL_3V3",
        "3": "DAC_MEMORY_CTRL",
        "5": "RAIL_3V3",
        "6": "DAC_GHOST_CTRL",
        "11": "RAIL_3V3",
        "10": "DAC_RETURN_CTRL",
        "14": "RAIL_3V3",
        "13": "DAC_WET_CTRL",
        "4": "MUX_MEMORY_CTRL",
        "7": "MUX_GHOST_CTRL",
        "9": "MUX_RETURN_CTRL",
        "12": "MUX_WET_CTRL",
    }.items():
        label_pin(sch, "U7", pin, net)

    add_two_pin(sch, "Device:R", "R84", "100k default-safe pull-down", (139.70, 58.42), "SAFE_SELECTOR_SEL", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R85", "10k release feed", (139.70, 66.04), "SAFE_CONTROL_RELEASE", "SAFE_SELECTOR_SEL", "Resistor_SMD:R_0805_2012Metric")
    # Anode at selector, cathode at active-low fault: fault assertion clamps SEL low.
    add_two_pin(sch, "Device:D_Schottky", "D81", "BAT54-class fault clamp", (139.70, 73.66), "HARDWARE_FAULT_N", "SAFE_SELECTOR_SEL")
    add_two_pin(sch, "Device:C", "C83", "100nF", (152.40, 83.82), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_part(sch, "Connector:TestPoint", "TP82", "SAFE_SELECTOR_SEL", (152.40, 58.42))
    label_pin(sch, "TP82", "1", "SAFE_SELECTOR_SEL")

    # Four bounded VCA-control outputs.
    control_channels = (
        ("MEMORY", "MUX_MEMORY_CTRL", "VCA_MEMORY_CTRL", "R86", "C84", "D82", "D83", "TP83"),
        ("GHOST", "MUX_GHOST_CTRL", "VCA_GHOST_CTRL", "R87", "C85", "D84", "D85", "TP84"),
        ("RETURN", "MUX_RETURN_CTRL", "VCA_RETURN_CTRL", "R88", "C86", "D86", "D87", "TP85"),
        ("WET", "MUX_WET_CTRL", "VCA_WET_CTRL", "R89", "C87", "D88", "D89", "TP86"),
    )
    y = 53.34
    for name, source, output, resistor, capacitor, upper, lower, testpoint in control_channels:
        filtered = f"{name}_CTRL_FILTERED"
        add_two_pin(sch, "Device:R", resistor, "1k", (226.06, y), source, filtered, "Resistor_SMD:R_0805_2012Metric")
        add_two_pin(sch, "Device:C", capacitor, "10nF", (238.76, y), filtered, "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_upper_clamp(sch, upper, filtered, (251.46, y - 2.54))
        add_lower_clamp(sch, lower, filtered, (251.46, y + 2.54))
        add_two_pin(sch, "Device:R", f"{resistor}A", "1k output isolate", (266.70, y), filtered, output, "Resistor_SMD:R_0805_2012Metric")
        add_part(sch, "Connector:TestPoint", testpoint, output, (279.40, y))
        label_pin(sch, testpoint, "1", output)
        y += 17.78

    # Eight panel potentiometers with simple ADC filtering.
    x_positions = (45.72, 83.82, 121.92, 160.02, 198.12, 236.22, 274.32, 312.42)
    for index, ((reference, value, output), x) in enumerate(zip(PANEL_CONTROLS, x_positions, strict=True), start=1):
        add_part(sch, "Device:R_Potentiometer", reference, value, (x, 154.94))
        label_pin(sch, reference, "1", "GND")
        label_pin(sch, reference, "3", "RAIL_3V3")
        raw = f"{output}_RAW"
        label_pin(sch, reference, "2", raw)
        add_two_pin(sch, "Device:R", f"R9{index}A", "1k ADC isolate", (x, 170.18), raw, output, "Resistor_SMD:R_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C9{index}", "100nF ADC filter", (x, 180.34), output, "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Three active-low panel/service inputs.
    x_positions = (96.52, 172.72, 248.92)
    for index, ((switch, value, output), x) in enumerate(zip(OPERATING_INPUTS, x_positions, strict=True), start=1):
        raw = f"{output}_RAW_N"
        add_two_pin(sch, "Device:R", f"R10{index}", "100k pull-up", (x - 12.70, 215.90), "RAIL_3V3", raw, "Resistor_SMD:R_0805_2012Metric")
        add_two_pin(sch, "Switch:SW_Push", switch, value, (x, 215.90), raw, "GND")
        add_two_pin(sch, "Device:R", f"R11{index}", "1k isolate", (x + 15.24, 215.90), raw, output, "Resistor_SMD:R_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C10{index}", "10nF debounce/RF", (x + 27.94, 215.90), output, "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Four low-current state-light drivers.
    y = 246.38
    x = 63.50
    for index, (name, signal, led, transistor) in enumerate(STATE_LIGHTS, start=1):
        base_net = f"STATE_{name}_BASE"
        collector = f"STATE_{name}_COLLECTOR"
        add_two_pin(sch, "Device:R", f"R12{index}", "10k base", (x, y), signal, base_net, "Resistor_SMD:R_0805_2012Metric")
        add_two_pin(sch, "Device:R", f"R13{index}", "100k base pull-down", (x + 12.70, y + 7.62), base_net, "GND", "Resistor_SMD:R_0805_2012Metric")
        add_part(sch, "Transistor_BJT:Q_NPN_BCE", transistor, "NPN LED DRIVER", (x + 27.94, y))
        label_pin(sch, transistor, "1", base_net)
        label_pin(sch, transistor, "2", collector)
        label_pin(sch, transistor, "3", "GND")
        add_two_pin(sch, "Device:LED", led, f"SLS-1 {name}", (x + 43.18, y), collector, f"STATE_{name}_LED_ANODE")
        add_two_pin(sch, "Device:R", f"R14{index}", "1k LED limit", (x + 58.42, y), f"STATE_{name}_LED_ANODE", "RAIL_3V3", "Resistor_SMD:R_0805_2012Metric")
        x += 83.82

    add_part(sch, "Connector:TestPoint", "TP87", "RAIL_3V3", (342.90, 154.94))
    label_pin(sch, "TP87", "1", "RAIL_3V3")
    add_part(sch, "Connector:TestPoint", "TP88", "GND", (355.60, 154.94))
    label_pin(sch, "TP88", "1", "GND")

    sch.add_text(
        "MCP4728 LDAC is tied low: accepted writes update at the final-byte acknowledge.\n"
        "EEPROM must request 0xFFF attenuation, but TMUX1574 remains the authoritative safety layer.",
        position=(40.64, 116.84),
        size=1.27,
    )
    sch.add_text(
        "SEL low = +3.3 V safe attenuation. SEL high = MCP4728 normal control.\n"
        "HARDWARE_FAULT_N low clamps SEL low through D81; MCU release alone cannot override fault.",
        position=(137.16, 116.84),
        size=1.27,
    )
    sch.add_text(
        "Panel controls and LEDs are electrically captured only. Final panel mechanics and footprints remain blocked.",
        position=(40.64, 274.32),
        size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "08_CONTROLS_STATE component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")


if __name__ == "__main__":
    build()
