#!/usr/bin/env python3
"""Prepare the committed native hierarchy for the final 00_TOP review.

The pinned schematic API accepted but did not serialise non-input hierarchy
shapes on several early child-sheet generators. This amendment reconciles every
child hierarchical label to the committed manifest, removes stale hierarchy-
capture authority from the top sheet and manifest, and writes a marker that is
promoted only after the final integration validator and KiCad ERC pass.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
MANIFEST = ROOT / "hierarchy-manifest.json"
TOP = ROOT / "MerrinGriefSynthMemoryCoreA.kicad_sch"
MARKER = ROOT / "00_TOP_FINAL_REVIEW_COMPLETE"


def replace_once(text: str, old: str, new: str, description: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {description}, found {count}")
    return text.replace(old, new, 1)


def repair_label_shape(text: str, name: str, required: str) -> tuple[str, bool]:
    pattern = (
        rf'(\(hierarchical_label "{re.escape(name)}"\s+\(shape )'
        rf'([^)]+)(\))'
    )
    matches = list(re.finditer(pattern, text, re.MULTILINE))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one hierarchical label {name}, found {len(matches)}"
        )
    current = matches[0].group(2)
    if current == required:
        return text, False
    repaired = re.sub(
        pattern,
        rf"\g<1>{required}\g<3>",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return repaired, True


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("stage") != "hierarchy-and-interface-capture":
        raise RuntimeError(f"Unexpected pre-review manifest stage: {manifest.get('stage')}")
    if manifest.get("temporary_interface_harnesses") is not True:
        raise RuntimeError("Expected stale temporary-interface authority before amendment")

    changes: list[tuple[str, int]] = []
    for sheet in manifest["sheets"]:
        path = ROOT / sheet["filename"]
        text = path.read_text(encoding="utf-8")
        count = 0
        for pin in sheet["pins"]:
            text, changed = repair_label_shape(text, pin["name"], pin["direction"])
            count += int(changed)
        if count:
            path.write_text(text, encoding="utf-8")
            changes.append((path.name, count))

    top = TOP.read_text(encoding="utf-8")
    top = replace_once(
        top,
        '(rev "V5.2 native hierarchy capture")',
        '(rev "V5.2 integrated schematic review")',
        "top-sheet revision",
    )
    top = replace_once(
        top,
        '(text "Hierarchy/interface capture. Detailed circuits replace temporary harnesses sheet by sheet."',
        '(text "All nine component sheets captured. Final integrated interface and ERC review."',
        "top-sheet status annotation",
    )
    TOP.write_text(top, encoding="utf-8")

    manifest["stage"] = "component-capture-complete"
    manifest["temporary_interface_harnesses"] = False
    manifest["component_sheets_captured"] = True
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    MARKER.write_text(
        "00_TOP integrated interface candidate generated; promoted only after final validators and KiCad ERC pass.\n",
        encoding="utf-8",
    )

    print(f"Reconciled child hierarchy directions: {changes}")
    print("Top-sheet and manifest authority advanced to component-capture-complete")


if __name__ == "__main__":
    main()
