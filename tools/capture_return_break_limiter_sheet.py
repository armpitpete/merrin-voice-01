#!/usr/bin/env python3
"""Capture 06_RETURN_BREAK_LIMITER for Memory Core Prototype A.

Implements the accepted Return safety architecture:

RETURN_DAC -> 1/3 normalisation -> SSI2164 channel 3 -> Break ->
analogue Return shaping -> independent +/-2.5 V Schottky clamp ->
RETURN_LIMITED -> fixed 0.6816 Return-feed stage.

The sheet also derives a bounded, fault-neutral ABSENCE_INFLUENCE envelope from
RETURN_LIMITED. The SSI2164 is emitted as a genuine five-unit project symbol so
channel 3 and the common power unit can live on this sheet while channels 1, 2
and 4 remain available to sheet 05. Active-device footprints remain blank.
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

HIER_INPUTS = (
    "RAIL_P12",
    "RAIL_N12",
    "RAIL_3V3",
    "HARDWARE_FAULT_N",
    "RETURN_DAC",
    "VCA_RETURN_CTRL",
)
HIER_OUTPUTS = ("RETURN_LIMITED", "RETURN_FEED", "ABSENCE_INFLUENCE")
ALLOWED_EXPORTS = frozenset(HIER_OUTPUTS)
FIXED_FEED_RIN = 40.2
FIXED_FEED_RF = 27.4
FIXED_FEED_NOMINAL = FIXED_FEED_RF / FIXED_FEED_RIN


def _effects(hidden: bool = False) -> str:
    suffix = " hide" if hidden else ""
    return (
        "\t\t\t(effects\n"
        "\t\t\t\t(font (size 1.27 1.27))\n"
        f"\t\t\t{suffix}\n"
        "\t\t\t)\n"
    )


def _property(name: str, value: str, y: float, hidden: bool = False) -> str:
    return (
        f'\t\t(property "{name}" "{value}"\n'
        f"\t\t\t(at 0 {y} 0)\n"
        f"{_effects(hidden)}"
        "\t\t)\n"
    )


def _render_ssi_unit(name: str, unit: int, pins: tuple[helpers.SymbolPin, ...]) -> str:
    rows = max(pin.row for pin in pins)
    half_height = max(6.35, rows * 1.27 + 1.27)
    out = [
        f'\t\t(symbol "{name}_{unit}_1"\n',
        "\t\t\t(rectangle\n",
        f"\t\t\t\t(start -6.35 {half_height})\n",
        f"\t\t\t\t(end 6.35 {-half_height})\n",
        "\t\t\t\t(stroke (width 0.254) (type default))\n",
        "\t\t\t\t(fill (type background))\n",
        "\t\t\t)\n",
    ]
    for pin in pins:
        y = half_height - 2.54 * pin.row
        x = -10.16 if pin.side == "left" else 10.16
        rotation = 0 if pin.side == "left" else 180
        out.extend(
            [
                f"\t\t\t(pin {pin.pin_type} line\n",
                f"\t\t\t\t(at {x} {y} {rotation})\n",
                "\t\t\t\t(length 3.81)\n",
                f'\t\t\t\t(name "{pin.name}" (effects (font (size 0.762 0.762))))\n',
                f'\t\t\t\t(number "{pin.number}" (effects (font (size 1.016 1.016))))\n',
                "\t\t\t)\n",
            ]
        )
    out.append("\t\t)\n")
    return "".join(out)


def render_ssi2164_multi_symbol() -> str:
    name = "SSI2164S_MULTI"
    units = {
        1: (
            helpers.SymbolPin("2", "IIN1", "input", "left", 1),
            helpers.SymbolPin("3", "VC1", "input", "left", 3),
            helpers.SymbolPin("4", "IOUT1", "output", "right", 2),
        ),
        2: (
            helpers.SymbolPin("7", "IIN2", "input", "left", 1),
            helpers.SymbolPin("6", "VC2", "input", "left", 3),
            helpers.SymbolPin("5", "IOUT2", "output", "right", 2),
        ),
        3: (
            helpers.SymbolPin("15", "IIN3", "input", "left", 1),
            helpers.SymbolPin("14", "VC3", "input", "left", 3),
            helpers.SymbolPin("13", "IOUT3", "output", "right", 2),
        ),
        4: (
            helpers.SymbolPin("10", "IIN4", "input", "left", 1),
            helpers.SymbolPin("11", "VC4", "input", "left", 3),
            helpers.SymbolPin("12", "IOUT4", "output", "right", 2),
        ),
        5: (
            helpers.SymbolPin("1", "MODE", "input", "left", 1),
            helpers.SymbolPin("8", "GND", "power_in", "left", 3),
            helpers.SymbolPin("9", "V-", "power_in", "left", 4),
            helpers.SymbolPin("16", "V+", "power_in", "right", 2),
        ),
    }
    out = [
        f'\t(symbol "{name}"\n',
        "\t\t(exclude_from_sim no)\n",
        "\t\t(in_bom yes)\n",
        "\t\t(on_board yes)\n",
        _property("Reference", "U", 11.43),
        _property("Value", name, -11.43),
        _property("Footprint", "", 0, True),
        _property("Datasheet", "https://www.soundsemiconductor.com/downloads/ssi2164datasheet.pdf", 0, True),
        _property(
            "Description",
            "SSI2164 quad current-in/current-out VCA; five-unit application symbol; official SOP-16 pin map",
            0,
            True,
        ),
    ]
    for unit, pins in units.items():
        out.append(_render_ssi_unit(name, unit, pins))
    out.append("\t)\n")
    return "".join(out)


def append_symbols() -> None:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    additions = []
    if '(symbol "SSI2164S_MULTI"' not in text:
        additions.append(render_ssi2164_multi_symbol())
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


def pin_position(sch, reference, pin):
    point = sch.get_component_pin_position(reference, str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {reference}.{pin}")
    return (point.x, point.y)


def component_pin_position(component, pin):
    point = component.get_pin_position(str(pin))
    if point is None:
        raise RuntimeError(f"Missing pin {component.reference}.{pin} unit {component._data.unit}")
    return (point.x, point.y)


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def label_component_pin(sch, component, pin, net):
    sch.add_label(net, position=component_pin_position(component, pin))


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


def add_upper_clamp(sch, reference, net, position):
    # Device:D_Schottky pin 1 is cathode and pin 2 is anode.
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class upper clamp", position, "RAIL_3V3", net)


def add_lower_clamp(sch, reference, net, position):
    add_two_pin(sch, "Device:D_Schottky", reference, "BAT54-class lower clamp", position, net, "GND")


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
            2: "Active-device, panel-pot and clamp-diode footprints remain blocked pending review.",
        },
    )
    sch.add_text("06 — RETURN / BREAK / LIMITER", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "SSI2164 CH3 • VARIABLE BREAK • UNITY-NORMALISED RETURN • INDEPENDENT ANALOGUE CLAMP",
        position=(20.32, 17.78),
        size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        add_hier(sch, signal, (20.32, y), HierarchicalLabelShape.INPUT, (35.56, y))
        y += 8.89
    y = 30.48
    for signal in HIER_OUTPUTS:
        add_hier(sch, signal, (391.16, y), HierarchicalLabelShape.OUTPUT, (375.92, y))
        y += 17.78

    ground = add_part(sch, "power:GND", "#PWR0601", "GND", (203.20, 284.48))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0601", "1", "GND")

    # Genuine shared SSI2164: official channel 3 is pins 15/14/13.
    ssi_ch3 = add_part(
        sch,
        "MerrinLab_PrototypeA:SSI2164S_MULTI",
        "U60",
        "SSI2164 — RETURN CH3",
        (116.84, 101.60),
        unit=3,
    )
    ssi_power = add_part(
        sch,
        "MerrinLab_PrototypeA:SSI2164S_MULTI",
        "U60",
        "SSI2164 — COMMON POWER",
        (116.84, 139.70),
        unit=5,
    )
    label_component_pin(sch, ssi_ch3, "15", "SSI_IIN3")
    label_component_pin(sch, ssi_ch3, "14", "SSI_VC3")
    label_component_pin(sch, ssi_ch3, "13", "SSI_IOUT3")
    label_component_pin(sch, ssi_power, "8", "GND")
    label_component_pin(sch, ssi_power, "9", "RAIL_N12")
    label_component_pin(sch, ssi_power, "16", "RAIL_P12")
    no_connect_component_pin(sch, ssi_power, "1")  # MODE open = Class AB.

    # Correct sheet-03's ~0.747 receiver to ~0.249 before the Return VCA.
    add_two_pin(sch, "Device:R", "R600", "20k", (58.42, 83.82), "RETURN_DAC", "RETURN_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R601", "10k", (71.12, 91.44), "RETURN_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C600", "10uF AC", (83.82, 83.82), "RETURN_DIV", "RETURN_VCA_AC")
    add_two_pin(sch, "Device:R", "R602", "20k SSI input", (96.52, 83.82), "RETURN_VCA_AC", "SSI_IIN3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R603", "220R stability", (96.52, 96.52), "SSI_IIN3", "SSI_STAB3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C601", "1.2nF stability", (106.68, 96.52), "SSI_STAB3", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # Return control remains in the attenuation-only 0–3.3 V range.
    add_two_pin(sch, "Device:R", "R604", "1k control isolate", (76.20, 114.30), "VCA_RETURN_CTRL", "SSI_VC3", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D600", "SSI_VC3", (91.44, 111.76))
    add_lower_clamp(sch, "D601", "SSI_VC3", (91.44, 116.84))

    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U61", "OPA1679 RETURN AUDIO", (218.44, 127.00))
    add_part(sch, "MerrinLab_PrototypeA:OPA1679_PW_APPLICATION", "U62", "OPA1679 REFERENCES / ABSENCE", (218.44, 238.76))
    for ref in ("U61", "U62"):
        label_pin(sch, ref, "4", "RAIL_P12")
        label_pin(sch, ref, "11", "RAIL_N12")
    for index in range(2):
        x = 55.88 + index * 45.72
        add_two_pin(sch, "Device:C", f"C61{index*4}", "100nF + rail", (x, 251.46), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C61{index*4+1}", "100nF - rail", (x + 10.16, 251.46), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C61{index*4+2}", "4.7uF + rail", (x + 20.32, 251.46), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
        add_two_pin(sch, "Device:C", f"C61{index*4+3}", "4.7uF - rail", (x + 30.48, 251.46), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C618", "100nF SSI + rail", (137.16, 139.70), "RAIL_P12", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C619", "100nF SSI - rail", (149.86, 139.70), "RAIL_N12", "GND", "Capacitor_SMD:C_0805_2012Metric")

    # U61A: SSI2164 current-to-voltage conversion, unity magnitude at VC=0 V.
    label_pin(sch, "U61", "3", "GND")
    label_pin(sch, "U61", "2", "SSI_IOUT3")
    label_pin(sch, "U61", "1", "RETURN_VCA")
    add_two_pin(sch, "Device:R", "R605", "20k I/V", (165.10, 83.82), "RETURN_VCA", "SSI_IOUT3", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C603", "100pF I/V", (177.80, 83.82), "RETURN_VCA", "SSI_IOUT3", "Capacitor_SMD:C_0805_2012Metric")

    # U61B: unity small-signal Break with variable nonlinear feedback.
    add_two_pin(sch, "Device:R", "R610", "20k", (160.02, 111.76), "RETURN_VCA", "BRK_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R611", "20k unity feedback", (182.88, 111.76), "BRK_OUT", "BRK_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C610", "330pF bandwidth", (195.58, 111.76), "BRK_OUT", "BRK_SUM", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U61", "5", "GND")
    label_pin(sch, "U61", "6", "BRK_SUM")
    label_pin(sch, "U61", "7", "BRK_OUT")
    add_two_pin(sch, "Device:D", "D602", "Break diode A", (155.00, 127.00), "BRK_OUT", "BRK_DIODE")
    add_two_pin(sch, "Device:D", "D603", "Break diode B", (167.70, 127.00), "BRK_DIODE", "BRK_OUT")
    add_part(sch, "MerrinLab_PrototypeA:R_POT_123", "RV60", "100k BREAK AMOUNT", (182.88, 127.00))
    label_pin(sch, "RV60", "1", "BRK_DIODE")
    label_pin(sch, "RV60", "2", "BRK_DIODE")
    label_pin(sch, "RV60", "3", "BRK_SUM")

    # U61C: unity small-signal Return shaping with asymmetric nonlinear feedback.
    add_two_pin(sch, "Device:R", "R612", "20k", (160.02, 149.86), "BRK_OUT", "RET_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R613", "20k unity feedback", (182.88, 149.86), "RET_NL_OUT", "RET_SUM", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C611", "390pF bandwidth loss", (195.58, 149.86), "RET_NL_OUT", "RET_SUM", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U61", "10", "GND")
    label_pin(sch, "U61", "9", "RET_SUM")
    label_pin(sch, "U61", "8", "RET_NL_OUT")
    add_two_pin(sch, "Device:R", "R614", "6.8k nonlinear feed", (160.02, 162.56), "RET_NL_OUT", "RET_ASYM_A", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D", "D604", "Asym single", (175.26, 160.02), "RET_SUM", "RET_ASYM_A")
    add_two_pin(sch, "Device:D", "D605", "Asym pair 1", (175.26, 165.10), "RET_ASYM_A", "RET_ASYM_B")
    add_two_pin(sch, "Device:D", "D606", "Asym pair 2", (187.96, 165.10), "RET_ASYM_B", "RET_SUM")

    # Buffered +/-2.5 V clamp references from protected analogue rails.
    add_two_pin(sch, "Device:R", "R620", "38.3k 1%", (248.92, 91.44), "RAIL_P12", "REFP_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R621", "10k 1%", (261.62, 91.44), "REFP_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C620", "1uF", (274.32, 91.44), "REFP_DIV", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U62", "3", "REFP_DIV")
    label_pin(sch, "U62", "2", "REF_P2V5")
    label_pin(sch, "U62", "1", "REF_P2V5")

    add_two_pin(sch, "Device:R", "R622", "38.3k 1%", (248.92, 111.76), "RAIL_N12", "REFN_DIV", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R623", "10k 1%", (261.62, 111.76), "REFN_DIV", "GND", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:C", "C621", "1uF", (274.32, 111.76), "REFN_DIV", "GND", "Capacitor_SMD:C_0805_2012Metric")
    label_pin(sch, "U62", "5", "REFN_DIV")
    label_pin(sch, "U62", "6", "REF_N2V5")
    label_pin(sch, "U62", "7", "REF_N2V5")

    # RET-02: independent current-limited dual-polarity hard clamp and buffer.
    add_two_pin(sch, "Device:R", "R624", "2.2k clamp current", (233.68, 177.80), "RET_NL_OUT", "RET_CLAMP_NODE", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D607", "Upper hard clamp", (248.92, 175.26), "REF_P2V5", "RET_CLAMP_NODE")
    add_two_pin(sch, "Device:D_Schottky", "D608", "Lower hard clamp", (248.92, 180.34), "RET_CLAMP_NODE", "REF_N2V5")
    label_pin(sch, "U61", "12", "RET_CLAMP_NODE")
    label_pin(sch, "U61", "13", "RET_LIM_BUF")
    label_pin(sch, "U61", "14", "RET_LIM_BUF")
    add_two_pin(sch, "Device:R", "R625", "47R output isolate", (286.00, 177.80), "RET_LIM_BUF", "RETURN_LIMITED", "Resistor_SMD:R_0805_2012Metric")

    # U62C: fixed inverting feed; 27.4/40.2 = 0.6816 nominal.
    add_two_pin(sch, "Device:R", "R626", "40.2k 1%", (304.80, 177.80), "RETURN_LIMITED", "RETFEED_SUM", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U62", "10", "GND")
    label_pin(sch, "U62", "9", "RETFEED_SUM")
    label_pin(sch, "U62", "8", "RETURN_FEED")
    add_two_pin(sch, "Device:R", "R627", "27.4k 1%", (327.66, 177.80), "RETURN_FEED", "RETFEED_SUM", "Resistor_SMD:R_0805_2012Metric")

    # RET-03: bounded envelope derived only from RETURN_LIMITED.
    add_two_pin(sch, "Device:R", "R630", "10k rectifier feed", (248.92, 208.28), "RETURN_LIMITED", "ABS_RECT_IN", "Resistor_SMD:R_0805_2012Metric")
    add_two_pin(sch, "Device:D_Schottky", "D609", "Envelope rectifier", (261.62, 208.28), "ABS_ENV_RAW", "ABS_RECT_IN")
    add_two_pin(sch, "Device:C", "C630", "1uF attack/release", (274.32, 208.28), "ABS_ENV_RAW", "GND", "Capacitor_SMD:C_0805_2012Metric")
    add_two_pin(sch, "Device:R", "R631", "100k release", (287.02, 208.28), "ABS_ENV_RAW", "GND", "Resistor_SMD:R_0805_2012Metric")
    label_pin(sch, "U62", "12", "ABS_ENV_RAW")
    label_pin(sch, "U62", "13", "ABS_CTRL_DRV")
    label_pin(sch, "U62", "14", "ABS_CTRL_DRV")
    add_two_pin(sch, "Device:R", "R632", "1k output isolate", (322.58, 208.28), "ABS_CTRL_DRV", "ABSENCE_INFLUENCE", "Resistor_SMD:R_0805_2012Metric")
    add_upper_clamp(sch, "D610", "ABSENCE_INFLUENCE", (337.82, 205.74))
    add_lower_clamp(sch, "D611", "ABSENCE_INFLUENCE", (337.82, 210.82))
    # Active-low fault clamps the control neutral independently of envelope state.
    add_two_pin(sch, "Device:D_Schottky", "D612", "Fault-neutral clamp", (353.06, 208.28), "HARDWARE_FAULT_N", "ABSENCE_INFLUENCE")
    add_two_pin(sch, "Device:R", "R633", "100k neutral pull-down", (368.30, 215.90), "ABSENCE_INFLUENCE", "GND", "Resistor_SMD:R_0805_2012Metric")

    test_points = (
        ("TP600", "RETURN_DAC", "RETURN_DAC", (45.72, 83.82)),
        ("TP601", "RETURN_NORM", "RETURN_DIV", (83.82, 73.66)),
        ("TP602", "RETURN_VCA", "RETURN_VCA", (200.66, 83.82)),
        ("TP603", "BREAK", "BRK_OUT", (210.82, 111.76)),
        ("TP604", "RETURN_NONLINEAR", "RET_NL_OUT", (210.82, 149.86)),
        ("TP605", "+2V5_REF", "REF_P2V5", (287.02, 91.44)),
        ("TP606", "-2V5_REF", "REF_N2V5", (287.02, 111.76)),
        ("TP607", "RETURN_LIMITED", "RETURN_LIMITED", (292.10, 167.64)),
        ("TP608", "RETURN_FEED", "RETURN_FEED", (342.90, 177.80)),
        ("TP609", "ABSENCE_INFLUENCE", "ABSENCE_INFLUENCE", (373.38, 200.66)),
        ("TP610", "SSI_VC3", "SSI_VC3", (106.68, 114.30)),
    )
    for reference, value, net, position in test_points:
        add_part(sch, "Connector:TestPoint", reference, value, position)
        label_pin(sch, reference, "1", net)

    sch.add_text(
        "GAIN CONTRACT\n"
        "sheet-03 Return receiver ~0.747; R600/R601 = 1/3; combined ~0.249.\n"
        "SSI2164 VC3 is restricted to 0…3.3 V, so VCA gain cannot exceed unity.\n"
        "Break and RET-01 are unity at small signal; nonlinear branches alter shape, not linear gain.",
        position=(40.64, 190.50),
        size=1.27,
    )
    sch.add_text(
        "HARD LIMITER\n"
        "R624 limits clamp current. D607/D608 clamp to buffered +/-2.5 V references.\n"
        "Expected first-pass limit ~+/-2.7…2.8 V. Limiter remains analogue and MCU-independent.",
        position=(40.64, 228.60),
        size=1.27,
    )
    sch.add_text(
        f"FIXED FEED: 27.4k / 40.2k = {FIXED_FEED_NOMINAL:.4f} nominal; 1% worst case <0.696.\n"
        "Only RETURN_LIMITED, RETURN_FEED and ABSENCE_INFLUENCE cross this boundary.",
        position=(241.30, 238.76),
        size=1.27,
    )
    sch.add_text(
        "Official SSI2164 channel 3 pins: 15 IIN3, 14 VC3, 13 IOUT3.\n"
        "Pins 10/11/12 are channel 4 and are reserved for the wet-master unit on sheet 05.",
        position=(241.30, 261.62),
        size=1.27,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "06_RETURN_BREAK_LIMITER component-level capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("SSI2164 official channel-3 pins 15/14/13 + power unit captured")


if __name__ == "__main__":
    build()
