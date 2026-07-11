#!/usr/bin/env python3
"""Capture 05_MEMORY_GHOST_WET for Memory Core Prototype A.

Moves the real SSI2164 channel ownership for Memory, Ghost and wet master onto
sheet 05 while preserving U60 as the single physical five-unit device shared
with sheet 06. The accepted signal route is:

MEMORY_DAC -> SSI2164 CH1 -> I/V
GHOST_DAC  -> SSI2164 CH2 -> I/V
                         -> equal half-sum -> SSI2164 CH4 wet master -> WET_MIX

Only WET_MIX may leave this sheet. Active-device footprints remain blank.
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
SHEET_FILE = ROOT / "05_MEMORY_GHOST_WET.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "05_MEMORY_GHOST_WET_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_wet_symbol_helpers", POWER_HELPERS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_HELPERS}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

HIER_INPUTS = (
    "RAIL_P12",
    "RAIL_N12",
    "MEMORY_DAC",
    "GHOST_DAC",
    "VCA_MEMORY_CTRL",
    "VCA_GHOST_CTRL",
    "VCA_WET_CTRL",
)
HIER_OUTPUTS = ("WET_MIX",)
ALLOWED_EXPORTS = frozenset(HIER_OUTPUTS)

SSI_REFERENCE = "U60"
SSI_LIBRARY_ID = "MerrinLab_PrototypeA:SSI2164S_MULTI"
SSI_CHANNEL_PINS = {
    1: {"iin": "2", "vc": "3", "iout": "4", "role": "MEMORY"},
    2: {"iin": "7", "vc": "6", "iout": "5", "role": "GHOST"},
    4: {"iin": "10", "vc": "11", "iout": "12", "role": "WET MASTER"},
}

VCA_INPUT_KOHM = 20.0
VCA_IV_KOHM = 20.0
SUM_INPUT_KOHM = 40.2
SUM_FEEDBACK_KOHM = 20.0
SUM_BRANCH_GAIN = SUM_FEEDBACK_KOHM / SUM_INPUT_KOHM


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("05_MEMORY_GHOST_WET sheet not found")


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


def add_hier(sch, name, position, shape, end):
    sch.add_hierarchical_label(name, position=position, shape=shape, size=1.27)
    sch.add_wire(start=position, end=end)
    sch.add_label(name, position=end)


def add_test_point(sch, reference, value, net, position):
    add_part(sch, "Connector:TestPoint", reference, value, position)
    label_pin(sch, reference, "1", net)


def build() -> None:
    cache = ksa.get_symbol_cache()
    cache.add_library_path(str(SYMBOL_LIBRARY.resolve()))

    top = ksa.load_schematic(str(TOP))
    parent_uuid, sheet_uuid = find_sheet_context(top)
    sch = ksa.create_schematic(PROJECT)
    sch.set_hierarchy_context(parent_uuid, sheet_uuid)
    sch.set_paper_size("A3")
    sch.set_title_block(
        title="Memory Core Prototype A — Memory / Ghost / Wet",
        rev="V5.2 component capture 05",
        company="MerrinLab",
        comments={
            1: "U60 units 1, 2 and 4 share the physical SSI2164 with units 3 and 5 on sheet 06.",
            2: "Only WET_MIX may leave this sheet; active-device footprints remain blocked.",
        },
    )
    sch.add_text("05 — MEMORY / GHOST / WET", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "SSI2164 CH1 MEMORY • CH2 GHOST • EQUAL HALF-SUM • CH4 WET MASTER",
        position=(20.32, 17.78),
        size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        add_hier(sch, signal, (20.32, y), HierarchicalLabelShape.INPUT, (35.56, y))
        y += 8.89
    add_hier(
        sch,
        "WET_MIX",
        (391.16, 30.48),
        HierarchicalLabelShape.OUTPUT,
        (375.92, 30.48),
    )

    ground = add_part(sch, "power:GND", "#PWR0501", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0501", "1", "GND")

    memory = add_part(
        sch,
        SSI_LIBRARY_ID,
        SSI_REFERENCE,
        "SSI2164 — MEMORY CH1",
        (116.84, 83.82),
        unit=1,
    )
    ghost = add_part(
        sch,
        SSI_LIBRARY_ID,
        SSI_REFERENCE,
        "SSI2164 — GHOST CH2",
        (116.84, 137.16),
        unit=2,
    )
    wet = add_part(
        sch,
        SSI_LIBRARY_ID,
        SSI_REFERENCE,
        "SSI2164 — WET MASTER CH4",
        (276.86, 111.76),
        unit=4,
    )

    for component, unit, prefix, position in (
        (memory, 1, "MEM", (116.84, 83.82)),
        (ghost, 2, "GHOST", (116.84, 137.16)),
        (wet, 4, "WET", (276.86, 111.76)),
    ):
        pins = SSI_CHANNEL_PINS[unit]
        label_component_pin(sch, component, pins["iin"], f"SSI_IIN{unit}")
        label_component_pin(sch, component, pins["vc"], f"SSI_VC{unit}")
        label_component_pin(sch, component, pins["iout"], f"SSI_IOUT{unit}")
        sch.add_text(
            f"{prefix}: pins {pins['iin']} IIN{unit}, {pins['vc']} VC{unit}, {pins['iout']} IOUT{unit}",
            position=(position[0] - 12.70, position[1] + 15.24),
            size=0.9,
        )

    add_part(
        sch,
        "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION",
        "U50",
        "OPA1679 MEMORY/GHOST/WET",
        (213.36, 177.80),
    )
    label_pin(sch, "U50", "4", "RAIL_P12")
    label_pin(sch, "U50", "11", "RAIL_N12")

    add_two_pin(sch, "Device:C", "C500", "10uF AC", (58.42, 83.82), "MEMORY_DAC", "MEMORY_VCA_AC")
    add_two_pin(sch, "Device:R", "R500", "20k SSI input", (76.20, 83.82), "MEMORY_VCA_AC", "SSI_IIN1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R501", "220R stability", (91.44, 96.52), "SSI_IIN1", "SSI_STAB1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C501", "1.2nF stability", (104.14, 96.52), "SSI_STAB1", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R502", "1k control isolate", (76.20, 111.76), "VCA_MEMORY_CTRL", "SSI_VC1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C502", "100nF control filter", (91.44, 111.76), "SSI_VC1", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U50", "3", "GND")
    label_pin(sch, "U50", "2", "SSI_IOUT1")
    label_pin(sch, "U50", "1", "MEMORY_VCA")
    add_two_pin(sch, "Device:R", "R503", "20k I/V", (157.48, 83.82), "MEMORY_VCA", "SSI_IOUT1", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C503", "100pF I/V", (170.18, 83.82), "MEMORY_VCA", "SSI_IOUT1", "Capacitor_SMD:C_0805_2012Metric")

    add_two_pin(sch, "Device:C", "C504", "10uF AC", (58.42, 137.16), "GHOST_DAC", "GHOST_VCA_AC")
    add_two_pin(sch, "Device:R", "R504", "20k SSI input", (76.20, 137.16), "GHOST_VCA_AC", "SSI_IIN2", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R505", "220R stability", (91.44, 149.86), "SSI_IIN2", "SSI_STAB2", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C505", "1.2nF stability", (104.14, 149.86), "SSI_STAB2", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R506", "1k control isolate", (76.20, 165.10), "VCA_GHOST_CTRL", "SSI_VC2", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C506", "100nF control filter", (91.44, 165.10), "SSI_VC2", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U50", "5", "GND")
    label_pin(sch, "U50", "6", "SSI_IOUT2")
    label_pin(sch, "U50", "7", "GHOST_VCA")
    add_two_pin(sch, "Device:R", "R507", "20k I/V", (157.48, 137.16), "GHOST_VCA", "SSI_IOUT2", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C507", "100pF I/V", (170.18, 137.16), "GHOST_VCA", "SSI_IOUT2", "Capacitor_SMD:C_0805_2012Metric")

    add_two_pin(sch, "Device:R", "R510", "40.2k 1% Memory sum", (190.50, 96.52), "MEMORY_VCA", "WET_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R511", "40.2k 1% Ghost sum", (190.50, 111.76), "GHOST_VCA", "WET_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U50", "10", "GND")
    label_pin(sch, "U50", "9", "WET_SUM_NODE")
    label_pin(sch, "U50", "8", "WET_SUM")
    add_two_pin(sch, "Device:R", "R512", "20k 1% half-sum feedback", (228.60, 111.76), "WET_SUM", "WET_SUM_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C510", "220pF sum bandwidth", (241.30, 111.76), "WET_SUM", "WET_SUM_NODE", "Capacitor_SMD:C_0805_2012Metric")

    add_two_pin(sch, "Device:C", "C520", "10uF AC", (246.38, 137.16), "WET_SUM", "WET_MASTER_AC")
    add_two_pin(sch, "Device:R", "R520", "20k SSI input", (261.62, 137.16), "WET_MASTER_AC", "SSI_IIN4", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R521", "220R stability", (284.48, 137.16), "SSI_IIN4", "SSI_STAB4", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C521", "1.2nF stability", (297.18, 137.16), "SSI_STAB4", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R522", "1k control isolate", (261.62, 157.48), "VCA_WET_CTRL", "SSI_VC4", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C522", "100nF control filter", (276.86, 157.48), "SSI_VC4", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U50", "12", "GND")
    label_pin(sch, "U50", "13", "SSI_IOUT4")
    label_pin(sch, "U50", "14", "WET_MASTER_OUT")
    add_two_pin(sch, "Device:R", "R523", "20k I/V", (322.58, 111.76), "WET_MASTER_OUT", "SSI_IOUT4", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C523", "100pF I/V", (335.28, 111.76), "WET_MASTER_OUT", "SSI_IOUT4", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R524", "47R output isolate", (353.06, 111.76), "WET_MASTER_OUT", "WET_MIX", "Resistor_SMD:R_0805_2012Metric")

    add_two_pin(sch, "Device:C", "C530", "100nF + rail", (73.66, 228.60), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C531", "100nF - rail", (88.90, 228.60), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C532", "4.7uF + rail", (104.14, 228.60), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C533", "4.7uF - rail", (119.38, 228.60), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    for reference, value, net, position in (
        ("TP500", "MEMORY_DAC", "MEMORY_DAC", (45.72, 83.82)),
        ("TP501", "MEMORY_VCA", "MEMORY_VCA", (180.34, 76.20)),
        ("TP502", "GHOST_DAC", "GHOST_DAC", (45.72, 137.16)),
        ("TP503", "GHOST_VCA", "GHOST_VCA", (180.34, 129.54)),
        ("TP504", "WET_SUM", "WET_SUM", (233.68, 96.52)),
        ("TP505", "WET_MIX", "WET_MIX", (368.30, 104.14)),
        ("TP506", "SSI_VC1", "SSI_VC1", (106.68, 111.76)),
        ("TP507", "SSI_VC2", "SSI_VC2", (106.68, 165.10)),
        ("TP508", "SSI_VC4", "SSI_VC4", (292.10, 157.48)),
    ):
        add_test_point(sch, reference, value, net, position)

    sch.add_text(
        "SHARED DEVICE CONTRACT\n"
        "U60 unit 1 = Memory (2 IIN1, 3 VC1, 4 IOUT1).\n"
        "U60 unit 2 = Ghost (7 IIN2, 6 VC2, 5 IOUT2).\n"
        "U60 unit 4 = wet master (10 IIN4, 11 VC4, 12 IOUT4).\n"
        "U60 units 3 and 5 remain on sheet 06; no second SSI2164 is created.",
        position=(40.64, 190.50),
        size=1.1,
    )
    sch.add_text(
        f"WET SUM CONTRACT\n"
        f"R510 = R511 = {SUM_INPUT_KOHM:.1f}k; R512 = {SUM_FEEDBACK_KOHM:.1f}k.\n"
        f"Each branch magnitude = {SUM_BRANCH_GAIN:.4f}; two equal full-scale branches ~= 0.995 total.\n"
        "VCA controls are bounded and fail-safe-selected on sheet 08; sheet 05 adds isolation/filtering only.",
        position=(218.44, 205.74),
        size=1.1,
    )
    sch.add_text(
        "BOUNDARY\n"
        "Memory, Ghost, wet-sum, SSI current nodes and controls remain local.\n"
        "Only WET_MIX crosses the sheet-05 hierarchy boundary.",
        position=(218.44, 246.38),
        size=1.1,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "05_MEMORY_GHOST_WET component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("U60 units 1/2/4 placed on sheet 05; units 3/5 remain on sheet 06")


if __name__ == "__main__":
    build()
