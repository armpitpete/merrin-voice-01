# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
01_POWER_PROTECTION COMPONENT CAPTURE COMPLETE
COMMITTED POWER SHEET ERC VALIDATED
OTHER COMPONENT-LEVEL SHEETS IN PROGRESS
08_CONTROLS_STATE NEXT
PCB WORK BLOCKED
```

This folder contains the native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

The hierarchy establishes the accepted sheet boundaries and cross-sheet signals. Component-level circuitry is being added one sheet at a time, with KiCad ERC run after each bounded capture.

It must not yet be described as a completed hardware schematic or production-ready design.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch       CAPTURED / ERC VALIDATED
├── 02_MCU_CLOCK_DEBUG.kicad_sch        INTERFACE SCAFFOLD
├── 03_CODEC_CONVERSION.kicad_sch       INTERFACE SCAFFOLD
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch INTERFACE SCAFFOLD
├── 05_MEMORY_GHOST_WET.kicad_sch       INTERFACE SCAFFOLD
├── 06_RETURN_BREAK_LIMITER.kicad_sch   INTERFACE SCAFFOLD
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD
├── 08_CONTROLS_STATE.kicad_sch         NEXT CAPTURE
└── 09_TEST_SERVICE.kicad_sch           INTERFACE SCAFFOLD
```

## Accepted interface constraints

- Direct Present remains outside the digital core.
- Memory captures shaped Present after Pressure and Absence.
- PCM3168A conversion uses one ADC ingress and three DAC roles: Memory, Ghost and Return send.
- Return passes through Break, analogue Return shaping and the independent limiter boundary.
- The Return sheet may export feedback audio only as `RETURN_LIMITED` and the fixed `RETURN_FEED` derived from it.
- `ABSENCE_INFLUENCE` is a bounded control output derived from limited Return.
- `WATCHDOG_HEARTBEAT` enters the power/protection and hardware-fault system.
- TMUX1574 safe-control release remains a controls/safety-sheet responsibility.

The machine-readable interface list is stored in `hierarchy-manifest.json`.

## Captured sheet 01 — Power / Protection

`01_POWER_PROTECTION.kicad_sch` now contains real component-level circuitry rather than a temporary interface harness.

Captured functions:

- protected positive and negative 12 V rail entry;
- provisional input current limiting, reverse-polarity protection and ferrite filtering;
- 3.293 V TPS62160 digital regulator;
- 5.453 V TPS62160 codec preregulator;
- TPS7A2050 quiet 5 V codec-analogue regulator;
- TPS3808G33 3.3 V supervision and manual reset;
- TPS3431 independent watchdog;
- active-low open-drain `HARDWARE_FAULT_N` combination;
- required rail, fault and watchdog test points;
- explicit schematic power-source annotations after passive protection and conversion boundaries.

### Sheet 01 validation

The component-level sheet was generated, parsed and checked under pinned KiCad CLI 10.0.4.

The capture passed the current stage policy:

```text
0 ERC errors
no temporary interface-harness warnings on 01_POWER_PROTECTION
```

During ERC repair, the following real findings were corrected rather than suppressed:

1. the stock KiCad ferrite symbol name was corrected;
2. a supervisor timing resistor overlap was removed;
3. downstream rails received explicit source annotations after passive boundaries;
4. a redundant quiet-5-V source annotation was removed because the LDO output already drives that rail.

### Sheet 01 boundary

The following remain deliberately open:

- active-device footprints;
- exact orderable inductor and capacitor parts;
- capacitor DC-bias derating;
- copper-dependent thermal calculations;
- exact power-input connector and final format;
- final fuse, protection-diode and ferrite-bead selections;
- TPS3431 VSON land-pattern and assembly verification.

The project-local TI symbols use the accepted manufacturer pin maps. Their footprints are intentionally blank until the independent footprint gate.

No sheet-01 choice authorises PCB work or purchasing.

## ERC policy

The schematic is checked with:

```text
KiCad CLI 10.0.4
official KiCad CI container
pinned container digest
```

Current staged-capture policy:

```text
0 ERC errors required
isolated_pin_label warnings allowed only on sheets that remain temporary scaffolds
captured sheets may not retain temporary interface-harness warnings
```

The remaining `isolated_pin_label` warnings belong only to uncaptured sheets 02–09. They come from temporary non-BOM, non-board interface harness symbols that keep hierarchical labels electrically attached until actual circuitry replaces them.

They are not accepted permanent exceptions.

As each sheet receives its real circuit:

1. remove that sheet's temporary interface harness;
2. connect every hierarchical label to the actual circuit;
3. rerun full hierarchical ERC;
4. correct real electrical findings;
5. document any unavoidable intentional exception;
6. do not permit new warning classes silently.

The finished component-level schematic must pass ERC with no unexplained errors or warnings.

## Active capture order

```text
[x] 01_POWER_PROTECTION
[ ] 08_CONTROLS_STATE       NEXT
[ ] 02_MCU_CLOCK_DEBUG
[ ] 03_CODEC_CONVERSION
[ ] 06_RETURN_BREAK_LIMITER
[ ] 04_INPUT_PRESSURE_ABSENCE
[ ] 05_MEMORY_GHOST_WET
[ ] 07_OUTPUT_MUTE_PROTECTION
[ ] 09_TEST_SERVICE
[ ] 00_TOP final interface and ERC review
```

Power and independent fault behaviour are captured first. The next sheet implements the MCP4728, TMUX1574 fail-safe control selection, panel control acquisition and SLS-1 state outputs before the MCU and audio sheets depend on them.

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
