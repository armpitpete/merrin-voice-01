# SSI2164 buffered-control edit contract

## Goal

Correct the SSI2164 control-voltage loading error by inserting one dedicated OPA4196 quad unity-gain buffer between the TMUX1574 filtered control nodes and the four SSI2164 control inputs.

The implemented control law must preserve:

```text
0.00 V at SSI VC  = unity
3.30 V at SSI VC  = approximately -100 dB attenuation
negative SSI VC   = forbidden
```

## Base authority

```text
main commit                  8df52377de753c8c910d67fc31405782d52a1be8
Lane 02 jack authority       CLOSED
PCB / panel / purchasing     BLOCKED
```

## Selected architecture

```text
buffer                         OPA4196 quad operational amplifier
supply                         protected +/-12 V
configuration                  four unity-gain followers
package target                 PW / TSSOP-14
footprint assignment           BLOCKED pending exact footprint review
local supply bypass            100 nF from each supply pin to ground
post-buffer isolation          20 ohm per channel
post-buffer clamps             retained at 0 V and +3.3 V boundaries
SSI local series links         0 ohm
```

The OPA4196 is separate from the seven-package OPA1679 audio allocation.

## Allowed files

- `docs/v5.2-ssi2164-mcp4728-fail-safe-control.md`
- `docs/v5.2-power-current-and-thermal-budget.md`
- `docs/v5.2-return-limiter-and-opamp-allocation.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_EDIT_CONTRACT.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_CONTROL_REVIEW.md`
- `hardware/memory-core-prototype-a/SSI2164_BUFFER_AUDIT.json`
- `hardware/memory-core-prototype-a/MerrinLab_PrototypeA.kicad_sym`
- `hardware/memory-core-prototype-a/05_MEMORY_GHOST_WET.kicad_sch`
- `hardware/memory-core-prototype-a/06_RETURN_BREAK_LIMITER.kicad_sch`
- `hardware/memory-core-prototype-a/08_CONTROLS_STATE.kicad_sch`
- `hardware/memory-core-prototype-a/05_MEMORY_GHOST_WET_VALIDATION.md`
- `hardware/memory-core-prototype-a/06_RETURN_BREAK_LIMITER_VALIDATION.md`
- `tools/capture_memory_ghost_wet_sheet.py`
- `tools/capture_return_break_limiter_sheet.py`
- `tools/capture_controls_state_sheet.py`
- `tools/validate_ssi2164_buffer_lane.py`
- one dedicated read-only GitHub Actions workflow for this lane

## Forbidden changes

- no SSI2164 footprint assignment;
- no OPA4196 footprint assignment;
- no OPA1679 package or decoupling changes;
- no Return limiter/clamp-diode exact-part selection;
- no PCB creation, placement or routing;
- no panel CAD or fabrication;
- no purchasing or production authority;
- no unrelated schematic changes;
- no merge without independent exact-head review.

## Expected electrical diff

1. Add one OPA4196 quad buffer to sheet 08.
2. Keep TMUX1574 safe selection and pre-buffer 1 kΩ / 10 nF filtering.
3. Buffer each filtered control node at unity gain.
4. Add 20 Ω post-buffer isolation per channel.
5. Place the existing 0 V / +3.3 V clamps after the buffer.
6. Change the four downstream SSI control-series resistors from 1 kΩ to 0 Ω links.
7. Preserve all four SSI2164 control-pin and channel assignments.

## Checks

```text
python tools/validate_ssi2164_buffer_lane.py
python tools/validate_current_schematic_stage.py
KiCad 10 hierarchical ERC
```

## Stop rule

Stop immediately if:

- the exact SSI2164 VC voltage cannot be proven within the accepted range;
- the OPA4196 symbol or package identity is ambiguous;
- the controlled generators and generated sheets disagree;
- ERC or any existing validation fails;
- an unlisted file must change;
- PCB, panel, purchasing or production authority would be required.
