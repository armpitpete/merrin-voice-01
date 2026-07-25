#!/usr/bin/env python3
"""Allow only the proven coincident same-net labels in the SSI2164 lane validator.

The generated sheet intentionally places the OPA4196 non-inverting input label at
the same physical coordinate as the associated filter-capacitor pin label for the
Memory and Ghost channels. KiCad serialises both attached labels. This patch
changes only the validator's expected multiplicity for those two coordinates;
all other exact-coordinate checks continue to require one label record.
"""

from __future__ import annotations

from pathlib import Path

VALIDATOR_PATH = Path("tools/validate_ssi2164_buffer_lane.py")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one validator match, found {count}: {old!r}")
    return text.replace(old, new, 1)


def main() -> None:
    text = VALIDATOR_PATH.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "def assert_label_at(text: str, name: str, x: float, y: float) -> None:\n",
        '''COINCIDENT_LABEL_COUNTS = {
    ("MEM_CTRL_BUFFER_IN", 91.44, 107.95): 2,
    ("GHOST_CTRL_BUFFER_IN", 91.44, 161.29): 2,
}


def assert_label_at(text: str, name: str, x: float, y: float) -> None:
''',
    )
    text = replace_once(
        text,
        "    assert count == 1, (name, x, y, count)\n",
        '''    expected_count = COINCIDENT_LABEL_COUNTS.get((name, x, y), 1)
    assert count == expected_count, (name, x, y, expected_count, count)
''',
    )

    VALIDATOR_PATH.write_text(text, encoding="utf-8")
    print("Validator multiplicity updated for two proven coincident OPA4196 input junctions")


if __name__ == "__main__":
    main()
