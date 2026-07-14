#!/usr/bin/env python3
"""Capture 02_MCU_CLOCK_DEBUG for Memory Core Prototype A.

The sheet uses the exact STM32H743VIT6 LQFP-100 top-view pin map from ST
DS12110 Rev 11 (January 2026). It implements the accepted SAI1, I2C1, panel
ADC, safety, state, reset and SWD allocation, plus power/reference decoupling
and a 24.576 MHz external HSE oscillator.

The STM32 and oscillator footprints remain blank pending independent package
and footprint review. Unused MCU pins receive explicit no-connect markers.
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
SHEET_FILE = ROOT / "02_MCU_CLOCK_DEBUG.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "02_MCU_CLOCK_DEBUG_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_mcu_symbol_helpers", POWER_HELPERS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_HELPERS}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

# Exact LQFP-100 pin map from ST DS12110 Rev 11, Figure 5.
PIN_NAMES = {
    1: "PE2", 2: "PE3", 3: "PE4", 4: "PE5", 5: "PE6",
    6: "VBAT", 7: "PC13", 8: "PC14-OSC32_IN", 9: "PC15-OSC32_OUT",
    10: "VSS", 11: "VDD", 12: "PH0-OSC_IN", 13: "PH1-OSC_OUT",
    14: "NRST", 15: "PC0", 16: "PC1", 17: "PC2_C", 18: "PC3_C",
    19: "VSSA", 20: "VREF+", 21: "VDDA", 22: "PA0", 23: "PA1",
    24: "PA2", 25: "PA3", 26: "VSS", 27: "VDD", 28: "PA4",
    29: "PA5", 30: "PA6", 31: "PA7", 32: "PC4", 33: "PC5",
    34: "PB0", 35: "PB1", 36: "PB2", 37: "PE7", 38: "PE8",
    39: "PE9", 40: "PE10", 41: "PE11", 42: "PE12", 43: "PE13",
    44: "PE14", 45: "PE15", 46: "PB10", 47: "PB11", 48: "VCAP1",
    49: "VSS", 50: "VDD", 51: "PB12", 52: "PB13", 53: "PB14",
    54: "PB15", 55: "PD8", 56: "PD9", 57: "PD10", 58: "PD11",
    59: "PD12", 60: "PD13", 61: "PD14", 62: "PD15", 63: "PC6",
    64: "PC7", 65: "PC8", 66: "PC9", 67: "PA8", 68: "PA9",
    69: "PA10", 70: "PA11", 71: "PA12", 72: "PA13", 73: "VCAP2",
    74: "VSS", 75: "VDD", 76: "PA14", 77: "PA15", 78: "PC10",
    79: "PC11", 80: "PC12", 81: "PD0", 82: "PD1", 83: "PD2",
    84: "PD3", 85: "PD4", 86: "PD5", 87: "PD6", 88: "PD7",
    89: "PB3", 90: "PB4", 91: "PB5", 92: "PB6", 93: "PB7",
    94: "BOOT0", 95: "PB8", 96: "PB9", 97: "PE0", 98: "PE1",
    99: "VSS", 100: "VDD",
}

POWER_IN_PINS = {6, 10, 11, 19, 20, 21, 26, 27, 49, 50, 74, 75, 99, 100}
POWER_OUT_PINS = {48, 73}
INPUT_PINS = {2, 12, 14, 22, 23, 24, 25, 28, 29, 30, 31, 57, 60, 61, 62, 76, 94}
OUTPUT_PINS = {1, 3, 4, 5, 13, 55, 56, 58, 59, 63, 64, 65, 66}
BIDIRECTIONAL_PINS = {72, 95, 96}

SELECTED_NETS = {
    1: "CODEC_MCLK",
    2: "CODEC_DOUT",
    3: "CODEC_LRCLK",
    4: "CODEC_BCLK",
    5: "CODEC_DIN",
    6: "RAIL_3V3",
    10: "GND",
    11: "RAIL_3V3",
    12: "HSE_IN",
    14: "HARDWARE_FAULT_N",
    19: "GND",
    20: "MCU_ANALOG_3V3",
    21: "MCU_ANALOG_3V3",
    22: "PANEL_MEMORY_TIME",
    23: "PANEL_MEMORY_FADE",
    24: "PANEL_MEMORY_BLUR",
    25: "PANEL_GHOST_DISTANCE",
    26: "GND",
    27: "RAIL_3V3",
    28: "PANEL_GHOST_DRIFT",
    29: "PANEL_GHOST_PRESENCE",
    30: "PANEL_RETURN_AMOUNT",
    31: "PANEL_PRESENT_WET",
    48: "VCAP1",
    49: "GND",
    50: "RAIL_3V3",
    55: "CODEC_RESET_N",
    56: "CODEC_MUTE_N",
    57: "HARDWARE_FAULT_N",
    58: "WATCHDOG_HEARTBEAT",
    59: "SAFE_CONTROL_RELEASE",
    60: "SERVICE_TEST",
    61: "RESET_CLEAR",
    62: "SAFE_MUTE",
    63: "STATE_LED_R",
    64: "STATE_LED_G",
    65: "STATE_LED_B",
    66: "STATE_LED_AUX",
    72: "SWDIO",
    73: "VCAP2",
    74: "GND",
    75: "RAIL_3V3",
    76: "SWCLK",
    94: "BOOT0",
    95: "CTRL_I2C_SCL",
    96: "CTRL_I2C_SDA",
    99: "GND",
    100: "RAIL_3V3",
}

HIER_INPUTS = (
    "RAIL_3V3", "HARDWARE_FAULT_N", "CODEC_DOUT", "CTRL_I2C_SDA",
    "PANEL_MEMORY_TIME", "PANEL_MEMORY_FADE", "PANEL_MEMORY_BLUR",
    "PANEL_GHOST_DISTANCE", "PANEL_GHOST_DRIFT", "PANEL_GHOST_PRESENCE",
    "PANEL_RETURN_AMOUNT", "PANEL_PRESENT_WET",
    "SERVICE_TEST", "RESET_CLEAR", "SAFE_MUTE",
)

HIER_OUTPUTS = (
    "CODEC_MCLK", "CODEC_BCLK", "CODEC_LRCLK", "CODEC_DIN",
    "CTRL_I2C_SCL", "CODEC_RESET_N", "CODEC_MUTE_N",
    "SAFE_CONTROL_RELEASE", "WATCHDOG_HEARTBEAT",
    "STATE_LED_R", "STATE_LED_G", "STATE_LED_B", "STATE_LED_AUX",
)


def pin_type(pin: int) -> str:
    if pin in POWER_IN_PINS:
        return "power_in"
    if pin in POWER_OUT_PINS:
        return "power_out"
    if pin in INPUT_PINS:
        return "input"
    if pin in OUTPUT_PINS:
        return "output"
    if pin in BIDIRECTIONAL_PINS:
        return "bidirectional"
    return "bidirectional"


def mcu_symbol() -> helpers.SymbolDefinition:
    pins = []
    for number in range(1, 101):
        if number <= 50:
            side = "left"
            row = number
        else:
            side = "right"
            row = number - 50
        pins.append(
            helpers.SymbolPin(
                str(number),
                PIN_NAMES[number],
                pin_type(number),
                side,
                row,
            )
        )

    return helpers.SymbolDefinition(
        "STM32H743VIT6_LQFP100",
        "STM32H743VIT6 application-specific LQFP-100 symbol; ST DS12110 Rev 11 Figure 5",
        "https://www.st.com/resource/en/datasheet/stm32h743vi.pdf",
        tuple(pins),
    )


OSCILLATOR_SYMBOL = helpers.SymbolDefinition(
    "OSC_CMOS_4PIN",
    "Generic 24.576 MHz 3.3 V CMOS oscillator; exact part and footprint pending",
    "",
    (
        helpers.SymbolPin("1", "EN", "input", "left", 1),
        helpers.SymbolPin("2", "GND", "power_in", "left", 3),
        helpers.SymbolPin("4", "VDD", "power_in", "left", 2),
        helpers.SymbolPin("3", "OUT", "output", "right", 2),
    ),
)


def append_symbols() -> None:
    library = SYMBOL_LIBRARY
    text = library.read_text(encoding="utf-8")
    additions = []
    for definition in (mcu_symbol(), OSCILLATOR_SYMBOL):
        if f'(symbol "{definition.name}"' not in text:
            additions.append(helpers.render_symbol(definition))

    if not additions:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    library.write_text(stripped[:-1] + "".join(additions) + ")\n", encoding="utf-8")


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("02_MCU_CLOCK_DEBUG sheet not found")


def add_part(sch, lib_id, reference, value, position, footprint=""):
    return sch.components.add(
        lib_id=lib_id,
        reference=reference,
        value=value,
        position=position,
        footprint=footprint,
    )


def pin_position(sch, reference, pin):
    point = sch.get_component_pin_position(reference, str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def no_connect_pin(sch, reference, pin):
    sch.no_connects.add(position=pin_position(sch, reference, pin))


def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_hier(sch, name, position, shape, end):
    sch.add_hierarchical_label(name, position=position, shape=shape, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def build() -> None:
    append_symbols()
    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))

    top = ksa.load_schematic(str(TOP))
    parent_uuid, sheet_uuid = find_sheet_context(top)

    sch = ksa.create_schematic(PROJECT)
    sch.set_hierarchy_context(parent_uuid, sheet_uuid)
    sch.set_paper_size("A3")
    sch.set_title_block(
        title="Memory Core Prototype A — MCU / Clock / Debug",
        rev="V5.2 component capture 02",
        company="MerrinLab",
        comments={
            1: "Exact LQFP-100 pin map from ST DS12110 Rev 11 Figure 5.",
            2: "MCU and oscillator footprints remain blocked pending review.",
        },
    )

    sch.add_text("02 — MCU / CLOCK / DEBUG", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "STM32H743VIT6 • 24.576 MHz HSE BYPASS • SAI1 TDM • I²C1 • SWD",
        position=(20.32, 17.78),
        size=1.27,
    )

    # Hierarchical interfaces.
    y = 30.48
    for signal in HIER_INPUTS:
        shape = HierarchicalLabelShape.BIDIRECTIONAL if signal == "CTRL_I2C_SDA" else HierarchicalLabelShape.INPUT
        add_hier(sch, signal, (20.32, y), shape, (35.56, y))
        y += 6.35

    y = 30.48
    for signal in HIER_OUTPUTS:
        add_hier(sch, signal, (391.16, y), HierarchicalLabelShape.OUTPUT, (375.92, y))
        y += 6.35

    # MCU and exact pin mapping.
    add_part(
        sch,
        "MerrinLab_PrototypeA:STM32H743VIT6_LQFP100",
        "U10",
        "STM32H743VIT6",
        (205.74, 144.78),
    )

    for pin, net in SELECTED_NETS.items():
        label_pin(sch, "U10", pin, net)

    for pin in range(1, 101):
        if pin not in SELECTED_NETS:
            no_connect_pin(sch, "U10", pin)

    # Global ground on this captured sheet.
    ground = add_part(sch, "power:GND", "#PWR0201", "GND", (205.74, 279.40))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0201", "1", "GND")

    # Digital decoupling for five VDD pins plus bulk.
    decoupling_x = (101.60, 116.84, 132.08, 147.32, 162.56)
    for index, x in enumerate(decoupling_x, start=1):
        add_two_pin(
            sch,
            "Device:C",
            f"C20{index}",
            "100nF",
            (x, 228.60),
            "RAIL_3V3",
            "GND",
            "Capacitor_SMD:C_0805_2012Metric",
        )
    add_two_pin(sch, "Device:C", "C206", "4.7µF", (177.80, 228.60), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Analogue supply/reference filtering.
    add_two_pin(sch, "Device:L_Ferrite", "FB20", "600Ω@100MHz provisional", (106.68, 177.80), "RAIL_3V3", "MCU_ANALOG_3V3")
    add_two_pin(sch, "Device:C", "C207", "1µF", (124.46, 177.80), "MCU_ANALOG_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C208", "100nF", (139.70, 177.80), "MCU_ANALOG_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    flag = add_part(sch, "power:PWR_FLAG", "#FLG0201", "PWR_FLAG", (154.94, 177.80))
    flag.in_bom = False
    flag.on_board = False
    label_pin(sch, "#FLG0201", "1", "MCU_ANALOG_3V3")

    # VCAP outputs require dedicated low-ESR capacitors and no other load.
    add_two_pin(sch, "Device:C", "C209", "2.2µF low-ESR", (258.06, 170.18), "VCAP1", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C210", "2.2µF low-ESR", (273.30, 170.18), "VCAP2", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # VBAT is tied to 3.3 V because Prototype A has no battery domain.
    add_two_pin(sch, "Device:C", "C211", "100nF", (106.68, 193.04), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Exact audio-family reference: active 24.576 MHz oscillator into HSE bypass input.
    add_part(sch, "MerrinLab_PrototypeA:OSC_CMOS_4PIN", "U11", "24.576MHz 3V3 CMOS OSC", (86.36, 124.46))
    for pin, net in {"1": "RAIL_3V3", "2": "GND", "4": "RAIL_3V3", "3": "HSE_OSC_OUT"}.items():
        label_pin(sch, "U11", pin, net)
    add_two_pin(sch, "Device:R", "R200", "33Ω series", (111.76, 124.46), "HSE_OSC_OUT", "HSE_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C212", "100nF", (71.12, 124.46), "RAIL_3V3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_part(sch, "Connector:TestPoint", "TP200", "HSE_24M576", (124.46, 116.84))
    label_pin(sch, "TP200", "1", "HSE_IN")

    # Safe defaults for codec reset and mute outputs.
    add_two_pin(sch, "Device:R", "R201", "100k reset default low", (304.80, 83.82), "CODEC_RESET_N", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R202", "100k mute default low", (320.04, 83.82), "CODEC_MUTE_N", "GND", "Resistor_SMD:R_0805_2012Metric")

    # BOOT0 deterministic low with service test point.
    add_two_pin(sch, "Device:R", "R203", "100k BOOT0 pull-down", (289.56, 193.04), "BOOT0", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_part(sch, "Connector:TestPoint", "TP201", "BOOT0", (304.80, 193.04))
    label_pin(sch, "TP201", "1", "BOOT0")

    # SWD service connector. Footprint remains blank pending service/mechanical decision.
    add_part(sch, "Connector_Generic:Conn_01x05", "J20", "SWD SERVICE", (342.90, 167.64))
    for pin, net in {"1": "RAIL_3V3", "2": "SWDIO", "3": "SWCLK", "4": "HARDWARE_FAULT_N", "5": "GND"}.items():
        label_pin(sch, "J20", pin, net)

    # Key digital and safety test points.
    test_points = (
        ("TP202", "CODEC_MCLK", "CODEC_MCLK", (304.80, 111.76)),
        ("TP203", "CODEC_BCLK", "CODEC_BCLK", (320.04, 111.76)),
        ("TP204", "CODEC_LRCLK", "CODEC_LRCLK", (335.28, 111.76)),
        ("TP205", "CODEC_DIN", "CODEC_DIN", (350.52, 111.76)),
        ("TP206", "CODEC_DOUT", "CODEC_DOUT", (365.76, 111.76)),
        ("TP207", "I2C_SCL", "CTRL_I2C_SCL", (304.80, 127.00)),
        ("TP208", "I2C_SDA", "CTRL_I2C_SDA", (320.04, 127.00)),
        ("TP209", "WATCHDOG_HEARTBEAT", "WATCHDOG_HEARTBEAT", (335.28, 127.00)),
        ("TP210", "FAULT_RESET_N", "HARDWARE_FAULT_N", (350.52, 127.00)),
        ("TP211", "SAFE_RELEASE", "SAFE_CONTROL_RELEASE", (365.76, 127.00)),
        ("TP212", "MCU_ANALOG_3V3", "MCU_ANALOG_3V3", (154.94, 193.04)),
    )
    for reference, value, net, position in test_points:
        add_part(sch, "Connector:TestPoint", reference, value, position)
        label_pin(sch, reference, "1", net)

    sch.add_text(
        "HSE bypass mode: U11 drives PH0-OSC_IN through R200; PH1-OSC_OUT is explicitly unused.\n"
        "24.576 MHz is within the STM32H743 4–48 MHz external HSE range.",
        position=(40.64, 147.32),
        size=1.27,
    )
    sch.add_text(
        "All unused LQFP-100 GPIOs are explicitly no-connect.\n"
        "The accepted allocation is encoded by physical pin number, not symbol position.",
        position=(259.08, 216.66),
        size=1.27,
    )
    sch.add_text(
        "U10 and U11 footprints intentionally blank. Final decoupling placement, oscillator part,\n"
        "LQFP land pattern and SWD connector remain footprint/mechanical gate items.",
        position=(40.64, 266.70),
        size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "02_MCU_CLOCK_DEBUG component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("STM32H743VIT6 LQFP-100 pins encoded: 100")


if __name__ == "__main__":
    build()
