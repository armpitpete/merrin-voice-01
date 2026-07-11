# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
01_POWER_PROTECTION COMPONENT CAPTURE COMPLETE
08_CONTROLS_STATE COMPONENT CAPTURE COMPLETE
COMMITTED SHEETS ERC VALIDATED
02_MCU_CLOCK_DEBUG NEXT
PCB WORK BLOCKED
```

This folder contains the native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

The hierarchy establishes the accepted sheet boundaries and cross-sheet signals. Component-level circuitry is being added one sheet at a time, with full hierarchical ERC run after each bounded capture.

It must not yet be described as a completed hardware schematic or production-ready design.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch       CAPTURED / ERC VALIDATED
├── 02_MCU_CLOCK_DEBUG.kicad_sch        NEXT CAPTURE
├── 03_CODEC_CONVERSION.kicad_sch       INTERFACE SCAFFOLD
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch INTERFACE SCAFFOLD
├── 05_MEMORY_GHOST_WET.kicad_sch       INTERFACE SCAFFOLD
├── 06_RETURN_BREAK_LIMITER.kicad_sch   INTERFACE SCAFFOLD
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD
├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED
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
- Eight panel controls and three operating inputs are explicit signals between sheets 08 and 02.
- Global ground is established from sheet 01 and shared by captured sheets.

The machine-readable interface list is stored in `hierarchy-manifest.json`.

## Captured sheet 01 — Power / Protection

`01_POWER_PROTECTION.kicad_sch` contains real component-level circuitry rather than a temporary interface harness.

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
- explicit schematic power-source annotations after passive protection and conversion boundaries;
- global GND source connection.

### Sheet 01 validation

```text
0 ERC errors
no temporary interface-harness warnings on 01_POWER_PROTECTION
```

ERC drove correction of:

1. a stock KiCad ferrite-symbol name;
2. a supervisor timing-resistor overlap;
3. missing source annotations after passive boundaries;
4. one redundant quiet-5-V source annotation;
5. the custom-symbol library load context when global ground was added.

### Sheet 01 boundary

Still open:

- active-device footprints;
- exact orderable inductors and capacitors;
- capacitor DC-bias derating;
- copper-dependent thermal calculations;
- exact power-input connector and final format;
- final fuse, protection-diode and ferrite selections;
- TPS3431 VSON land-pattern and assembly verification.

## Captured sheet 08 — Controls / State / Safe Selector

`08_CONTROLS_STATE.kicad_sch` now contains the real controls and fail-safe selection circuit.

Captured functions:

- MCP4728 four-channel normal-operation control DAC;
- shared I²C pull-ups;
- MCP4728 LDAC tied low for acknowledged update behaviour;
- MCP4728 ready/busy test point;
- TMUX1574 four-channel 2:1 fail-safe selector;
- +3.3 V safe inputs for maximum SSI2164 attenuation;
- MCP4728 normal-control inputs;
- external pull-down on selector release;
- hardware-fault Schottky clamp that overrides MCU release;
- four filtered and bounded SSI2164 control outputs;
- eight panel-potentiometer ADC signals;
- active-low `SERVICE_TEST`, `RESET_CLEAR` and `SAFE_MUTE` inputs;
- four low-current transistor-driven SLS-1 state outputs;
- global GND connection;
- control and safety test points.

### Sheet 08 fail-safe rule

```text
SEL low  = +3.3 V safe attenuation
SEL high = MCP4728 normal control
HARDWARE_FAULT_N low clamps SEL low
MCU release cannot override an asserted hardware fault
```

The MCP4728 EEPROM state must still request maximum attenuation, but EEPROM is not the primary safety mechanism.

### Sheet 08 validation

```text
0 ERC errors
no temporary interface-harness warnings on 08_CONTROLS_STATE
```

ERC and generator review drove correction of:

1. eleven missing controls-to-MCU hierarchy signals;
2. dangling MCU scaffold labels, replaced with a temporary non-board harness;
3. a missing global-ground relationship;
4. a selector pull-down/release resistor overlap that shorted release to ground;
5. stock potentiometer and LED library-version mismatches;
6. an unavailable generic NPN stock-symbol alias;
7. TMUX pins whose generic bidirectional types conflicted with their fixed application roles;
8. provisional references containing trailing letters.

### Sheet 08 boundary

Still open:

- exact MCP4728 and TMUX1574 footprints;
- exact LED colours, current targets and panel mechanics;
- exact transistor choice and footprint;
- exact panel-potentiometer and switch parts;
- measured TMUX release/fault-clamp timing;
- MCP4728 EEPROM programming and bring-up proof;
- measured SSI2164 control range after sheet 05/06 integration.

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

The remaining `isolated_pin_label` warnings belong only to uncaptured sheets. They come from temporary non-BOM, non-board interface harness symbols that keep hierarchical labels electrically attached until actual circuitry replaces them.

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
[x] 08_CONTROLS_STATE
[ ] 02_MCU_CLOCK_DEBUG       NEXT
[ ] 03_CODEC_CONVERSION
[ ] 06_RETURN_BREAK_LIMITER
[ ] 04_INPUT_PRESSURE_ABSENCE
[ ] 05_MEMORY_GHOST_WET
[ ] 07_OUTPUT_MUTE_PROTECTION
[ ] 09_TEST_SERVICE
[ ] 00_TOP final interface and ERC review
```

Sheet 02 will replace the MCU scaffold with the STM32H743VIT6, SAI1 transport pins, I²C bus, eight ADC inputs, operating inputs, safety outputs, state outputs, HSE, reset and SWD/debug circuitry.

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
