# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
01_POWER_PROTECTION COMPLETE / ERC VALIDATED
08_CONTROLS_STATE COMPLETE / ERC VALIDATED
02_MCU_CLOCK_DEBUG COMPLETE / ERC VALIDATED
03_CODEC_CONVERSION NEXT
PCB WORK BLOCKED
```

This folder contains the native KiCad hierarchy for **Merrin Grief Synth — Constrained Grief**.

Component-level circuitry is being added one sheet at a time. Full hierarchical ERC is run after each bounded capture.

The project is not yet a completed hardware schematic or production-ready design.

## Native hierarchy

```text
MerrinGriefSynthMemoryCoreA.kicad_sch
├── 01_POWER_PROTECTION.kicad_sch       CAPTURED / ERC VALIDATED
├── 02_MCU_CLOCK_DEBUG.kicad_sch        CAPTURED / ERC VALIDATED
├── 03_CODEC_CONVERSION.kicad_sch       NEXT CAPTURE
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch INTERFACE SCAFFOLD
├── 05_MEMORY_GHOST_WET.kicad_sch       INTERFACE SCAFFOLD
├── 06_RETURN_BREAK_LIMITER.kicad_sch   INTERFACE SCAFFOLD
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD
├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED
└── 09_TEST_SERVICE.kicad_sch           INTERFACE SCAFFOLD
```

## Locked interface constraints

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

Captured functions:

- protected positive and negative 12 V rail entry;
- provisional current limiting, reverse-polarity protection and ferrite filtering;
- 3.293 V TPS62160 digital regulator;
- 5.453 V TPS62160 codec preregulator;
- TPS7A2050 quiet 5 V codec-analogue regulator;
- TPS3808G33 supervision and manual reset;
- TPS3431 independent watchdog;
- active-low open-drain `HARDWARE_FAULT_N` combination;
- rail, fault and watchdog test points;
- explicit source annotations after passive conversion boundaries;
- global GND source.

Validation:

```text
0 ERC errors
no temporary interface-harness warnings on 01_POWER_PROTECTION
```

ERC drove correction of stock-symbol naming, a resistor overlap, missing and redundant source annotations, and project-local-symbol loading while adding global ground.

Still open:

- active-device footprints;
- exact inductors, capacitors, protection parts and connector;
- capacitor derating and copper-dependent thermal checks;
- TPS3431 VSON land-pattern and assembly verification.

## Captured sheet 08 — Controls / State / Safe Selector

Captured functions:

- MCP4728 four-channel normal-control DAC;
- I²C pull-ups and ready/busy test point;
- TMUX1574 four-channel fail-safe selector;
- +3.3 V default attenuation inputs;
- hardware-fault clamp overriding MCU release;
- four filtered and bounded SSI2164 control outputs;
- eight panel-potentiometer ADC signals;
- `SERVICE_TEST`, `RESET_CLEAR` and `SAFE_MUTE` inputs;
- four transistor-driven SLS-1 state outputs;
- global GND and safety test points.

Locked selector rule:

```text
SEL low  = +3.3 V safe attenuation
SEL high = MCP4728 normal control
HARDWARE_FAULT_N low forces SEL low
```

Validation:

```text
0 ERC errors
no temporary interface-harness warnings on 08_CONTROLS_STATE
```

ERC drove correction of missing hierarchy signals, dangling MCU labels, global ground scope, a selector-net overlap, symbol-library mismatches, TMUX application pin types and reference formatting.

Still open:

- exact MCP4728 and TMUX1574 footprints;
- exact panel controls, LEDs and transistor parts;
- measured release/fault timing;
- MCP4728 EEPROM and bring-up proof;
- measured SSI2164 control range after sheets 05 and 06 are integrated.

## Captured sheet 02 — MCU / Clock / Debug

`02_MCU_CLOCK_DEBUG.kicad_sch` now replaces the temporary MCU scaffold.

Captured functions:

- project-local `STM32H743VIT6_LQFP100` symbol containing all 100 physical pins;
- exact LQFP-100 pin numbers from ST DS12110 Rev 11;
- accepted SAI1 allocation on PE2–PE6;
- I²C1 on PB8/PB9;
- eight panel ADC inputs on PA0–PA7;
- codec reset/mute, fault sense, watchdog and safe-release signals on PD8–PD12;
- service, reset and safe-mute inputs on PD13–PD15;
- SLS-1 outputs on PC6–PC9;
- SWDIO and SWCLK on PA13/PA14;
- BOOT0 deterministic pull-down;
- five VDD/VSS supply pairs;
- filtered VDDA/VREF+ analogue supply;
- VBAT tied to Prototype A 3.3 V;
- both VCAP outputs with dedicated 2.2 µF capacitors;
- 24.576 MHz external CMOS HSE source in bypass mode;
- SWD service connector and digital/safety test points;
- explicit no-connect markers on every unused MCU pin.

Locked physical signals:

```text
PE2  CODEC_MCLK
PE3  CODEC_DOUT
PE4  CODEC_LRCLK
PE5  CODEC_BCLK
PE6  CODEC_DIN

PB8  CTRL_I2C_SCL
PB9  CTRL_I2C_SDA

PA0–PA7   eight panel controls
PD8–PD15  safety and operating controls
PC6–PC9   state outputs
PA13/PA14 SWD
```

Validation:

```text
100 physical MCU pins encoded
selected-pin contract passed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 02_MCU_CLOCK_DEBUG
committed-file rerun passed with generation skipped
```

Still open:

- exact STM32H743VIT6 footprint verification;
- exact 24.576 MHz oscillator and footprint;
- decoupling physical placement;
- oscillator signal-integrity review;
- SWD connector choice and mechanics;
- CubeMX `.ioc` and generated clock-tree proof;
- measured MCLK/BCLK/LRCLK timing;
- SRAM/DMA linker placement and firmware resource proof.

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

Remaining scaffold warnings are temporary and are not accepted permanent exceptions.

As each sheet receives its real circuit:

1. remove its temporary interface harness;
2. connect every hierarchical label to actual circuitry;
3. rerun full hierarchical ERC;
4. correct real electrical findings;
5. document any unavoidable intentional exception;
6. do not permit new warning classes silently.

The finished component-level schematic must pass ERC with no unexplained errors or warnings.

## Active capture order

```text
[x] 01_POWER_PROTECTION
[x] 08_CONTROLS_STATE
[x] 02_MCU_CLOCK_DEBUG
[ ] 03_CODEC_CONVERSION       NEXT
[ ] 06_RETURN_BREAK_LIMITER
[ ] 04_INPUT_PRESSURE_ABSENCE
[ ] 05_MEMORY_GHOST_WET
[ ] 07_OUTPUT_MUTE_PROTECTION
[ ] 09_TEST_SERVICE
[ ] 00_TOP final interface and ERC review
```

Sheet 03 will replace the codec scaffold with the PCM3168A supply, reset/control, TDM transport, ADC ingress, three used DAC outputs, conversion-boundary analogue stages and explicit unused-channel treatment.

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
