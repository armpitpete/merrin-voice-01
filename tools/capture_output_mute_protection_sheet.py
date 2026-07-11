#!/usr/bin/env python3
"""Capture 07_OUTPUT_MUTE_PROTECTION for Memory Core Prototype A.

The sheet consumes Direct Present and the bounded wet mix, forms an equal
half-sum, provides a passive output-level control, implements a fail-muted
JFET shunt with hardware-fault control, and drives a protected mono output.
U32 units B/C/D are the final three channels of the single physical OPA1679
already represented by unit A and the power unit on sheet 03.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import kicad_sch_api as ksa

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP = ROOT / f"{PROJECT}.kicad_sch"
SHEET_FILE = ROOT / "07_OUTPUT_MUTE_PROTECTION.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "07_OUTPUT_MUTE_PROTECTION_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SUPPORT_PATH = Path(__file__).with_name("opa1679_multi_support.py")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


helpers = load("output_symbol_helpers", POWER_HELPERS)
support = load("opa1679_multi_support", SUPPORT_PATH)

HIER_INPUTS = (
    "RAIL_P12",
    "RAIL_N12",
    "DIRECT_PRESENT",
    "WET_MIX",
    "HARDWARE_FAULT_N",
)
HIER_OUTPUTS: tuple[str, ...] = ()
ALLOWED_EXPORTS = frozenset()

OPA_REFERENCE = "U32"
OPA_UNITS = {
    2: {"plus": "5", "minus": "6", "out": "7", "role": "FINAL HALF-SUM"},
    3: {"plus": "10", "minus": "9", "out": "8", "role": "OUTPUT LEVEL BUFFER"},
    4: {"plus": "12", "minus": "13", "out": "14", "role": "POST-MUTE DRIVER"},
}
OPA_POSITIONS = {
    2: (116.84, 101.60),
    3: (213.36, 101.60),
    4: (309.88, 101.60),
}

SUM_INPUT_KOHM = 40.2
SUM_FEEDBACK_KOHM = 20.0
SUM_BRANCH_GAIN = SUM_FEEDBACK_KOHM / SUM_INPUT_KOHM
MAX_INPUT_VPP = 6.0
MAX_CALCULATED_MIX_VPP = 2 * SUM_BRANCH_GAIN * MAX_INPUT_VPP
OUTPUT_LEVEL_KOHM = 10.0
MUTE_NEGATIVE_REFERENCE_V = -12.0
MUTE_NEGATIVE_PULL_KOHM = 100.0
MUTE_GROUND_PULL_KOHM = 1000.0
MUTE_CAP_UF = 1.0
MUTE_GATE_STEADY_V = MUTE_NEGATIVE_REFERENCE_V * (
    MUTE_GROUND_PULL_KOHM / (MUTE_NEGATIVE_PULL_KOHM + MUTE_GROUND_PULL_KOHM)
)
MUTE_RELEASE_TAU_MS = (
    (MUTE_NEGATIVE_PULL_KOHM * MUTE_GROUND_PULL_KOHM)
    / (MUTE_NEGATIVE_PULL_KOHM + MUTE_GROUND_PULL_KOHM)
    * MUTE_CAP_UF
)
FAULT_PULLUP_KOHM = 2.2
OPTO_LED_RESISTOR_KOHM = 3.3
OPTO_LED_FORWARD_V = 1.2
OPTO_LED_CURRENT_MA = (12.0 - OPTO_LED_FORWARD_V) / (
    FAULT_PULLUP_KOHM + OPTO_LED_RESISTOR_KOHM
)
MUTE_NEGATIVE_PULL_CURRENT_MA = abs(MUTE_NEGATIVE_REFERENCE_V) / MUTE_NEGATIVE_PULL_KOHM
MIN_ASSUMED_OPTO_COLLECTOR_MA = 0.5 * OPTO_LED_CURRENT_MA
CALCULATED_FAULT_CLAMP_MS = (
    abs(MUTE_GATE_STEADY_V) * MUTE_CAP_UF
    / (MIN_ASSUMED_OPTO_COLLECTOR_MA - MUTE_NEGATIVE_PULL_CURRENT_MA)
)

OPTO = helpers.SymbolDefinition(
    "LTV817S_MUTE_APPLICATION",
    "LTV-817S-class optocoupler used for fail-muted JFET gate control; SO-4 pin map; footprint pending",
    "https://optoelectronics.liteon.com/upload/download/DS70-2009-0014/LTV-8X7%20series%20201606.pdf",
    (
        helpers.SymbolPin("1", "LED_A", "input", "left", 1),
        helpers.SymbolPin("2", "LED_K", "passive", "left", 3),
        helpers.SymbolPin("3", "EMITTER", "passive", "right", 3),
        helpers.SymbolPin("4", "COLLECTOR", "passive", "right", 1),
    ),
)


def append_symbols() -> None:
    support.append_symbol_library(SYMBOL_LIBRARY)
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    if f'(symbol "{OPTO.name}"' in text:
        return
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    SYMBOL_LIBRARY.write_text(
        stripped[:-1] + helpers.render_symbol(OPTO) + ")\n",
        encoding="utf-8",
    )


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("07_OUTPUT_MUTE_PROTECTION sheet not found")


def add_part(sch, lib_id, reference, value, position, footprint="", unit=1):
    return sch.components.add(
        lib_id=lib_id,
        reference=reference,
        value=value,
        position=position,
        footprint=footprint,
        unit=unit,
    )


def pin_position(sch, reference, pin):
    point = sch.get_component_pin_position(reference, str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def component_pin_position(component, pin):
    point = component.get_pin_position(str(pin))
    if point is None:
        raise RuntimeError(
            f"Missing pin {component.reference}.{pin} unit {component._data.unit}"
        )
    return (point.x, point.y)


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def label_component_pin(sch, component, pin, net):
    sch.add_label(net, position=component_pin_position(component, pin))


def add_two_pin(sch, lib_id, reference, value, position, net1, net2, footprint=""):
    add_part(sch, lib_id, reference, value, position, footprint)
    label_pin(sch, reference, "1", net1)
    label_pin(sch, reference, "2", net2)


def add_hier(sch, name, position, end):
    sch.add_hierarchical_label(name, position=position, shape="input", size=1.27)
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
        title="Memory Core Prototype A — Output / Mute / Protection",
        rev="V5.2 component capture 07",
        company="MerrinLab",
        comments={
            1: "U32 units B/C/D complete the physical OPA1679 whose A/power units remain on sheet 03.",
            2: "Output jack and active-device footprints remain blocked pending independent review.",
        },
    )
    sch.add_text("07 — OUTPUT / MUTE / PROTECTION", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "DIRECT + WET HALF-SUM • OUTPUT LEVEL • FAIL-MUTED JFET • PROTECTED MONO OUT",
        position=(20.32, 17.78),
        size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        add_hier(sch, signal, (20.32, y), (35.56, y))
        y += 10.16

    ground = add_part(sch, "power:GND", "#PWR0701", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0701", "1", "GND")

    opa = {}
    for unit in (2, 3, 4):
        opa[unit] = add_part(
            sch,
            support.LIB_ID,
            OPA_REFERENCE,
            support.VALUE,
            OPA_POSITIONS[unit],
            unit=unit,
        )
        pins = OPA_UNITS[unit]
        sch.add_text(
            f"U32{chr(64 + unit)} {pins['role']}: pins {pins['plus']} +, {pins['minus']} -, {pins['out']} OUT",
            position=(OPA_POSITIONS[unit][0] - 15.24, OPA_POSITIONS[unit][1] + 15.24),
            size=0.9,
        )

    # U32B: equal half-sum. Two maximum 6 Vpp inputs calculate to <6 Vpp.
    add_two_pin(sch, "Device:R", "R700", "40.2k 1% Direct sum", (58.42, 83.82), "DIRECT_PRESENT", "FINAL_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R701", "40.2k 1% Wet sum", (58.42, 99.06), "WET_MIX", "FINAL_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    label_component_pin(sch, opa[2], "5", "GND")
    label_component_pin(sch, opa[2], "6", "FINAL_SUM_NODE")
    label_component_pin(sch, opa[2], "7", "FINAL_MIX")
    add_two_pin(sch, "Device:R", "R702", "20k 1% half-sum feedback", (139.70, 83.82), "FINAL_MIX", "FINAL_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C700", "220pF mix bandwidth", (152.40, 83.82), "FINAL_MIX", "FINAL_SUM_NODE", "Capacitor_SMD:C_0805_2012Metric")

    # Passive output-level attenuator followed by U32C unity buffer.
    add_part(sch, "Device:R_Potentiometer", "RV700", "10k A OUTPUT LEVEL", (180.34, 124.46))
    label_pin(sch, "RV700", "1", "GND")
    label_pin(sch, "RV700", "2", "OUTPUT_LEVEL")
    label_pin(sch, "RV700", "3", "FINAL_MIX")
    label_component_pin(sch, opa[3], "10", "OUTPUT_LEVEL")
    label_component_pin(sch, opa[3], "9", "OUT_PREMUTE")
    label_component_pin(sch, opa[3], "8", "OUT_PREMUTE")

    # Fail-muted shunt. Healthy HARDWARE_FAULT_N saturates Q71 and keeps the
    # optocoupler dark. Fault/undefined logic lights U70, which clamps the JFET
    # gate toward 0 V. The negative RC path gives a controlled healthy release.
    add_two_pin(sch, "Device:R", "R703", "10k mute isolation", (233.68, 124.46), "OUT_PREMUTE", "MUTE_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_part(sch, "MerrinLab_PrototypeA:J113_SHUNT_APPLICATION", "Q70", "J113 OUTPUT MUTE SHUNT", (264.16, 147.32))
    label_pin(sch, "Q70", "1", "MUTE_NODE")
    label_pin(sch, "Q70", "2", "MUTE_GATE")
    label_pin(sch, "Q70", "3", "GND")

    add_two_pin(sch, "Device:R", "R711", "10k fault inverter base", (91.44, 198.12), "HARDWARE_FAULT_N", "FAULT_INV_BASE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R712", "100k fault base pull-down", (106.68, 213.36), "FAULT_INV_BASE", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_part(sch, "Transistor_BJT:Q_NPN_BCE", "Q71", "MMBT3904 fault inverter provisional", (132.08, 198.12))
    label_pin(sch, "Q71", "1", "FAULT_INV_BASE")
    label_pin(sch, "Q71", "2", "MUTE_FAULT_HIGH")
    label_pin(sch, "Q71", "3", "GND")
    add_two_pin(sch, "Device:R", "R713", "2.2k +12V fault pull-up", (154.94, 182.88), "RAIL_P12", "MUTE_FAULT_HIGH", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R714", "3.3k optocoupler LED", (170.18, 198.12), "MUTE_FAULT_HIGH", "MUTE_LED_A", "Resistor_SMD:R_0805_2012Metric")
    add_part(sch, "MerrinLab_PrototypeA:LTV817S_MUTE_APPLICATION", "U70", "LTV-817S-CLASS FAIL-MUTE", (203.20, 198.12))
    label_pin(sch, "U70", "1", "MUTE_LED_A")
    label_pin(sch, "U70", "2", "GND")
    label_pin(sch, "U70", "3", "MUTE_GATE")
    label_pin(sch, "U70", "4", "GND")
    add_two_pin(sch, "Device:R", "R715", "100k controlled release", (238.76, 182.88), "RAIL_N12", "MUTE_GATE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R716", "1M power-off mute", (254.00, 198.12), "MUTE_GATE", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C710", "1uF mute ramp", (269.24, 198.12), "MUTE_GATE", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U32D buffers the muted node. Output is AC-coupled, current-limited,
    # rail-clamped and RF-referenced before the logical WQP518MA jack symbol.
    label_component_pin(sch, opa[4], "12", "MUTE_NODE")
    label_component_pin(sch, opa[4], "13", "POST_MUTE")
    label_component_pin(sch, opa[4], "14", "POST_MUTE")
    add_two_pin(sch, "Device:C", "C720", "10uF bipolar output AC", (330.20, 124.46), "POST_MUTE", "OUTPUT_AC")
    add_two_pin(sch, "Device:R", "R720", "1k output protection", (350.52, 124.46), "OUTPUT_AC", "OUTPUT_TIP", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R721", "100k output reference", (350.52, 144.78), "OUTPUT_TIP", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C721", "220pF output RF", (365.76, 144.78), "OUTPUT_TIP", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D701", "BAT54-class +rail clamp", (350.52, 162.56), "OUTPUT_TIP", "RAIL_P12")
    add_two_pin(sch, "Device:D_Schottky", "D702", "BAT54-class -rail clamp", (365.76, 162.56), "RAIL_N12", "OUTPUT_TIP")

    add_part(sch, "MerrinLab_PrototypeA:WQP518MA_APPLICATION", "J70", "WQP518MA / THONKICONN OUTPUT", (386.08, 124.46))
    label_pin(sch, "J70", "1", "OUTPUT_TIP")
    sch.no_connects.add(position=pin_position(sch, "J70", "2"))
    label_pin(sch, "J70", "3", "GND")

    # Local rail decoupling for output, mute and protection circuitry. U32's
    # physical package decoupling remains beside its power unit on sheet 03.
    add_two_pin(sch, "Device:C", "C730", "100nF + rail", (58.42, 248.92), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C731", "100nF - rail", (73.66, 248.92), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C732", "4.7uF + rail", (88.90, 248.92), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C733", "4.7uF - rail", (104.14, 248.92), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    for reference, value, net, position in (
        ("TP700", "FINAL_MIX", "FINAL_MIX", (142.24, 68.58)),
        ("TP701", "OUT_PREMUTE", "OUT_PREMUTE", (223.52, 68.58)),
        ("TP702", "OUTPUT_TIP", "OUTPUT_TIP", (365.76, 68.58)),
        ("TP703", "MUTE_GATE", "MUTE_GATE", (274.32, 175.26)),
    ):
        add_test_point(sch, reference, value, net, position)

    sch.add_text(
        "SHARED OPA1679 CONTRACT\n"
        "U32 unit 1 + power unit 5 remain on sheet 03.\n"
        "U32 units 2/3/4 implement final half-sum, level buffer and post-mute driver here.\n"
        "Exactly seven physical OPA1679 packages remain in Prototype A.",
        position=(40.64, 223.52),
        size=1.05,
    )
    sch.add_text(
        f"OUTPUT GAIN CONTRACT\n"
        f"R700 = R701 = {SUM_INPUT_KOHM:.1f}k; R702 = {SUM_FEEDBACK_KOHM:.1f}k.\n"
        f"Each branch = {SUM_BRANCH_GAIN:.4f}; two {MAX_INPUT_VPP:.1f} Vpp inputs calculate to {MAX_CALCULATED_MIX_VPP:.2f} Vpp.\n"
        "The 10k output control only attenuates; normal output remains below 10 Vpp.",
        position=(177.80, 223.52),
        size=1.05,
    )
    sch.add_text(
        f"FAIL-MUTE CONTRACT\n"
        f"Fault/undefined HARDWARE_FAULT_N lights U70 and clamps MUTE_GATE toward 0 V.\n"
        f"Healthy release approaches {MUTE_GATE_STEADY_V:.2f} V from RAIL_N12 with about {MUTE_RELEASE_TAU_MS:.1f} ms RC time constant.\n"
        f"At 50% assumed CTR, the first-pass fault-clamp estimate is {CALCULATED_FAULT_CLAMP_MS:.1f} ms; exact optocoupler/JFET parts remain a later measured gate.",
        position=(294.64, 223.52),
        size=1.05,
    )
    sch.add_text(
        "BOUNDARY\n"
        "All mix, level, mute, output-protection and jack nodes remain local to sheet 07.\n"
        "No audio or control net is exported from this sheet; physical jack/footprint acceptance remains blocked.",
        position=(218.44, 269.24),
        size=1.05,
    )

    sch.save(str(SHEET_FILE))
    text = SHEET_FILE.read_text(encoding="utf-8")
    for name, unit, pin in (
        ("GND", 2, "5"),
        ("FINAL_SUM_NODE", 2, "6"),
        ("FINAL_MIX", 2, "7"),
        ("OUTPUT_LEVEL", 3, "10"),
        ("OUT_PREMUTE", 3, "9"),
        ("OUT_PREMUTE", 3, "8"),
        ("MUTE_NODE", 4, "12"),
        ("POST_MUTE", 4, "13"),
        ("POST_MUTE", 4, "14"),
    ):
        text = support.repair_label(text, name, OPA_POSITIONS[unit], unit, pin)
    SHEET_FILE.write_text(text, encoding="utf-8")

    MARKER.write_text(
        "07_OUTPUT_MUTE_PROTECTION component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("U32 units 2/3/4 placed on sheet 07; units 1/5 remain on sheet 03")


if __name__ == "__main__":
    build()
