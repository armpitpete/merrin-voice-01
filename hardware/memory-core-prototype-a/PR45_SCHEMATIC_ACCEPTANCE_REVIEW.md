# PR #45 — Schematic Acceptance Review

## Decision

```text
NATIVE COMPONENT-LEVEL SCHEMATIC: ACCEPTED AS A REVIEWED PROTOTYPE CANDIDATE
HIERARCHY / INTERFACES / SHARED DEVICES: ACCEPTED
KICAD 10 ERC: PASS — 0 ERRORS / 0 WARNINGS
RETURN SAFETY CLAIMS: TRANSFERRED TO EXACT-PART AND BENCH GATES
OUTPUT FAIL-MUTE CLAIMS: TRANSFERRED TO EXACT-PART AND BENCH GATES
FOOTPRINTS: NOT ACCEPTED
PCB PLACEMENT / ROUTING: NOT AUTHORISED
FABRICATION / PURCHASING: NOT AUTHORISED
SQUASH-MERGE METHOD: APPROVED
MERGE EXECUTION: NOT AUTHORISED BY THIS REVIEW RECORD
PR STATE: KEEP DRAFT UNTIL THE DELIBERATE MERGE ACTION
```

This review accepts the V5.2 schematic as the bounded output of the native capture lane. It does not certify production safety, measured performance, exact packages, footprints, mechanics or manufacturability.

The squash-merge method is explicitly approved. This approval selects the merge method only; it does not itself merge PR #45, mark it ready, begin footprint work or grant PCB authority.

## Review basis

At the start of this review, PR #45 was:

```text
141 commits ahead of main
81 changed files
81,590 additions
0 deletions
```

The change set contains:

- the top-level KiCad hierarchy and nine component sheets;
- the project-local application-symbol library;
- generation, amendment and repair scripts;
- native contract validators;
- KiCad 10 ERC workflows;
- sheet validation records and capture markers.

The final committed-file review passed without regenerating or promoting the schematic. This proves that the committed native files, rather than only a generated workspace, satisfy the integrated validators and KiCad ERC gate.

## Accepted schematic evidence

The following are accepted at schematic-capture level:

- all nine child sheets are present and connected through `00_TOP`;
- all parent sheet pins and child hierarchical labels agree in name and direction;
- all 45 hierarchy nets have a provider and a consumer;
- sheet 04 exports only `DIRECT_PRESENT`, `SHAPED_PRESENT`, and `ADC_ANALOG_IN`;
- sheet 05 exports only `WET_MIX`;
- sheet 06 exports only `RETURN_LIMITED`, `RETURN_FEED`, and `ABSENCE_INFLUENCE`;
- sheets 07 and 09 export no hierarchy net;
- raw Return, Break, limiter, wet-sum, mute, output-protection and service-probe nodes remain local;
- `U60` is one physical SSI2164 shared across sheets 05 and 06;
- `U32` is one physical OPA1679 shared across sheets 03 and 07;
- former hierarchy harnesses and `J901`–`J909` scaffold references are absent;
- KiCad CLI 10.0.4 reports zero errors and zero warnings.

No blocking hierarchy, reference-allocation, shared-device or ERC defect remains in the accepted native files.

## Validation limitation

The automated gates are strong but bounded.

They verify:

- hierarchy and native label directions;
- symbol pin contracts;
- multi-unit ownership;
- reference uniqueness;
- selected resistor-value and topology tokens;
- calculated design constants;
- blank-footprint boundaries;
- KiCad ERC.

They do not independently prove:

- every analogue transfer function under component tolerance;
- device behaviour across temperature and production spread;
- power-up, power-down or asymmetric-rail sequencing;
- loop stability, recovery or endurance;
- mute depth or audible transient performance;
- external-overvoltage current paths;
- real load drive and output impedance;
- mechanical or footprint correctness.

Those omissions are not hidden exceptions. They are transferred gates below.

## Integrated Return safety audit

### Accepted architecture

The Return lane has a coherent bounded structure:

```text
RETURN_DAC
  → one-third normalisation
  → SSI2164 channel 3
  → unity-normal Break stage
  → unity-normal asymmetric Return shaping
  → current-limited dual-polarity clamp
  → buffered RETURN_LIMITED
  → fixed RETURN_FEED branch
```

Accepted static safeguards:

- official SSI2164 channel-3 pins are used: `15 IIN3`, `14 VC3`, `13 IOUT3`;
- the SSI2164 Mode pin is left open for Class-AB operation;
- the input and stability network follows the accepted current-input architecture;
- `VCA_RETURN_CTRL` is series-isolated and clamped to the 0–3.3 V control range;
- the hard limiter is analogue and independent of MCU action;
- `RETURN_FEED` is fixed by `27.4 kΩ / 40.2 kΩ`;
- `ABSENCE_INFLUENCE` is derived only from `RETURN_LIMITED` and is neutralised during hardware fault;
- unbounded internal Return nodes do not cross the sheet boundary.

### Transferred Return gates

The following are not schematic acceptance claims:

1. **Control-law calibration** — the SSI2164 control input and its external series resistance affect the realised attenuation law and endpoint. Verify the full control range with the exact device.
2. **Limiter threshold and symmetry** — exact Schottky forward voltage, reference tolerance, op-amp output behaviour and loading determine the real limit.
3. **Loop polarity and gain** — verify the complete codec → Return → Memory loop at minimum, nominal and maximum control settings.
4. **Recovery and stability** — measure recovery from hard limiting, nonlinear stages, rapid control movement and fault transitions.
5. **Worst-setting endurance** — run the defined 30-minute maximum-Return test while monitoring output, rails, device temperature and latch-up.
6. **Fault neutralisation** — prove `ABSENCE_INFLUENCE` returns to a neutral state during watchdog, reset, rail sequencing and disconnected-control faults.

A failure in any of these gates may require a schematic revision before footprint or PCB work continues.

## Integrated output and mute audit

### Accepted architecture

The output lane is a coherent prototype path:

```text
DIRECT_PRESENT + WET_MIX
  → equal inverting half-sum
  → passive output level
  → buffer
  → shunt mute
  → post-mute driver
  → bipolar AC coupling
  → series output protection
  → RF/reference network and rail clamps
  → logical mono output jack
```

Accepted static constraints:

- Direct and Wet each have a calculated magnitude of approximately `0.4975`;
- two `6 Vpp` inputs calculate to approximately `5.97 Vpp` before passive attenuation;
- the output-level control cannot add gain;
- the mute defaults toward the shunt-on state for low or undefined `HARDWARE_FAULT_N` while the designed supply path is present;
- the output is AC-coupled and series-current-limited;
- all mute, protection and jack nodes remain local to sheet 07.

### Transferred output gates

1. **Mute device selection** — `J113-class` is not an accepted part. `VGS(off)`, on-resistance and spread determine whether residual audio is acceptably low. The current schematic must not be described as guaranteeing silence.
2. **Asymmetric rail loss** — the optocoupler fault path uses the positive analogue rail while the healthy release uses the negative rail. Prove behaviour for every rail-arrival and rail-loss order.
3. **Mute timing** — the `12.7 ms` clamp and `90.9 ms` release figures are first-pass calculations. Measure exact fault response, release, mute depth and pop energy.
4. **Output loading** — the `1 kΩ` series resistor limits current but creates load-dependent attenuation and output impedance. Verify intended loads and cable capacitance.
5. **External overvoltage** — confirm clamp-diode current, rail injection and back-power behaviour with the exact diode parts and power states.
6. **Jack and coupling behaviour** — verify output DC, coupling-capacitor polarity assumptions, insertion/removal transients and switched-contact behaviour with the exact jack.
7. **Endurance** — run sustained output short, overload and maximum-level tests within an explicitly bounded procedure.

These gates determine whether the current topology survives unchanged or returns to schematic revision.

## Gate separation

### Gate A — Schematic acceptance: passed

Accepted now:

- logical architecture;
- hierarchy and net boundaries;
- symbol pin contracts;
- shared-device allocation;
- calculated first-pass values;
- native KiCad parse and ERC.

### Gate B — Exact-part and footprint review: not started

Must include, per device:

- exact manufacturer part number;
- official package drawing;
- pin-number and pin-1 orientation check;
- exposed-pad or thermal-pad treatment;
- courtyard, assembly and hand/reflow constraints;
- footprint source and independent review;
- explicit confirmation that the selected part satisfies the schematic assumptions.

Selecting a footprint does not waive a failed electrical assumption. Exact-part review may return the design to Gate A.

### Gate C — Bench acceptance: not started

Must include:

- power and rail sequencing;
- codec levels and clocks;
- VCA control range;
- Return loop gain, polarity, limiting and endurance;
- mute depth, timing and pop behaviour;
- output level, load drive, fault current and endurance;
- service-probe loading;
- documented pass/fail limits and retained evidence.

### Gate D — PCB and production: blocked

No placement, routing, fabrication output, purchasing or production pricing is authorised by this review.

## Repository hygiene completed during review

Removed after reference and workflow inspection:

- the two exhausted self-writing status-closeout workflows;
- their two one-use README mutation scripts;
- the original temporary-hierarchy bootstrap generator;
- its corrected bootstrap wrapper.

The bootstrap generators could overwrite accepted component sheets with temporary interface harnesses. Their implementation and every generated stage remain recoverable from PR history, so removal preserves evidence while eliminating the destructive entry point.

## Post-cleanup verification

The cleaned branch was rechecked after the one-use and bootstrap paths were removed and the authority records were updated.

Independent committed-file results:

```text
final 00_TOP integrated workflow          PASS
consolidated generic schematic ERC        PASS
integrated Return workflow                PASS
output / mute / protection workflow       PASS
reconciliation / generation / promotion   SKIPPED
KiCad ERC                                 0 errors / 0 warnings
```

The cleanup did not alter the accepted native schematic.

## Merge-method decision

### Approved: squash merge

The squash-merge decision is approved.

Reasons:

- the branch contains a long sequence of incremental generation, promotion, repair and bot commits;
- many intermediate commits intentionally represent rejected or superseded generated states;
- the final native files and validation records are the authority, not the transient commit sequence;
- a squash commit gives `main` one bounded, reviewable schematic-capture change;
- the PR, Actions history and validation records retain the full evidence trail;
- all current-head workflows are green and the committed native files pass without regeneration or promotion.

A normal merge commit and a rebase merge are rejected for this PR because both would unnecessarily carry the transient capture history into `main`.

Approved squash title:

```text
V5.2: capture and validate Memory Core Prototype A schematic
```

Approved squash body:

```text
Capture the nine-sheet native KiCad hierarchy for Memory Core Prototype A,
validate shared devices and restricted boundaries, complete the integrated
00_TOP review, and retain explicit footprint, bench, PCB and production gates.
```

This record does not execute the merge. PR #45 remains draft until the deliberate merge action is separately authorised.

## Next authorised lane

The next repository action is the deliberate squash merge of PR #45 using the approved title and body.

Only after that merge completes may exact-part and footprint verification begin in a separate PR. Start with the highest-risk physical assumptions:

1. J113-class output mute device and its required mute-depth performance;
2. output optocoupler, NPN inverter and power-sequencing assumptions;
3. WQP518MA / Thonkiconn input and output jack pin maps and mechanics;
4. SSI2164 exact package and control-law assumptions;
5. OPA1679 package and decoupling placement requirements;
6. Return limiter and clamp diodes;
7. service connector and test-point access.

PCB placement, routing, fabrication and purchasing remain blocked.