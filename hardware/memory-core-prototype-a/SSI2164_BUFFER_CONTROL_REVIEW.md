# SSI2164 buffered-control review

## Decision

The SSI2164 control ports are buffered with one shared OPA4196 quad operational amplifier, `U63`, powered from protected +/-12 V.

```text
U63 unit 1  Memory VC1 buffer   sheet 05
U63 unit 2  Ghost VC2 buffer    sheet 05
U63 unit 3  Return VC3 buffer   sheet 06
U63 unit 4  wet-master VC4      sheet 05
U63 unit 5  common power        sheet 06
```

Each channel retains its 1 kΩ / capacitor pre-buffer filter, uses a unity-gain follower, adds 20 Ω output isolation, and clamps the post-buffer SSI2164 control node to the 0 V / +3.3 V domain.

## Electrical result

At the lowest accepted SSI2164 control-port impedance:

```text
VC at 3.3 V request = 3.3 V × 9 kΩ / (9 kΩ + 20 Ω)
                    = 3.2927 V
attenuation         = 3.2927 V / 33 mV/dB
                    = approximately 99.8 dB
```

Using the existing lower resistor-only +3.3 V estimate gives approximately 98.1 dB attenuation.

## Physical-coordinate result

The pinned schematic API mirrors custom multi-unit pin Y coordinates. The committed repair tool corrects only U63 input, feedback, output and common-power label attachments after native generation.

Two intentional coincident label pairs are present:

```text
MEM_CTRL_BUFFER_IN    C502 pin 1 + U63A pin 3    91.44, 107.95
GHOST_CTRL_BUFFER_IN  C506 pin 1 + U63B pin 5    91.44, 161.29
```

The lane validator expects multiplicity two only at those proven same-net junctions. Every other U63 physical coordinate remains unique.

## Committed-state proof

Final read-only authority workflow:

```text
.github/workflows/ssi2164-buffered-control-authority.yml
workflow run 30175313367
```

Results:

```text
committed lane validator                 PASS
committed Memory/Ghost/Wet validator     PASS
committed current-stage validator        PASS
UUID-normalized regeneration             PASS
post-regeneration validators             PASS
KiCad 10 hierarchical ERC errors         0
KiCad 10 hierarchical ERC warnings       0
```

The pinned generator replaces KiCad serialization UUIDs during full regeneration. The authority workflow proved:

```text
sheet 05 UUID count       416 unique
sheet 06 UUID count       501 unique
removed UUID lines        917
added UUID lines          917
non-UUID lines changed    0
normalized content        exactly equal
```

## Repository state

- Implementation-only patch scripts are removed.
- The write-enabled temporary workflow is removed.
- The retained authority workflow is read-only.
- SSI2164 and OPA4196 footprints remain blank.
- PCB, routing, panel, fabrication, purchasing and production remain blocked.

## Remaining gates

- independent exact-head review of PR #49;
- owner authorisation before marking the PR ready;
- owner authorisation before merge;
- exact SSI2164 and OPA4196 land-pattern review in a later protected lane;
- exact post-buffer clamp-diode selection;
- regulator-reference tolerance in the complete attenuation bound;
- bench measurement of unity, attenuation, startup and fault behaviour.

Do not mark PR #49 ready or merge it if the head, base, final file scope, validators, semantic-regeneration proof or ERC result changes.
