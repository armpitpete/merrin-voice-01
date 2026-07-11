#!/usr/bin/env python3
"""Capture 06_RETURN_BREAK_LIMITER for Memory Core Prototype A.

Implements SSI2164 Return VCA channel 3, bounded Break, unity normalisation,
independent buffered +/-2.5 V clamp references, the hard Return limiter,
fixed 0.6816 Return-feed attenuation, and bounded Return-derived Absence
control. Only RETURN_LIMITED, RETURN_FEED and ABSENCE_INFLUENCE leave the
sheet.

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
SHEET_FILE = ROOT / "06_RETURN_BREAK_LIMITER.kicad_sch"
SYMBOL_LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
MARKER = ROOT / "06_RETURN_BREAK_LIMITER_CAPTURED"

POWER_HELPERS = Path(__file__).with_name("capture_power_protection_sheet.py")
SPEC = importlib.util.spec_from_file_location("prototype_a_return_symbol_helpers", POWER_HELPERS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load symbol helpers: {POWER_HELPERS}")
helpers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = helpers
SPEC.loader.exec_module(helpers)

HIER_INPUTS = ("RAIL_P12", "RAIL_N12", "RETURN_DAC", "VCA_RETURN_CTRL")
HIER_OUTPUTS = ("RETURN_LIMITED", "RETURN_FEED", "ABSENCE_INFLUENCE")
ALLOWED_AUDIO_EXPORTS = frozenset(HIER_OUTPUTS)

FIXED_FEED_RIN = "40.2k"
FIXED_FEED_RF = "27.4k"
FIXED_FEED_NOMINAL = 27.4 / 40.2
LIMIT_REFERENCE = "2.5V"
LIMIT_SERIES = "2.2k"

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

SSI_UNITS = {
    1: (("2", "IIN1", "input", "left", 2), ("3", "VC1", "input", "left", 3), ("4", "IOUT1", "output", "right", 2)),
    2: (("7", "IIN2", "input", "left", 2), ("6", "VC2", "input", "left", 3), ("5", "IOUT2", "output", "right", 2)),
    3: (("10", "IIN3", "input", "left", 2), ("11", "VC3", "input", "left", 3), ("12", "IOUT3", "output", "right", 2)),
    4: (("15", "IIN4", "input", "left", 2), ("14", "VC4", "input", "left", 3), ("13", "IOUT4", "output", "right", 2)),
    5: (("1", "MODE", "input", "left", 2), ("8", "GND", "power_in", "left", 4), ("16", "V+", "power_in", "right", 2), ("9", "V-", "power_in", "right", 4)),
}


def _pin_block(number: str, name: str, pin_type: str, side: str, row: int, half_height: float) -> str:
    x = -10.16 if side == "left" else 10.16
    rotation = 0 if side == "left" else 180
    y = half_height - 2.54 * row
    return (
        f"\t\t\t(pin {pin_type} line\n"
        f"\t\t\t\t(at {x} {y} {rotation})\n"
        "\t\t\t\t(length 3.81)\n"
        f"\t\t\t\t(name \"{name}\"\n"
        "\t\t\t\t\t(effects (font (size 0.762 0.762)))\n"
        "\t\t\t\t)\n"
        f"\t\t\t\t(number \"{number}\"\n"
        "\t\t\t\t\t(effects (font (size 1.016 1.016)))\n"
        "\t\t\t\t)\n"
        "\t\t\t)\n"
    )


def render_ssi2164_multi_unit() -> str:
    name = "SSI2164S_APPLICATION"
    half_height = 7.62
    out = [
        f'\t(symbol "{name}"\n',
        "\t\t(exclude_from_sim no)\n",
        "\t\t(in_bom yes)\n",
        "\t\t(on_board yes)\n",
        helpers.property_block("Reference", "U", half_height + 2.54),
        helpers.property_block("Value", name, -(half_height + 2.54)),
        helpers.property_block("Footprint", "", 0, True),
        helpers.property_block("Datasheet", "https://www.soundsemiconductor.com/downloads/ssi2164datasheet.pdf", 0, True),
        helpers.property_block("Description", "SSI2164 quad current-in/current-out VCA; five schematic units; SOP-16 footprint pending", 0, True),
    ]
    for unit, pins in SSI_UNITS.items():
        out.extend([
            f'\t\t(symbol "{name}_{unit}_1"\n',
            "\t\t\t(rectangle\n",
            f"\t\t\t\t(start -6.35 {half_height})\n",
            f"\t\t\t\t(end 6.35 {-half_height})\n",
            "\t\t\t\t(stroke (width 0.254) (type default))\n",
            "\t\t\t\t(fill (type background))\n",
            "\t\t\t)\n",
        ])
        for pin in pins:
            out.append(_pin_block(*pin, half_height))
        out.append("\t\t)\n")
    out.append("\t)\n")
    return "".join(out)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    if '(symbol "OPA1679_PW_APPLICATION"' not in text:
        additions.append(helpers.render_symbol(OPA1679))
    if '(symbol "SSI2164S_APPLICATION"' not in text:
        additions.append(render_ssi2164_multi_unit())
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
    raise RuntimeError("06_RETURN_BREAK_LIMITER sheet not found")


def add_part(sch, lib_id, reference, value, position, footprint="", unit=1):
    return sch.components.add(
        lib_id=lib_id,
        reference=reference,
        value=value,
        position=position,
        footprint=footprint,
        unit=unit,
    )


def component_pin_position(component, pin):
    point = component.get_pin_position(str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {component.reference}.{pin} unit {component._data.unit}")
    return (point.x, point.y)


def label_component_pin(sch, component, pin, net):
    sch.add_label(net, position=component_pin_position(component, pin))


def pin_position(sch, reference, pin):
    point = sch.get_component_pin_position(reference, str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def no_connect_component_pin(sch, component, pin):
    sch.no_connects.add(position=component_pin_position(component, pin))


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
        title="Memory Core Prototype A — Return / Break / Limiter",
        rev="V5.2 component capture 06",
        company="MerrinLab",
        comments={
            1: "Only RETURN_LIMITED, RETURN_FEED and ABSENCE_INFLUENCE may leave this sheet.",
            2: "SSI2164/op-amp/diode footprints remain blocked pending independent review.",
        },
    )
    sch.add_text("06 — RETURN / BREAK / LIMITER", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "SSI2164 RETURN VCA • BOUNDED BREAK • INDEPENDENT HARD CLAMP • FIXED FEED",
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

    ground = add_part(sch, "power:GND", "#PWR0601", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0601", "1", "GND")

    # SSI2164 unit C is Return channel 3; unit E owns MODE and power pins.
    ssi_return = add_part(
        sch, "MerrinLab_PrototypeA:SSI2164S_APPLICATION", "U50", "SSI2164 RETURN CH3",
        (91.44, 91.44), unit=3,
    )
    ssi_power = add_part(
        sch, "MerrinLab_PrototypeA:SSI2164S_APPLICATION", "U50", "SSI2164 POWER",
        (91.44, 129.54), unit=5,
    )
    for pin, net in (("10", "SSI_IIN3"), ("11", "VCA_RETURN_CTRL"), ("12", "SSI_IOUT3")):
        label_component_pin(sch, ssi_return, pin, net)
    for pin, net in (("8", "GND"), ("16", "RAIL_P12"), ("9", "RAIL_N12")):
        label_component_pin(sch, ssi_power, pin, net)
    no_connect_component_pin(sch, ssi_power, "1")  # MODE open = Class AB.

    add_two_pin(sch, "Device:R", "R600", "20k input", (60.96, 83.82), "RETURN_DAC", "SSI_IIN3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R601", "220R stability", (60.96, 96.52), "SSI_IIN3", "SSI_RC3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C600", "1.2nF stability", (73.66, 96.52), "SSI_RC3", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C601", "100nF V+", (73.66, 139.70), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C602", "100nF V-", (86.36, 139.70), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Two quad op amps implement the accepted eight Return functions.
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U60", "OPA1679 RETURN A", (195.58, 177.80))
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U61", "OPA1679 RETURN B", (312.42, 177.80))
    for ref in ("U60", "U61"):
        label_pin(sch, ref, "4", "RAIL_P12")
        label_pin(sch, ref, "11", "RAIL_N12")
    for index, ref in enumerate(("U60", "U61")):
        x = 116.84 + index * 45.72
        add_two_pin(sch, "Device:C", f"C60{3 + index * 4}", "100nF + rail", (x, 246.38), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C60{4 + index * 4}", "100nF - rail", (x + 12.70, 246.38), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C60{5 + index * 4}", "4.7uF + rail", (x + 25.40, 246.38), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C60{6 + index * 4}", "4.7uF - rail", (x + 38.10, 246.38), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U60A: required current-output I/V stage, unity when VC3 = 0 V.
    label_pin(sch, "U60", "3", "GND")
    label_pin(sch, "U60", "2", "SSI_IOUT3")
    label_pin(sch, "U60", "1", "RETURN_VCA")
    add_two_pin(sch, "Device:R", "R602", "20k I/V", (121.92, 83.82), "RETURN_VCA", "SSI_IOUT3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C611", "100pF I/V", (134.62, 83.82), "RETURN_VCA", "SSI_IOUT3", "Capacitor_SMD:C_0805_2012Metric")

    # U60B: inverting unity Break stage with bounded soft clipping and bandwidth loss.
    add_two_pin(sch, "Device:R", "R603", "22k Break input", (121.92, 111.76), "RETURN_VCA", "BREAK_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U60", "5", "GND")
    label_pin(sch, "U60", "6", "BREAK_SUM")
    label_pin(sch, "U60", "7", "BREAK_OUT")
    add_two_pin(sch, "Device:R", "R604", "22k Break feedback", (147.32, 111.76), "BREAK_OUT", "BREAK_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C612", "1nF Break blur", (160.02, 111.76), "BREAK_OUT", "BREAK_SUM", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:D", "D600", "BAV199-class soft clip", (147.32, 124.46), "BREAK_OUT", "BREAK_SUM")
    add_two_pin(sch, "Device:D", "D601", "BAV199-class soft clip", (160.02, 124.46), "BREAK_SUM", "BREAK_OUT")

    # U60C: unity gain normaliser; Break + normaliser small-signal magnitude <= 1.
    add_two_pin(sch, "Device:R", "R605", "22k normalise input", (182.88, 111.76), "BREAK_OUT", "RET_NORM_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U60", "10", "GND")
    label_pin(sch, "U60", "9", "RET_NORM_SUM")
    label_pin(sch, "U60", "8", "RETURN_NORM")
    add_two_pin(sch, "Device:R", "R606", "22k normalise feedback", (208.28, 111.76), "RETURN_NORM", "RET_NORM_SUM", "Resistor_SMD:R_0805_2012Metric")

    # U60D/U61A: buffered independent clamp references from protected +/-12 V.
    add_two_pin(sch, "Device:R", "R607", "38k +ref top", (121.92, 162.56), "RAIL_P12", "REF_P_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R608", "10k +ref bottom", (134.62, 162.56), "REF_P_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C613", "1uF +ref", (147.32, 162.56), "REF_P_DIV", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U60", "12", "REF_P_DIV")
    label_pin(sch, "U60", "13", "REF_P2V5")
    label_pin(sch, "U60", "14", "REF_P2V5")

    add_two_pin(sch, "Device:R", "R609", "38k -ref top", (238.76, 162.56), "RAIL_N12", "REF_N_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R610", "10k -ref bottom", (251.46, 162.56), "REF_N_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C614", "1uF -ref", (264.16, 162.56), "REF_N_DIV", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U61", "3", "REF_N_DIV")
    label_pin(sch, "U61", "2", "REF_N2V5")
    label_pin(sch, "U61", "1", "REF_N2V5")

    # Independent dual-polarity hard clamp followed by U61B buffer.
    add_two_pin(sch, "Device:R", "R611", LIMIT_SERIES, (238.76, 96.52), "RETURN_NORM", "RETURN_CLAMP", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D602", "BAT54-class high clamp", (251.46, 88.90), "REF_P2V5", "RETURN_CLAMP")
    add_two_pin(sch, "Device:D_Schottky", "D603", "BAT54-class low clamp", (251.46, 104.14), "RETURN_CLAMP", "REF_N2V5")
    label_pin(sch, "U61", "5", "RETURN_CLAMP")
    label_pin(sch, "U61", "6", "RETURN_LIMITED")
    label_pin(sch, "U61", "7", "RETURN_LIMITED")

    # U61C: fixed inverting feed. SUM-01 is also inverting, preserving loop polarity.
    add_two_pin(sch, "Device:R", "R612", FIXED_FEED_RIN, (292.10, 96.52), "RETURN_LIMITED", "RETFEED_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U61", "10", "GND")
    label_pin(sch, "U61", "9", "RETFEED_SUM")
    label_pin(sch, "U61", "8", "RETURN_FEED")
    add_two_pin(sch, "Device:R", "R613", FIXED_FEED_RF, (317.50, 96.52), "RETURN_FEED", "RETFEED_SUM", "Resistor_SMD:R_0805_2012Metric")

    # U61D: precision positive envelope, slow smoothing and bounded 0-3 V control.
    label_pin(sch, "U61", "12", "RETURN_LIMITED")
    label_pin(sch, "U61", "13", "ABS_RECT")
    label_pin(sch, "U61", "14", "ABS_RECT_DRIVE")
    add_two_pin(sch, "Device:D_Schottky", "D604", "BAT54-class precision rectifier", (330.20, 139.70), "ABS_RECT", "ABS_RECT_DRIVE")
    add_two_pin(sch, "Device:R", "R614", "10k attack", (342.90, 139.70), "ABS_RECT", "ABSENCE_INFLUENCE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C615", "4.7uF release", (355.60, 147.32), "ABSENCE_INFLUENCE", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R615", "220k release", (368.30, 147.32), "ABSENCE_INFLUENCE", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Zener", "D605", "3.0V control clamp provisional", (380.00, 147.32), "ABSENCE_INFLUENCE", "GND")

    for reference, value, net, position in (
        ("TP600", "RETURN_DAC", "RETURN_DAC", (55.88, 68.58)),
        ("TP601", "RETURN_VCA", "RETURN_VCA", (116.84, 68.58)),
        ("TP602", "BREAK_OUT", "BREAK_OUT", (172.72, 68.58)),
        ("TP603", "RETURN_NORM", "RETURN_NORM", (228.60, 68.58)),
        ("TP604", "+2V5_REF", "REF_P2V5", (238.76, 177.80)),
        ("TP605", "-2V5_REF", "REF_N2V5", (251.46, 177.80)),
        ("TP606", "RETURN_LIMITED", "RETURN_LIMITED", (279.40, 68.58)),
        ("TP607", "RETURN_FEED", "RETURN_FEED", (330.20, 68.58)),
        ("TP608", "ABSENCE_INFLUENCE", "ABSENCE_INFLUENCE", (375.92, 129.54)),
        ("TP609", "VCA_RETURN_CTRL", "VCA_RETURN_CTRL", (111.76, 129.54)),
    ):
        add_test_point(sch, reference, value, net, position)

    sch.add_text(
        "SSI2164 CH3: pins 10 IIN3, 11 VC3, 12 IOUT3. MODE pin 1 open = Class AB.\n"
        "Current output is converted by U60A; it is not treated as a voltage output.",
        position=(40.64, 203.20), size=1.27,
    )
    sch.add_text(
        "Clamp references +/-2.5 V plus Schottky Vf give approximately 5.4-5.6 Vpp RETURN_LIMITED.\n"
        "Fixed feed magnitude = 27.4k / 40.2k = 0.6816; 1% worst case < 0.696.",
        position=(40.64, 218.44), size=1.27,
    )
    sch.add_text(
        "Small-signal path: SSI VCA <= unity; Break = -1; normaliser = -1.\n"
        "Only RETURN_LIMITED, RETURN_FEED and bounded ABSENCE_INFLUENCE cross this sheet.",
        position=(40.64, 233.68), size=1.27,
    )
    sch.add_text(
        "U50/U60/U61 and clamp-diode footprints intentionally blank. Exact diode leakage/Vf,\n"
        "reference source/sink current, measured loop gain and 30-minute endurance remain gates.",
        position=(40.64, 269.24), size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "06_RETURN_BREAK_LIMITER component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print(f"Fixed feed nominal magnitude: {FIXED_FEED_NOMINAL:.6f}")
    print("SSI2164 channel 3 and power units encoded")


if __name__ == "__main__":
    build()
