#!/usr/bin/env python3
"""Capture 04_INPUT_PRESSURE_ABSENCE for Memory Core Prototype A.

Implements the switched input jack, quiet no-cable state, RF/overvoltage
protection, AC coupling and input buffering, the direct Present split, bounded
Pressure soft limiting, Return-derived Absence attenuation, and the final
Memory-input summing node. Only fixed RETURN_FEED and bounded
ABSENCE_INFLUENCE enter from sheet 06.

Active-device and jack footprints remain blank pending independent review.
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
SHEET_FILE = ROOT / "04_INPUT_PRESSURE_ABSENCE.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "04_INPUT_PRESSURE_ABSENCE_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_input_symbol_helpers", POWER_HELPERS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_HELPERS}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

HIER_INPUTS = ("RAIL_P12", "RAIL_N12", "RETURN_FEED", "ABSENCE_INFLUENCE")
HIER_OUTPUTS = ("DIRECT_PRESENT", "SHAPED_PRESENT", "ADC_ANALOG_IN")
ALLOWED_RETURN_IMPORTS = frozenset(("RETURN_FEED", "ABSENCE_INFLUENCE"))

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

WQP518MA = helpers.SymbolDefinition(
    "WQP518MA_APPLICATION",
    "Switched 3.5 mm mono input jack application symbol; physical pin map and footprint pending",
    "",
    (
        helpers.SymbolPin("1", "TIP", "passive", "left", 1),
        helpers.SymbolPin("2", "TIP_NORMAL", "passive", "left", 2),
        helpers.SymbolPin("3", "SLEEVE", "passive", "left", 3),
    ),
)

J113 = helpers.SymbolDefinition(
    "J113_SHUNT_APPLICATION",
    "N-channel JFET used as voltage-controlled shunt; pin map and footprint pending",
    "",
    (
        helpers.SymbolPin("1", "D", "passive", "left", 1),
        helpers.SymbolPin("2", "G", "input", "left", 2),
        helpers.SymbolPin("3", "S", "passive", "right", 1),
    ),
)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    for definition in (OPA1679, WQP518MA, J113):
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
    raise RuntimeError("04_INPUT_PRESSURE_ABSENCE sheet not found")


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


def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_hier(sch, name, position, shape, end):
    sch.add_hierarchical_label(name, position=position, shape=shape, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def add_test_point(sch, reference, value, net, position):
    add_part(sch, "Connector:TestPoint", reference, value, position)
    label_pin(sch, reference, "1", net)


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
        title="Memory Core Prototype A — Input / Pressure / Absence",
        rev="V5.2 component capture 04",
        company="MerrinLab",
        comments={
            1: "Direct Present splits before Pressure, Absence and Memory summing.",
            2: "Jack, JFET, op-amp and diode footprints remain blocked pending review.",
        },
    )
    sch.add_text("04 — INPUT / PRESSURE / ABSENCE", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "SWITCHED INPUT • QUIET NO-CABLE STATE • DIRECT PRESENT • PRESSURE • ABSENCE • MEMORY SUM",
        position=(20.32, 17.78), size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        add_hier(sch, signal, (20.32, y), HierarchicalLabelShape.INPUT, (35.56, y))
        y += 12.70
    y = 30.48
    for signal in HIER_OUTPUTS:
        add_hier(sch, signal, (391.16, y), HierarchicalLabelShape.OUTPUT, (375.92, y))
        y += 19.05

    ground = add_part(sch, "power:GND", "#PWR0401", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0401", "1", "GND")

    # Switched jack. TIP_NORMAL is grounded so no cable forces TIP to quiet zero.
    add_part(sch, "MerrinLab_PrototypeA:WQP518MA_APPLICATION", "J40", "WQP518MA / THONKICONN INPUT", (55.88, 91.44))
    label_pin(sch, "J40", "1", "INPUT_TIP")
    label_pin(sch, "J40", "2", "GND")
    label_pin(sch, "J40", "3", "GND")

    # Input protection and RF rejection before the audio buffer.
    add_two_pin(sch, "Device:R", "R400", "1k input protection", (81.28, 83.82), "INPUT_TIP", "INPUT_PROTECTED", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R401", "1M input reference", (93.98, 96.52), "INPUT_PROTECTED", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C400", "220pF RF", (106.68, 96.52), "INPUT_PROTECTED", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D400", "BAT54-class +rail clamp", (93.98, 76.20), "INPUT_PROTECTED", "RAIL_P12")
    add_two_pin(sch, "Device:D_Schottky", "D401", "BAT54-class -rail clamp", (106.68, 76.20), "RAIL_N12", "INPUT_PROTECTED")
    add_two_pin(sch, "Device:C", "C401", "1uF AC coupling", (121.92, 83.82), "INPUT_PROTECTED", "INPUT_AC")
    add_two_pin(sch, "Device:R", "R402", "1M post-coupling bias", (134.62, 96.52), "INPUT_AC", "GND", "Resistor_SMD:R_0805_2012Metric")

    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U40", "OPA1679 INPUT/PRESSURE/SUM", (203.20, 177.80))
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U41", "OPA1679 ABSENCE/OUTPUT", (317.50, 177.80))
    for ref in ("U40", "U41"):
        label_pin(sch, ref, "4", "RAIL_P12")
        label_pin(sch, ref, "11", "RAIL_N12")
    for index in range(2):
        x = 73.66 + index * 55.88
        base = 402 + index * 4
        add_two_pin(sch, "Device:C", f"C{base}", "100nF + rail", (x, 246.38), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C{base+1}", "100nF - rail", (x + 12.70, 246.38), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C{base+2}", "4.7uF + rail", (x + 25.40, 246.38), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C{base+3}", "4.7uF - rail", (x + 38.10, 246.38), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U40A input follower and Direct Present split.
    label_pin(sch, "U40", "3", "INPUT_AC")
    label_pin(sch, "U40", "2", "INPUT_BUFFER")
    label_pin(sch, "U40", "1", "INPUT_BUFFER")
    add_two_pin(sch, "Device:R", "R403", "47R direct isolation", (157.48, 83.82), "INPUT_BUFFER", "DIRECT_PRESENT", "Resistor_SMD:R_0805_2012Metric")

    # U40B Pressure: unity inverting stage with bounded feedback clipping and blur.
    add_two_pin(sch, "Device:R", "R404", "22k Pressure input", (157.48, 111.76), "INPUT_BUFFER", "PRESSURE_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U40", "5", "GND")
    label_pin(sch, "U40", "6", "PRESSURE_SUM")
    label_pin(sch, "U40", "7", "PRESSURE_OUT")
    add_two_pin(sch, "Device:R", "R405", "22k Pressure feedback", (182.88, 111.76), "PRESSURE_OUT", "PRESSURE_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C410", "1nF Pressure blur", (195.58, 111.76), "PRESSURE_OUT", "PRESSURE_SUM", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:D", "D402", "BAV199-class Pressure clip", (182.88, 124.46), "PRESSURE_OUT", "PRESSURE_SUM")
    add_two_pin(sch, "Device:D", "D403", "BAV199-class Pressure clip", (195.58, 124.46), "PRESSURE_SUM", "PRESSURE_OUT")

    # U41A/B map bounded 0-3 V Absence influence to approximately -8..0 V JFET gate drive.
    add_two_pin(sch, "Device:R", "R406", "30.1k Absence input", (233.68, 162.56), "ABSENCE_INFLUENCE", "ABS_CTRL_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R407", "121k -12V offset", (233.68, 175.26), "RAIL_N12", "ABS_CTRL_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U41", "3", "GND")
    label_pin(sch, "U41", "2", "ABS_CTRL_SUM")
    label_pin(sch, "U41", "1", "ABS_CTRL_POS")
    add_two_pin(sch, "Device:R", "R408", "80.6k control gain", (259.08, 162.56), "ABS_CTRL_POS", "ABS_CTRL_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R409", "22k gate inverter input", (271.78, 175.26), "ABS_CTRL_POS", "ABS_GATE_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U41", "5", "GND")
    label_pin(sch, "U41", "6", "ABS_GATE_SUM")
    label_pin(sch, "U41", "7", "ABS_GATE_DRIVE")
    add_two_pin(sch, "Device:R", "R410", "22k gate inverter feedback", (297.18, 175.26), "ABS_GATE_DRIVE", "ABS_GATE_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R411", "100k JFET gate stop", (297.18, 190.50), "ABS_GATE_DRIVE", "ABS_GATE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Zener", "D404", "9.1V gate clamp provisional", (309.88, 190.50), "GND", "ABS_GATE")

    # J113 shunts Pressure output progressively as Return-derived Absence rises.
    add_part(sch, "MerrinLab_PrototypeA:J113_SHUNT_APPLICATION", "Q40", "J113 ABSENCE SHUNT", (243.84, 124.46))
    label_pin(sch, "Q40", "1", "PRESSURE_OUT")
    label_pin(sch, "Q40", "2", "ABS_GATE")
    label_pin(sch, "Q40", "3", "GND")

    # U40C buffers shaped Present after the Absence shunt.
    label_pin(sch, "U40", "10", "PRESSURE_OUT")
    label_pin(sch, "U40", "9", "SHAPED_PRESENT")
    label_pin(sch, "U40", "8", "SHAPED_PRESENT")

    # U40D sums only shaped Present and fixed RETURN_FEED for Memory capture.
    add_two_pin(sch, "Device:R", "R412", "20k shaped input", (274.32, 111.76), "SHAPED_PRESENT", "MEMORY_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R413", "20k fixed Return input", (274.32, 124.46), "RETURN_FEED", "MEMORY_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U40", "12", "GND")
    label_pin(sch, "U40", "13", "MEMORY_SUM")
    label_pin(sch, "U40", "14", "MEMORY_SUM_OUT")
    add_two_pin(sch, "Device:R", "R414", "20k Memory feedback", (299.72, 111.76), "MEMORY_SUM_OUT", "MEMORY_SUM", "Resistor_SMD:R_0805_2012Metric")

    # U41C final ADC driver/buffer; codec sheet performs the accepted 1/3 differential conversion.
    label_pin(sch, "U41", "10", "MEMORY_SUM_OUT")
    label_pin(sch, "U41", "9", "ADC_ANALOG_IN")
    label_pin(sch, "U41", "8", "ADC_ANALOG_IN")
    add_two_pin(sch, "Device:R", "R415", "47R ADC isolation", (337.82, 111.76), "ADC_ANALOG_IN", "ADC_ANALOG_IN_OUT", "Resistor_SMD:R_0805_2012Metric")
    # Keep the hierarchical net on the isolated side.
    sch.add_label("ADC_ANALOG_IN", position=pin_position(sch, "R415", "2"))

    # U41D spare: stable 0 V follower.
    label_pin(sch, "U41", "12", "GND")
    label_pin(sch, "U41", "13", "INPUT_SPARE_OUT")
    label_pin(sch, "U41", "14", "INPUT_SPARE_OUT")

    for reference, value, net, position in (
        ("TP400", "INPUT_TIP", "INPUT_TIP", (55.88, 68.58)),
        ("TP401", "INPUT_PROTECTED", "INPUT_PROTECTED", (96.52, 68.58)),
        ("TP402", "INPUT_BUFFER", "INPUT_BUFFER", (147.32, 68.58)),
        ("TP403", "DIRECT_PRESENT", "DIRECT_PRESENT", (185.42, 68.58)),
        ("TP404", "PRESSURE_OUT", "PRESSURE_OUT", (223.52, 68.58)),
        ("TP405", "ABS_GATE", "ABS_GATE", (261.62, 68.58)),
        ("TP406", "SHAPED_PRESENT", "SHAPED_PRESENT", (299.72, 68.58)),
        ("TP407", "RETURN_FEED", "RETURN_FEED", (337.82, 68.58)),
        ("TP408", "ADC_ANALOG_IN", "ADC_ANALOG_IN", (375.92, 68.58)),
    ):
        add_test_point(sch, reference, value, net, position)

    sch.add_text(
        "No cable: J40 TIP normal contact grounds the input before protection.\n"
        "Plug insertion opens the normal contact and admits the external signal.",
        position=(40.64, 203.20), size=1.27,
    )
    sch.add_text(
        "DIRECT_PRESENT splits after protected AC-coupled unity buffering and before Pressure/Absence.\n"
        "SHAPED_PRESENT contains Pressure plus Return-derived Absence attenuation.",
        position=(40.64, 218.44), size=1.27,
    )
    sch.add_text(
        "ADC_ANALOG_IN = -(SHAPED_PRESENT + RETURN_FEED), unity per input.\n"
        "The inverting sum restores the accepted feedback polarity from the inverting sheet-06 feed.",
        position=(40.64, 233.68), size=1.27,
    )
    sch.add_text(
        "J40/Q40/U40/U41 and diode footprints intentionally blank. JFET VGS(off), jack pin map,\n"
        "Pressure thresholds, Absence law, input surge behaviour and complete loop gain remain gates.",
        position=(40.64, 269.24), size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "04_INPUT_PRESSURE_ABSENCE component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("Direct Present split precedes Pressure and Absence")
    print("Memory sum accepts only SHAPED_PRESENT and fixed RETURN_FEED")


if __name__ == "__main__":
    build()
