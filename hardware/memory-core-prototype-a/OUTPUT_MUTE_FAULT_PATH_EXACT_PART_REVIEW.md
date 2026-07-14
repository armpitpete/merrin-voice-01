# Output Mute and Fault-Control Exact-Part Review

## Decision after second evidence repair

```text
Q70 MMBFJ113 EXACT PART / PIN MAP / PACKAGE: PASS, SUBJECT TO PR REVIEW
Q71 PMV20XNE EXACT PART / PIN MAP / PACKAGE: PASS, SUBJECT TO PR REVIEW
U70 VO617A-3X007T EXACT PART / PIN MAP / PACKAGE: PASS, SUBJECT TO PR REVIEW
POWERED HEALTHY-RELEASE TOPOLOGY: PASS AT CALCULATED SCHEMATIC LEVEL
Q70 CASE 318-08 INDEPENDENT DIMENSIONAL AUDIT: PASS
Q71 TO-236AB INDEPENDENT DIMENSIONAL AUDIT: PASS
U70 OPTION-7 SMD-4 DIMENSIONAL AUDIT: PASS
U70 25 C DATASHEET-BOUND SATURATION PROOF: PASS — 8.93:1
IMMUTABLE KICAD FOOTPRINT PROVENANCE: PASS
MEASURED BEHAVIOUR: GATE C
PCB / ROUTING / FABRICATION / PURCHASING: BLOCKED
PR ACCEPTANCE: SUBJECT TO NEW HUMAN REVIEW
```

The exact active parts, physical pin maps and package mappings remain unchanged. This repair closes the three evidence defects identified by the previous review. It does not approve measured behaviour or any PCB activity.

## Corrected topology

```text
RAIL_3V3 -- R10 10k -- HARDWARE_FAULT_N -- R711 10k -- Q71 gate
                                                |
                                             R712 100k
                                                |
                                               GND

RAIL_P12 -- R713 820R -- R714 1k -- U70 LED -- Q71 drain
Q71 source ----------------------------------------------- GND

RAIL_N12 -- R715 10k -- U70 emitter
U70 collector ------------------ MUTE_GATE
                                  |
                         R716 100k to GND
                         C710 100nF to GND
                                  |
                         Q70 physical gate
```

Healthy operation powers the isolated negative release. A fault, undefined fault state or loss of `RAIL_P12` removes that release and lets `R716` return the gate toward mute.

## Exact parts and pins

| Ref | Exact part | Package | Physical pins | Assigned KiCad footprint |
|---|---|---|---|---|
| Q70 | onsemi `MMBFJ113` | SOT-23 / TO-236, CASE 318-08 | 1 D, 2 S, 3 G | `Package_TO_SOT_SMD:SOT-23` |
| Q71 | Nexperia `PMV20XNE` | TO-236AB / SOT23 | 1 G, 2 S, 3 D | `Package_TO_SOT_SMD:SOT-23` |
| U70 | Vishay `VO617A-3X007T` | option-7 SMD-4 | 1 A, 2 K, 3 E, 4 C | `Package_DIP:SMDIP-4_W7.62mm` |

## Q70 independent CASE 318-08 dimensional proof

The onsemi datasheet identifies CASE 318-08 as `SOT-23 (TO-236)`. Q70 now has its own package record rather than inheriting Q71's audit.

```text
body length maximum       3.04 mm
body width maximum        1.40 mm
overall lead span maximum 2.64 mm
nominal adjacent pitch    0.95 mm
outer lead pitch range    1.78 to 2.04 mm
lead width maximum        0.50 mm
lead length maximum       0.69 mm
```

The immutable KiCad SOT-23 footprint provides:

```text
pads 1 / 2 / 3       0.90 x 0.80 mm
pin-1 to pin-2 pitch 1.90 mm
courtyard            3.40 x 3.50 mm
```

The validator checks Q70's pitch range, package envelope, pad overlap and pin orientation independently from Q71.

## Q71 independent TO-236AB proof

Q71 remains separately checked against the Nexperia TO-236AB envelope:

```text
body length maximum       3.00 mm
overall width maximum     2.50 mm
outer lead pitch          1.90 mm
lead width maximum        0.48 mm
lead length maximum       0.55 mm
```

## U70 25 C datasheet-bound saturation proof

Vishay specifies the following saturated condition in the electrical-characteristics table defined at `Tamb = 25 C` unless otherwise specified:

```text
IF = 5 mA
IC = 1.0 mA
VCE(sat) <= 0.4 V
```

The conservative LED path produces at least `5.304 mA`. The actual release-path load at the stated saturation voltage is:

```text
RAIL_N12 magnitude at +5% = 12.6 V
R715 + R716 at -1%        = 108.9 kOhm
VCE                       = 0.4 V
required collector current = 0.112 mA
```

The `1.0 mA` saturated test current therefore gives `8.93:1` calculated margin at the 25 C datasheet condition. **Full-temperature release behaviour remains Gate C.** No full-temperature saturation guarantee is claimed by Gate B.

## Q70 mute-depth boundary

```text
TJ = 25 C
VGS = 0 V
VDS <= 0.1 V
MMBFJ113 rDS(on) maximum = 100 ohm
R703 minimum             = 118.8 kOhm
calculated attenuation   = 61.50 dB
```

This remains a 25 C datasheet-bound calculation. Gate C must prove at least `60 dB` on assembled hardware across the declared operating temperature, part spread and signal conditions.

## Immutable footprint provenance

The accepted Gate-B geometry is the committed project-local copy of two files from the official `KiCad/kicad-footprints` repository at one immutable revision:

```text
upstream repository: KiCad/kicad-footprints
upstream commit:     7ebfa6b23cc292a56f751b7b5f4a0e12eeef69dd
```

```text
Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod
Git blob: 50a8c41bf25dc5843c0ceb95820dc83b930321f9
SHA-256:  db5b998f0d36708205a4b8edc0db1501deb0246a81b52e9cb036cfd58b7570d3

Package_DIP.pretty/SMDIP-4_W7.62mm.kicad_mod
Git blob: f45a9a53110c40e6dfdcdae40d07a29856841be2
SHA-256:  23f55da451d042a66c22a94cf3e622a242f6e5c4c7ed22909a564699350bf30d
```

Moving library branches and ambient workstation footprint versions are not Gate-B authority.

## Current validation requirement

The exact current PR head must pass:

1. Q70 CASE 318-08 independent dimensional validation;
2. Q71 TO-236AB independent dimensional validation;
3. U70 option-7 SMD-4 dimensional validation;
4. immutable source-commit, Git-blob and SHA-256 checks;
5. U70 25 C authority checks;
6. exact symbol, pin and hierarchy checks;
7. KiCad 10 hierarchical ERC with zero errors and zero warnings;
8. a committed-file rerun with no promotion diff.

## Remaining gates

Gate C retains full-temperature U70 release behaviour, measured mute depth, audible pop and transient energy, real rail ramps and sequencing, output load behaviour and endurance.

PCB placement, routing, fabrication and purchasing remain blocked. PR #46 requires another deliberate approval-or-rejection review before merge.
