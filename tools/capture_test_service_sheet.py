#!/usr/bin/env python3
"""Capture 09_TEST_SERVICE for Memory Core Prototype A.

The sheet is deliberately read-only. It collects the eight accepted hierarchy
signals through current-limited probe branches, individual test points and a
logical service header. It does not create service commands, panel controls,
production connector authority, current-measurement links or accepted footprints.
"""

from __future__ import annotations

from pathlib import Path

import kicad_sch_api as ksa

PROJECT = "MerrinGriefSynthMemoryCoreA"
ROOT = Path("hardware/memory-core-prototype-a")
TOP = ROOT / f"{PROJECT}.kicad_sch"
SHEET_FILE = ROOT / "09_TEST_SERVICE.kicad_sch"
MARKER = ROOT / "09_TEST_SERVICE_CAPTURED"

HIER_INPUTS = (
    "RAIL_3V3",
    "HARDWARE_FAULT_N",
    "SHAPED_PRESENT",
    "ADC_ANALOG_IN",
    "RETURN_LIMITED",
    "RETURN_FEED",
    "ABSENCE_INFLUENCE",
    "WET_MIX",
)
HIER_OUTPUTS: tuple[str, ...] = ()
ALLOWED_EXPORTS = frozenset()

PROBE_BRANCHES = (
    ("RAIL_3V3", "RAIL_3V3_PROBE", "R900", "1k rail short-limit"),
    ("HARDWARE_FAULT_N", "HARDWARE_FAULT_N_PROBE", "R901", "47k safety-state isolate"),
    ("SHAPED_PRESENT", "SHAPED_PRESENT_PROBE", "R902", "22k analogue probe isolate"),
    ("ADC_ANALOG_IN", "ADC_ANALOG_IN_PROBE", "R903", "22k analogue probe isolate"),
    ("RETURN_LIMITED", "RETURN_LIMITED_PROBE", "R904", "22k analogue probe isolate"),
    ("RETURN_FEED", "RETURN_FEED_PROBE", "R905", "22k analogue probe isolate"),
    ("ABSENCE_INFLUENCE", "ABSENCE_INFLUENCE_PROBE", "R906", "22k analogue probe isolate"),
    ("WET_MIX", "WET_MIX_PROBE", "R907", "22k analogue probe isolate"),
)

HEADER_PIN_NETS = {
    "1": "GND",
    "2": "RAIL_3V3_PROBE",
    "3": "HARDWARE_FAULT_N_PROBE",
    "4": "SHAPED_PRESENT_PROBE",
    "5": "ADC_ANALOG_IN_PROBE",
    "6": "RETURN_LIMITED_PROBE",
    "7": "RETURN_FEED_PROBE",
    "8": "ABSENCE_INFLUENCE_PROBE",
    "9": "WET_MIX_PROBE",
    "10": "GND",
}


def find_sheet_context(top: ksa.Schematic) -> tuple[str, str]:
    for sheet in top._data.get("sheets", []):
        if sheet.get("filename") == SHEET_FILE.name:
            return top.uuid, sheet["uuid"]
    raise RuntimeError("09_TEST_SERVICE sheet not found")


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


def label_pin(sch, reference, pin, net):
    sch.add_label(net, position=pin_position(sch, reference, pin))


def add_two_pin(sch, reference, value, position, net1, net2):
    add_part(
        sch,
        "Device:R",
        reference,
        value,
        position,
        "Resistor_SMD:R_0805_2012Metric",
    )
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
    top = ksa.load_schematic(str(TOP))
    parent_uuid, sheet_uuid = find_sheet_context(top)
    sch = ksa.create_schematic(PROJECT)
    sch.set_hierarchy_context(parent_uuid, sheet_uuid)
    sch.set_paper_size("A3")
    sch.set_title_block(
        title="Memory Core Prototype A — Test / Service",
        rev="V5.2 component capture 09",
        company="MerrinLab",
        comments={
            1: "Read-only service access. No service command or panel function is created here.",
            2: "Header/pads and footprints remain blocked pending fixture and physical review.",
        },
    )
    sch.add_text("09 — TEST / SERVICE", position=(20.32, 12.70), size=2.54)
    sch.add_text(
        "READ-ONLY PROBE ISOLATION • TEST POINTS • LOGICAL SERVICE HEADER",
        position=(20.32, 17.78),
        size=1.27,
    )

    y = 30.48
    for signal in HIER_INPUTS:
        add_hier(sch, signal, (20.32, y), (35.56, y))
        y += 10.16

    ground = add_part(sch, "power:GND", "#PWR0901", "GND", (203.20, 251.46))
    ground.in_bom = False
    ground.on_board = False
    label_pin(sch, "#PWR0901", "1", "GND")

    branch_y = 35.56
    test_y = 35.56
    for index, (source, probe, reference, value) in enumerate(PROBE_BRANCHES):
        add_two_pin(sch, reference, value, (96.52, branch_y), source, probe)
        add_test_point(
            sch,
            f"TP{900 + index}",
            probe,
            probe,
            (139.70, test_y),
        )
        branch_y += 20.32
        test_y += 20.32

    add_test_point(sch, "TP908", "SERVICE_GND", "GND", (139.70, 198.12))

    header = add_part(
        sch,
        "Connector_Generic:Conn_01x10",
        "J90",
        "LOGICAL SERVICE PROBE HEADER / PADS",
        (223.52, 104.14),
        "",
    )
    header.in_bom = True
    header.on_board = True
    for pin, net in HEADER_PIN_NETS.items():
        label_pin(sch, "J90", pin, net)

    sch.add_text(
        "SERVICE HEADER LOGICAL PIN MAP\n"
        "1 GND • 2 +3V3 probe • 3 hardware-fault probe • 4 shaped Present\n"
        "5 ADC analogue in • 6 Return limited • 7 Return feed\n"
        "8 Absence influence • 9 wet mix • 10 GND",
        position=(190.50, 45.72),
        size=1.05,
    )
    sch.add_text(
        "PROBE-ISOLATION CONTRACT\n"
        "+3V3 uses 1 kΩ: accidental ground short is limited to about 3.3 mA.\n"
        "HARDWARE_FAULT_N uses 47 kΩ so service access cannot strongly drive the safety net.\n"
        "Analogue probes use 22 kΩ; a 10 MΩ instrument adds under 0.22% loading.",
        position=(190.50, 157.48),
        size=1.05,
    )
    sch.add_text(
        "BOUNDARY\n"
        "All eight hierarchy signals are read-only inputs. No hierarchy output is created.\n"
        "SERVICE_TEST, RESET_CLEAR and SAFE_MUTE remain operating inputs between sheets 08 and 02.\n"
        "SWD remains on sheet 02. Power-branch current links remain a later sheet-01 physical gate.\n"
        "J90 is a logical header/pad grouping only; connector, fixture and footprint are not accepted.",
        position=(35.56, 223.52),
        size=1.05,
    )

    sch.save(str(SHEET_FILE))
    MARKER.write_text(
        "09_TEST_SERVICE read-only service capture generated and awaiting/holding ERC evidence.\n",
        encoding="utf-8",
    )
    print(f"Captured {SHEET_FILE}")
    print("Eight read-only probe branches, nine test points and one logical blank-footprint header placed")


if __name__ == "__main__":
    build()
