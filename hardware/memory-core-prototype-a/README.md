# Memory Core Prototype A — Native Schematic

## Current status

```text
NATIVE HIERARCHY CAPTURED
01_POWER_PROTECTION COMPLETE / ERC VALIDATED
08_CONTROLS_STATE COMPLETE / ERC VALIDATED
02_MCU_CLOCK_DEBUG COMPLETE / ERC VALIDATED
03_CODEC_CONVERSION COMPLETE / ERC VALIDATED
06_RETURN_BREAK_LIMITER COMPLETE / ERC VALIDATED
04_INPUT_PRESSURE_ABSENCE NEXT
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
├── 03_CODEC_CONVERSION.kicad_sch       CAPTURED / ERC VALIDATED
├── 04_INPUT_PRESSURE_ABSENCE.kicad_sch NEXT CAPTURE
├── 05_MEMORY_GHOST_WET.kicad_sch       INTERFACE SCAFFOLD
├── 06_RETURN_BREAK_LIMITER.kicad_sch   CAPTURED / ERC VALIDATED
├── 07_OUTPUT_MUTE_PROTECTION.kicad_sch INTERFACE SCAFFOLD
├── 08_CONTROLS_STATE.kicad_sch         CAPTURED / ERC VALIDATED
└── 09_TEST_SERVICE.kicad_sch           INTERFACE SCAFFOLD
```

## Locked interface constraints

- Direct Present remains outside the digital core.
- Memory captures shaped Present after Pressure and Absence.
- PCM3168A conversion uses one ADC ingress and three DAC roles: Memory, Ghost and Return send.
- Return passes through Break, analogue Return shaping and the independent limiter boundary.
- Sheet 06 may export only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`.
- Raw Return DAC, SSI2164 output, Break output, normalised Return and clamp nodes remain local to sheet 06.
- `WATCHDOG_HEARTBEAT` enters the power/protection and hardware-fault system.
- TMUX1574 safe-control release remains a controls/safety-sheet responsibility.
- Eight panel controls and three operating inputs are explicit signals between sheets 08 and 02.
- Global ground is established from sheet 01 and shared by captured sheets.
- Sheets 03 and 06 receive the accepted ±12 V analogue rails for OPA1679 stages.

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

Still open:

- exact MCP4728 and TMUX1574 footprints;
- exact panel controls, LEDs and transistor parts;
- measured release/fault timing;
- MCP4728 EEPROM and bring-up proof;
- measured SSI2164 control range after sheets 05 and 06 are integrated.

## Captured sheet 02 — MCU / Clock / Debug

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

## Captured sheet 03 — Codec / Conversion

Captured functions:

- project-local PCM3168A symbol containing all 64 package pins plus PowerPAD;
- quiet local 5 V analogue and 3.3 V digital branches with ferrite filtering and decoupling;
- VCOMAD, VCOMDA, VREFAD1 and VREFAD2 local decoupling;
- 24.576 MHz MCLK, 12.288 MHz BCLK and 48 kHz LRCLK slave connections;
- eight-slot TDM data on DIN1/DOUT1;
- I²C mode at address `0x44`;
- active-low reset/mute gate;
- ADC1 single-ended-to-differential OPA1679 ingress at ±1/3 gain;
- passive anti-alias conditioning referenced to VCOMAD;
- Memory, Ghost and Return DAC1–3 differential-to-single-ended filters;
- three used DAC outputs at approximately 0.747 gain;
- explicit test points, spare op-amp treatment and unused converter treatment.

Locked ADC level relationship:

```text
2 Vpp internal nominal
→ 1.333 Vpp differential ADC input
→ approximately −12.6 dBFS

6 Vpp internal headroom limit
→ 4.0 Vpp differential ADC input
→ approximately −3.0 dBFS
```

Locked DAC filter basis:

```text
TI Figure 61
R1 = 7.5 kΩ
R2 = 5.6 kΩ
R3 = 360 Ω
C1 = 3.3 nF
C2 = 680 pF
gain ≈ 0.747
f−3 dB ≈ 53 kHz
```

Validation:

```text
64 PCM3168A pins plus PowerPAD encoded
codec hierarchy and selected-pin contract passed
project-local PCM3168A and OPA1679 symbols parsed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 03_CODEC_CONVERSION
committed-file rerun passed with generation skipped
```

Still open:

- exact PCM3168A HTQFP-64 PowerPAD footprint verification;
- exact OPA1679 TSSOP-14 footprint verification;
- exact ferrite, coupling and reference capacitors;
- measured ADC full-scale and filter response;
- measured DAC reconstruction response and gain;
- codec register readback and inactive-channel firmware proof;
- measured reset/mute sequencing and pop behaviour;
- PowerPAD thermal-via and ground-plane review.

## Captured sheet 06 — Return / Break / Limiter

`06_RETURN_BREAK_LIMITER.kicad_sch` replaces the temporary Return scaffold and preserves the most safety-critical analogue boundary.

Captured signal route:

```text
RETURN_DAC
  ↓
SSI2164 channel 3 Return VCA
  ↓
OPA1679 current-to-voltage stage
  ↓
bounded Break stage
  ↓
unity Return normaliser
  ↓
2.2 kΩ clamp isolation
  ↓
buffered ±2.5 V dual-polarity Schottky clamp
  ↓
RETURN_LIMITED
  ├── fixed 0.6816 RETURN_FEED
  └── rectified, smoothed and 3 V-bounded ABSENCE_INFLUENCE
```

Captured functions:

- project-local five-unit `SSI2164S_APPLICATION` symbol with verified physical pin map;
- Return VCA on channel 3: pin 10 `IIN3`, pin 11 `VC3`, pin 12 `IOUT3`;
- SSI2164 MODE pin open for Class-AB operation;
- SSI2164 ±12 V power and analogue-ground connections;
- 20 kΩ input and required stability network;
- OPA1679 transimpedance conversion for the current-output VCA;
- unity-gain bounded Break stage with bandwidth loss and antiparallel soft clipping;
- unity Return normalisation so Break plus normalisation remains no greater than unity at small signal;
- buffered +2.5 V and −2.5 V clamp references derived independently from protected analogue rails;
- dual-polarity Schottky hard limiter isolated by 2.2 kΩ;
- buffered `RETURN_LIMITED` output;
- fixed inverting `RETURN_FEED` stage using 40.2 kΩ input and 27.4 kΩ feedback;
- precision positive-envelope path producing slow, bounded `ABSENCE_INFLUENCE`;
- test points at every safety-critical stage;
- reserved no-connect SSI2164 units 1, 2 and 4, pending replacement by real sheet-05 circuitry.

Locked limiter/feed relationship:

```text
buffered references: ±2.5 V
plus Schottky forward drop
→ approximately 5.4–5.6 Vpp at RETURN_LIMITED

RETURN_FEED magnitude
= 27.4 kΩ / 40.2 kΩ
= 0.6816 nominal
< 0.696 at 1% resistor worst case

5.6 Vpp × 0.6816
≈ 3.82 Vpp maximum nominal RETURN_FEED
```

The Return feed is inverting. The later sheet-04 Memory-input summing stage must restore the accepted loop polarity and may receive no raw Return net.

Export boundary:

```text
allowed from sheet 06:
RETURN_LIMITED
RETURN_FEED
ABSENCE_INFLUENCE

forbidden from sheet 06:
raw DAC Return
SSI2164 current output
Break output
normalised Return
clamp references
clamp node
rectifier internal nodes
```

Validation:

```text
SSI2164 channel-3 and power pin coordinates explicitly checked
all five SSI2164 schematic units present
fixed-feed resistor/value contract passed
restricted-export contract passed
native KiCad 10 parse passed
0 hierarchical ERC errors
no temporary interface-harness warnings on 06_RETURN_BREAK_LIMITER
first generated-artifact gate passed
```

ERC and contract review drove correction of:

1. mirrored Y coordinates from the pinned API's project-local multi-unit pin helper;
2. physically swapped MODE/GND/V+/V− attachments that pin-name checking alone did not expose;
3. missing SSI2164 units 1, 2 and 4;
4. brittle numeric-format assumptions in the validation contract;
5. an incorrect temporary interpretation that confused `RETURN_LIMITED` amplitude with the attenuated `RETURN_FEED` amplitude.

Still open:

- exact SSI2164 SOP-16 footprint and physical-pin review;
- exact OPA1679 TSSOP-14 footprints;
- exact soft-clip, Schottky and 3 V clamp diode selections and footprints;
- reference-divider tolerance, source/sink-current and temperature review;
- measured SSI2164 control law and unity-gain point;
- measured Break and normaliser small-signal gain;
- measured `RETURN_LIMITED` clamp thresholds and recovery;
- measured `RETURN_FEED` gain and complete loop gain;
- independent schematic-stage Return safety review after sheet 04 is integrated;
- 30-minute worst-setting endurance test;
- removal of reserved SSI2164 units 1, 2 and 4 from sheet 06 when sheet 05 captures their real circuits.

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
[x] 03_CODEC_CONVERSION
[x] 06_RETURN_BREAK_LIMITER
[ ] 04_INPUT_PRESSURE_ABSENCE  NEXT
[ ] 05_MEMORY_GHOST_WET
[ ] 07_OUTPUT_MUTE_PROTECTION
[ ] 09_TEST_SERVICE
[ ] 00_TOP final interface and ERC review
```

Sheet 04 must now capture the Thonkiconn input, protection, trim/buffer, Pressure, Absence, direct Present split and the Memory-input summing node. Only the fixed `RETURN_FEED` and bounded `ABSENCE_INFLUENCE` may enter it from sheet 06.

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
