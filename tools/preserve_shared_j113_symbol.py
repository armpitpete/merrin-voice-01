#!/usr/bin/env python3
"""Preserve sheet-04's generic J113 beside sheet-07's exact MMBFJ113.

The sheet-07 amendment adds an exact project-library definition. Sheet 04 still
legitimately references the older generic J113 symbol at Gate A. This step
restores that definition from sheet 04 and removes accidental duplicate exact
definitions. It is deterministic and idempotent.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path("hardware/memory-core-prototype-a")
LIBRARY = ROOT / "MerrinLab_PrototypeA.kicad_sym"
SHEET04 = ROOT / "04_INPUT_PRESSURE_ABSENCE.kicad_sch"
GENERIC = "J113_SHUNT_APPLICATION"
EXACT = "MMBFJ113_APPLICATION"


def balanced_block(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise RuntimeError(f"Unterminated S-expression at {start}")


def project_blocks(text: str, name: str) -> list[tuple[int, str]]:
    marker = f'\t(symbol "{name}"'
    rows = []
    offset = 0
    while True:
        found = text.find(marker, offset)
        if found == -1:
            return rows
        start = found + 1
        block = balanced_block(text, start)
        rows.append((found, block))
        offset = start + len(block)


def embedded_generic() -> str:
    text = SHEET04.read_text(encoding="utf-8")
    marker = f'\t\t(symbol "MerrinLab_PrototypeA:{GENERIC}"'
    found = text.index(marker)
    start = found + 2
    block = balanced_block(text, start)
    block = block.replace(
        f'(symbol "MerrinLab_PrototypeA:{GENERIC}"',
        f'(symbol "{GENERIC}"',
        1,
    )
    return "".join(
        line[1:] if line.startswith("\t") else line
        for line in block.splitlines(keepends=True)
    )


def remove_named(text: str, name: str) -> tuple[str, list[str]]:
    rows = project_blocks(text, name)
    blocks = [block for _start, block in rows]
    for start, block in reversed(rows):
        text = text[:start] + text[start + 1 + len(block):]
    return text, blocks


def append_blocks(text: str, blocks: list[str]) -> str:
    stripped = text.rstrip()
    if not stripped.endswith(")"):
        raise RuntimeError("Project symbol library does not end correctly")
    body = stripped[:-1]
    for block in blocks:
        body += "\t" + block + "\n"
    return body + ")\n"


def main() -> None:
    for required in (LIBRARY, SHEET04):
        if not required.exists():
            raise SystemExit(f"Missing required file: {required}")

    text = LIBRARY.read_text(encoding="utf-8")
    text, exact_blocks = remove_named(text, EXACT)
    if not exact_blocks:
        raise RuntimeError("Exact MMBFJ113 library definition was not produced")
    exact = exact_blocks[0]

    text, _generic_blocks = remove_named(text, GENERIC)
    generic = embedded_generic()
    text = append_blocks(text, [exact, generic])
    LIBRARY.write_text(text, encoding="utf-8")

    check = LIBRARY.read_text(encoding="utf-8")
    assert len(project_blocks(check, EXACT)) == 1
    assert len(project_blocks(check, GENERIC)) == 1
    print("Exact MMBFJ113 and shared generic J113 library definitions: PASS")


if __name__ == "__main__":
    main()
