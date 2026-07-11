# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
INTERFACES VALIDATED
COMPONENT-LEVEL CIRCUITS NOT YET COMPLETE
PCB WORK BLOCKED
```

This folder contains the first native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

The hierarchy is a structural and interface artifact. It establishes the accepted sheet boundaries and cross-sheet signals before detailed component-level schematic capture.

It must not be described as a completed hardware schematic or production-ready design.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch
├── 02_MCU_CLOCK_DEBUG.kicad_sch
├── 03_CODEC_CONVERSION.kicad_sch
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch
├── 05_MEMORY_GHOST_WET.kicad_sch
├── 06_RETURN_BREAK_LIMITER.kicad_sch
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch
├── 08_CONTROLS_STATE.kicad_sch
└── 09_TEST_SERVICE.kicad_sch
```

## Accepted interface constraints

- Direct Present remains outside the digital core.
- Memory captures shaped Present after Pressure and Absence.
- PCM3168A conversion uses one ADC ingress and three DAC roles: Memory, Ghost and Return send.
- Return passes through Break, analogue Return shaping and the independent limiter boundary.
- The Return sheet may export feedback audio only as `RETURN_LIMITED` and the separately fixed `RETURN_FEED` derived from it.
- `ABSENCE_INFLUENCE` is a bounded control output derived from limited Return.
- `WATCHDOG_HEARTBEAT` enters the power/protection and hardware-fault system.
- TMUX1574 safe-control release remains a controls/safety-sheet responsibility.

The machine-readable interface list is stored in `hierarchy-manifest.json`.

## ERC status

The hierarchy was generated and checked with:

```text
KiCad CLI 10.0.4
Official KiCad CI container
Pinned image digest
```

Current hierarchy policy:

```text
0 ERC errors required
only isolated_pin_label warnings allowed
```

The remaining `isolated_pin_label` warnings come from temporary non-BOM, non-board interface harness symbols inside the child sheets. These harnesses keep hierarchical labels electrically attached before actual circuitry replaces them.

They are not accepted permanent exceptions for the finished schematic.

As each sheet receives its real circuit:

1. remove that sheet's temporary interface harness;
2. connect every hierarchical label to the actual circuit;
3. rerun full ERC;
4. document any intentional exception;
5. do not permit new warning classes silently.

The finished component-level schematic must pass ERC with no unexplained errors or warnings.

## Next capture order

The safest component-level sequence is:

```text
1. 01_POWER_PROTECTION
2. 08_CONTROLS_STATE
3. 02_MCU_CLOCK_DEBUG
4. 03_CODEC_CONVERSION
5. 06_RETURN_BREAK_LIMITER
6. 04_INPUT_PRESSURE_ABSENCE
7. 05_MEMORY_GHOST_WET
8. 07_OUTPUT_MUTE_PROTECTION
9. 09_TEST_SERVICE
10. 00_TOP final interface and ERC review
```

This order establishes power and fail-safe behaviour before audio paths depend on them.

## Still blocked

- PCB placement
- PCB routing
- fabrication outputs
- parts purchasing
- production pricing
- final mechanical layout
- oscillator or internal voice-source work
- MIDI/CV expansion
- sequencer work
- demo media

## Gate before PCB work

PCB work may begin only after:

- all nine sheets contain accepted component-level circuitry;
- hierarchical ERC passes;
- every symbol pin and package is verified;
- exact footprints receive independent review;
- WQP518MA mechanical alignment is proven;
- Return safety receives schematic-stage independent review;
- remaining hardware risks are closed or transferred to explicit bounded bench tests.
