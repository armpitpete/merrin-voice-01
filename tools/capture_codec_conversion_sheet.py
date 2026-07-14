#!/usr/bin/env python3
"""Capture 03_CODEC_CONVERSION for Memory Core Prototype A.

Implements the accepted PCM3168A pin map, 48 kHz eight-slot TDM interface,
one buffered/attenuated differential ADC ingress, three AC-coupled
differential-to-single-ended DAC reconstruction stages, explicit unused-channel
treatment, local codec rail filtering, reset/mute gating and test points.

Active-device footprints remain blank pending independent verification.
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
SHEET_FILE = ROOT / "03_CODEC_CONVERSION.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "03_CODEC_CONVERSION_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_codec_symbol_helpers", POWER_HELPERS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_HELPERS}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

PCM_PIN_NAMES = {
    1: "VCOMAD", 2: "AGNDAD2", 3: "VCCAD2", 4: "RST", 5: "OVF",
    6: "LRCKAD", 7: "BCKAD", 8: "DOUT1", 9: "DOUT2", 10: "DOUT3",
    11: "DGND2", 12: "VDD2", 13: "ZERO", 14: "VCCDA1", 15: "VCOMDA",
    16: "AGNDDA1", 17: "VOUT8+", 18: "VOUT8-", 19: "VOUT7+",
    20: "VOUT7-", 21: "VOUT6+", 22: "VOUT6-", 23: "VOUT5+",
    24: "VOUT5-", 25: "VOUT4+", 26: "VOUT4-", 27: "VOUT3+",
    28: "VOUT3-", 29: "VOUT2+", 30: "VOUT2-", 31: "VOUT1+",
    32: "VOUT1-", 33: "AGNDDA2", 34: "VCCDA2", 35: "LRCKDA",
    36: "BCKDA", 37: "DIN1", 38: "DIN2", 39: "DIN3", 40: "DIN4",
    41: "SCKI", 42: "MC/SCL/FMT", 43: "MDI/SDA/DEMP", 44: "MDO/ADR1/MD1",
    45: "MS/ADR0/MD0", 46: "VDD1", 47: "DGND1", 48: "MODE",
    49: "VCCAD1", 50: "AGNDAD1", 51: "VIN1-", 52: "VIN1+",
    53: "VIN2-", 54: "VIN2+", 55: "VIN3-", 56: "VIN3+",
    57: "VIN4-", 58: "VIN4+", 59: "VREFAD1", 60: "VREFAD2",
    61: "VIN5-", 62: "VIN5+", 63: "VIN6-", 64: "VIN6+",
    65: "POWERPAD",
}

PCM_POWER_INPUTS = {2, 3, 11, 12, 14, 16, 33, 34, 46, 47, 49, 50, 65}
PCM_POWER_OUTPUTS = {1, 15, 59, 60}
PCM_INPUTS = {
    4, 6, 7, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 48,
    51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64,
}
PCM_OUTPUTS = {5, 8, 9, 10, 13, *range(17, 33)}
PCM_BIDIRECTIONAL = {43}

PCM_SELECTED_NETS = {
    1: "CODEC_VCOMAD", 2: "GND", 3: "CODEC_5V_LOCAL", 4: "CODEC_RST_HW_N",
    5: "CODEC_OVF", 6: "CODEC_LRCLK", 7: "CODEC_BCLK", 8: "CODEC_DOUT",
    11: "GND", 12: "CODEC_3V3_LOCAL", 13: "CODEC_ZERO", 14: "CODEC_5V_LOCAL",
    15: "CODEC_VCOMDA", 16: "GND", 27: "RETURN_DAC_P", 28: "RETURN_DAC_N",
    29: "GHOST_DAC_P", 30: "GHOST_DAC_N", 31: "MEMORY_DAC_P", 32: "MEMORY_DAC_N",
    33: "GND", 34: "CODEC_5V_LOCAL", 35: "CODEC_LRCLK", 36: "CODEC_BCLK",
    37: "CODEC_DIN", 38: "GND", 39: "GND", 40: "GND", 41: "CODEC_MCLK",
    42: "CTRL_I2C_SCL", 43: "CTRL_I2C_SDA", 44: "GND", 45: "GND",
    46: "CODEC_3V3_LOCAL", 47: "GND", 48: "GND", 49: "CODEC_5V_LOCAL",
    50: "GND", 51: "ADC_VIN1_N", 52: "ADC_VIN1_P", 53: "ADC2_UNUSED",
    54: "ADC2_UNUSED", 55: "ADC3_UNUSED", 56: "ADC3_UNUSED", 57: "ADC4_UNUSED",
    58: "ADC4_UNUSED", 59: "CODEC_VREFAD1", 60: "CODEC_VREFAD2",
    61: "ADC5_UNUSED", 62: "ADC5_UNUSED", 63: "ADC6_UNUSED", 64: "ADC6_UNUSED",
    65: "GND",
}

HIER_INPUTS = (
    "RAIL_P12", "RAIL_N12", "RAIL_3V3", "RAIL_5V_CODEC",
    "CODEC_MCLK", "CODEC_BCLK", "CODEC_LRCLK", "CODEC_DIN",
    "CTRL_I2C_SCL", "CTRL_I2C_SDA", "CODEC_RESET_N", "CODEC_MUTE_N",
    "ADC_ANALOG_IN",
)
HIER_OUTPUTS = ("CODEC_DOUT", "MEMORY_DAC", "GHOST_DAC", "RETURN_DAC")


def pcm_pin_type(pin: int) -> str:
    if pin in PCM_POWER_INPUTS:
        return "power_in"
    if pin in PCM_POWER_OUTPUTS:
        return "power_out"
    if pin in PCM_INPUTS:
        return "input"
    if pin in PCM_OUTPUTS:
        return "output"
    if pin in PCM_BIDIRECTIONAL:
        return "bidirectional"
    raise ValueError(pin)


def pcm_symbol() -> helpers.SymbolDefinition:
    pins = []
    for number in range(1, 66):
        if number <= 32:
            side, row = "left", number
        else:
            side, row = "right", number - 32
        pins.append(
            helpers.SymbolPin(str(number), PCM_PIN_NAMES[number], pcm_pin_type(number), side, row)
        )
    return helpers.SymbolDefinition(
        "PCM3168A_PAP_APPLICATION",
        "PCM3168A application-specific 64-pin HTQFP + PowerPAD symbol; TI SBAS452A",
        "https://www.ti.com/lit/ds/symlink/pcm3168a.pdf",
        tuple(pins),
    )


OPA1679 = helpers.SymbolDefinition(
    "OPA1679_PW_APPLICATION",
    "OPA1679 quad audio op amp; TSSOP-14 pin map; footprint pending",
    "https://www.ti.com/lit/ds/symlink/opa1679.pdf",
    (
        helpers.SymbolPin("1", "OUT_A", "output", "left", 1),
        helpers.SymbolPin("2", "IN_A-", "input", "left", 2),
        helpers.SymbolPin("3", "IN_A+", "input", "left", 3),
        helpers.SymbolPin("4", "V+", "power_in", "left", 4),
        helpers.SymbolPin("5", "IN_B+", "input", "left", 6),
        helpers.SymbolPin("6", "IN_B-", "input", "left", 7),
        helpers.SymbolPin("7", "OUT_B", "output", "left", 8),
        helpers.SymbolPin("8", "OUT_C", "output", "right", 1),
        helpers.SymbolPin("9", "IN_C-", "input", "right", 2),
        helpers.SymbolPin("10", "IN_C+", "input", "right", 3),
        helpers.SymbolPin("11", "V-", "power_in", "right", 4),
        helpers.SymbolPin("12", "IN_D+", "input", "right", 6),
        helpers.SymbolPin("13", "IN_D-", "input", "right", 7),
        helpers.SymbolPin("14", "OUT_D", "output", "right", 8),
    ),
)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    for definition in (pcm_symbol(), OPA1679):
        if f'(symbol "{definition.name}"' not in text:
            additions.append(helpers.render_symbol(definition))
    if not additions:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    SYMBOL_LIBRARY.write_text(stripped[:-1] + "".join(additions) + ")\n", encoding="utf-8")


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("03_CODEC_CONVERSION sheet not found")


def add_part(sch, lib_id, reference, value, position, footprint=""):
    return sch.components.add(
        lib_id=lib_id, reference=reference, value=value, position=position, footprint=footprint
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


def add_dac_stage(sch, prefix, refs, op_ref, pins, codec_p, codec_n, output_net, y):
    out_pin, minus_pin, plus_pin = pins
    raw_p = f"{prefix}_RAW_P"
    raw_n = f"{prefix}_RAW_N"
    filt_p = f"{prefix}_FILT_P"
    filt_n = f"{prefix}_FILT_N"
    op_p = f"{prefix}_OP_P"
    op_n = f"{prefix}_OP_N"
    op_out = f"{prefix}_OP_OUT"

    add_two_pin(sch, "Device:C", refs[0], "10µF AC", (245.0, y), codec_p, raw_p)
    add_two_pin(sch, "Device:C", refs[1], "10µF AC", (245.0, y + 10.0), codec_n, raw_n)
    add_two_pin(sch, "Device:R", refs[2], "7.5k", (265.0, y), raw_p, filt_p, "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", refs[3], "7.5k", (265.0, y + 10.0), raw_n, filt_n, "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", refs[4], "3.3nF", (280.0, y + 5.0), filt_p, filt_n, "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", refs[5], "360R", (295.0, y), filt_p, op_p, "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", refs[6], "360R", (295.0, y + 10.0), filt_n, op_n, "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", refs[7], "5.6k", (315.0, y - 5.0), op_p, "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", refs[8], "680pF", (330.0, y - 5.0), op_p, "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", refs[9], "5.6k", (315.0, y + 15.0), op_out, op_n, "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", refs[10], "680pF", (330.0, y + 15.0), op_out, op_n, "Capacitor_SMD:C_0805_2012Metric")

    label_pin(sch, op_ref, plus_pin, op_p)
    label_pin(sch, op_ref, minus_pin, op_n)
    label_pin(sch, op_ref, out_pin, op_out)
    add_two_pin(sch, "Device:R", refs[11], "47R output", (355.0, y + 5.0), op_out, output_net, "Resistor_SMD:R_0805_2012Metric")


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
        title="Memory Core Prototype A — Codec / Conversion",
        rev="V5.2 component capture 03",
        company="MerrinLab",
        comments={
            1: "PCM3168A 48 kHz / 8-slot TDM; ADC1 + DAC1–3 only.",
            2: "Codec/op-amp footprints remain blocked pending independent review.",
        },
    )
    sch.add_text("03 — CODEC / CONVERSION", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "PCM3168A • DIFFERENTIAL ADC INGRESS • MEMORY / GHOST / RETURN DAC FILTERS",
        position=(20.32, 17.78), size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        shape = HierarchicalLabelShape.BIDIRECTIONAL if signal == "CTRL_I2C_SDA" else HierarchicalLabelShape.INPUT
        add_hier(sch, signal, (20.32, y), shape, (35.56, y))
        y += 6.35
    y = 30.48
    for signal in HIER_OUTPUTS:
        add_hier(sch, signal, (391.16, y), HierarchicalLabelShape.OUTPUT, (375.92, y))
        y += 12.70

    ground = add_part(sch, "power:GND", "#PWR0301", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0301", "1", "GND")

    # Local filtered codec rails.
    add_two_pin(sch, "Device:L_Ferrite", "FB30", "600R@100MHz provisional", (60.96, 129.54), "RAIL_5V_CODEC", "CODEC_5V_LOCAL")
    add_two_pin(sch, "Device:L_Ferrite", "FB31", "600R@100MHz provisional", (60.96, 144.78), "RAIL_3V3", "CODEC_3V3_LOCAL")
    for ref, net, x in (("#FLG0301", "CODEC_5V_LOCAL", 78.74), ("#FLG0302", "CODEC_3V3_LOCAL", 91.44)):
        flag = add_part(sch, "power:PWR_FLAG", ref, "PWR_FLAG", (x, 137.16))
        flag.in_bom = False
        flag.on_board = False
        label_pin(sch, ref, "1", net)
    add_two_pin(sch, "Device:C", "C300", "10µF bulk", (78.74, 129.54), "CODEC_5V_LOCAL", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C301", "10µF bulk", (91.44, 144.78), "CODEC_3V3_LOCAL", "GND", "Capacitor_SMD:C_0805_2012Metric")

    add_part(sch, "MerrinLab_PrototypeA:PCM3168A_PAP_APPLICATION", "U30", "PCM3168A", (190.50, 139.70))
    for pin, net in PCM_SELECTED_NETS.items():
        label_pin(sch, "U30", pin, net)
    for pin in (9, 10, *range(17, 27)):
        no_connect_pin(sch, "U30", pin)

    # Per-supply decoupling and common/reference capacitors.
    supply_caps = (
        ("C302", "CODEC_5V_LOCAL", "GND"), ("C303", "CODEC_5V_LOCAL", "GND"),
        ("C304", "CODEC_5V_LOCAL", "GND"), ("C305", "CODEC_5V_LOCAL", "GND"),
        ("C306", "CODEC_3V3_LOCAL", "GND"), ("C307", "CODEC_3V3_LOCAL", "GND"),
    )
    for index, (ref, net1, net2) in enumerate(supply_caps):
        add_two_pin(sch, "Device:C", ref, "1µF local", (104.14 + index * 12.70, 205.74), net1, net2, "Capacitor_SMD:C_0805_2012Metric")
    for ref, net, x in (
        ("C308", "CODEC_VCOMAD", 104.14), ("C309", "CODEC_VCOMDA", 119.38),
        ("C310", "CODEC_VREFAD1", 134.62), ("C311", "CODEC_VREFAD2", 149.86),
    ):
        add_two_pin(sch, "Device:C", ref, "10µF reference", (x, 220.98), net, "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Active-low reset/mute AND: either low holds PCM3168A in reset/power-down.
    add_two_pin(sch, "Device:R", "R300", "10k reset pull-up", (104.14, 99.06), "CODEC_3V3_LOCAL", "CODEC_RST_HW_N", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D300", "BAT54-class", (119.38, 93.98), "CODEC_RESET_N", "CODEC_RST_HW_N")
    add_two_pin(sch, "Device:D_Schottky", "D301", "BAT54-class", (119.38, 104.14), "CODEC_MUTE_N", "CODEC_RST_HW_N")
    for reference, net, position in (
        ("TP300", "CODEC_OVF", (137.16, 93.98)), ("TP301", "CODEC_ZERO", (149.86, 93.98)),
        ("TP302", "CODEC_RST_HW_N", (162.56, 93.98)),
    ):
        add_part(sch, "Connector:TestPoint", reference, net, position)
        label_pin(sch, reference, "1", net)

    # Explicit unused differential ADC termination: pair together, then 100 nF to AGND.
    for index, net in enumerate(("ADC2_UNUSED", "ADC3_UNUSED", "ADC4_UNUSED", "ADC5_UNUSED", "ADC6_UNUSED"), start=0):
        add_two_pin(sch, "Device:C", f"C31{2 + index}", "100nF unused ADC", (172.72 + index * 12.70, 220.98), net, "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Two OPA1679 packages on accepted ±12 V analogue rails.
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U31", "OPA1679 ADC + MEMORY/GHOST", (173.0, 251.0))
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U32", "OPA1679 RETURN + SPARES", (326.0, 251.0))
    for ref in ("U31", "U32"):
        label_pin(sch, ref, "4", "RAIL_P12")
        label_pin(sch, ref, "11", "RAIL_N12")
    for i, ref in enumerate(("U31", "U32")):
        add_two_pin(sch, "Device:C", f"C32{i*4}", "100nF + rail", (70.0 + i * 40.0, 251.0), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C32{i*4+1}", "100nF - rail", (82.0 + i * 40.0, 251.0), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C32{i*4+2}", "4.7µF + rail", (94.0 + i * 40.0, 251.0), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C32{i*4+3}", "4.7µF - rail", (106.0 + i * 40.0, 251.0), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # ADC driver: +1/3 buffered phase and -1/3 inverting phase.
    add_two_pin(sch, "Device:R", "R301", "20k", (82.55, 174.62), "ADC_ANALOG_IN", "ADC_POS_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R302", "10k", (95.25, 174.62), "ADC_POS_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U31", "3", "ADC_POS_DIV")
    label_pin(sch, "U31", "2", "ADC_POS_BUF")
    label_pin(sch, "U31", "1", "ADC_POS_BUF")
    add_two_pin(sch, "Device:R", "R303", "30k", (82.55, 187.32), "ADC_ANALOG_IN", "ADC_NEG_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R304", "10k", (95.25, 187.32), "ADC_NEG_BUF", "ADC_NEG_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U31", "5", "GND")
    label_pin(sch, "U31", "6", "ADC_NEG_SUM")
    label_pin(sch, "U31", "7", "ADC_NEG_BUF")

    add_two_pin(sch, "Device:C", "C330", "1µF AC", (111.76, 174.62), "ADC_POS_BUF", "ADC_POS_AC")
    add_two_pin(sch, "Device:R", "R305", "100k bias", (124.46, 174.62), "CODEC_VCOMAD", "ADC_POS_AC", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R306", "1.5k", (137.16, 174.62), "ADC_POS_AC", "ADC_VIN1_P", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C331", "2.2nF anti-alias", (149.86, 174.62), "ADC_VIN1_P", "CODEC_VCOMAD", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C332", "1µF AC", (111.76, 187.32), "ADC_NEG_BUF", "ADC_NEG_AC")
    add_two_pin(sch, "Device:R", "R307", "100k bias", (124.46, 187.32), "CODEC_VCOMAD", "ADC_NEG_AC", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R308", "1.5k", (137.16, 187.32), "ADC_NEG_AC", "ADC_VIN1_N", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C333", "2.2nF anti-alias", (149.86, 187.32), "ADC_VIN1_N", "CODEC_VCOMAD", "Capacitor_SMD:C_0805_2012Metric")

    # TI Figure 61-style AC-coupled differential-to-single-ended DAC filters.
    add_dac_stage(sch, "MEM", ["C340", "C341", "R340", "R341", "C342", "R342", "R343", "R344", "C343", "R345", "C344", "R346"], "U31", ("8", "9", "10"), "MEMORY_DAC_P", "MEMORY_DAC_N", "MEMORY_DAC", 116.84)
    add_dac_stage(sch, "GHOST", ["C345", "C346", "R347", "R348", "C347", "R349", "R350", "R351", "C348", "R352", "C349", "R353"], "U31", ("14", "13", "12"), "GHOST_DAC_P", "GHOST_DAC_N", "GHOST_DAC", 157.48)
    add_dac_stage(sch, "RETURN", ["C350", "C351", "R354", "R355", "C352", "R356", "R357", "R358", "C353", "R359", "C354", "R360"], "U32", ("1", "2", "3"), "RETURN_DAC_P", "RETURN_DAC_N", "RETURN_DAC", 198.12)

    # U32 B/C/D unused channels: unity followers at 0 V.
    for out_pin, minus_pin, plus_pin, net in (
        ("7", "6", "5", "U32B_SPARE_FB"),
        ("8", "9", "10", "U32C_SPARE_FB"),
        ("14", "13", "12", "U32D_SPARE_FB"),
    ):
        label_pin(sch, "U32", plus_pin, "GND")
        label_pin(sch, "U32", minus_pin, net)
        label_pin(sch, "U32", out_pin, net)

    # Bench/service test points.
    for reference, net, position in (
        ("TP303", "ADC_ANALOG_IN", (50.80, 174.62)),
        ("TP304", "ADC_VIN1_P", (162.56, 174.62)),
        ("TP305", "ADC_VIN1_N", (162.56, 187.32)),
        ("TP306", "MEMORY_DAC", (370.84, 121.92)),
        ("TP307", "GHOST_DAC", (370.84, 162.56)),
        ("TP308", "RETURN_DAC", (370.84, 203.20)),
        ("TP309", "CODEC_5V_LOCAL", (78.74, 116.84)),
        ("TP310", "CODEC_3V3_LOCAL", (91.44, 157.48)),
    ):
        add_part(sch, "Connector:TestPoint", reference, net, position)
        label_pin(sch, reference, "1", net)

    sch.add_text(
        "ADC gain contract: each phase = ±ADC_ANALOG_IN / 3.\n"
        "2 Vpp nominal → 1.333 Vpp differential ≈ −12.6 dBFS; 6 Vpp → 4 Vpp differential ≈ −3.0 dBFS.",
        position=(45.72, 228.60), size=1.27,
    )
    sch.add_text(
        "DAC filters follow TI Figure 61 nominal values: R1 7.5k, R2 5.6k, R3 360R, C1 3.3nF, C2 680pF, gain ≈ 0.747, f−3dB ≈ 53kHz.",
        position=(220.98, 228.60), size=1.27,
    )
    sch.add_text(
        "ADC2–6 differential pins are paired and AC-terminated to AGND; DAC4–8 and DOUT2/3 are explicit no-connects.\n"
        "Firmware keeps inactive channels muted/power-save. VCOM/VREF are local decoupling references only.",
        position=(45.72, 266.70), size=1.27,
    )
    sch.add_text(
        "CODEC_MUTE_N is a hard reset/power-down request through the diode AND gate.\n"
        "PCM soft mute remains I²C-controlled; external SSI2164 attenuation remains the primary wet/Return safety clamp.",
        position=(220.98, 251.46), size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "03_CODEC_CONVERSION component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("PCM3168A package pins encoded: 64 + PowerPAD")


if __name__ == "__main__":
    build()
