# Merrin Voice 01 App v0.1 — System Definition

## Purpose

Explain how the **Constrained Grief** voice works by showing each module, the signal path, and the emotional job of every stage.

## Good enough

A person can open the app, click through the five modules, and understand what each part does without reading the full technical spec.

## System identity

Merrin Voice 01 is a five-module Eurorack voice arranged as one constrained emotional instrument.

It is not a general-purpose synth voice.

It is designed to be:

- slow
- minor
- dark
- soft-edged
- restricted
- melancholic

## Locked concept path

```text
SCALE → TONE → ENVELOPE → ROOM → MEMORY
```

## Locked module order

```text
MV-02 → MV-01 → MV-03 → MF-01 → MF-02
```

## Locked practical signal flow

```text
CV → MV-02 → MV-01 → MV-03 → MF-01 → MF-02 → Output
Gate → MV-03
```

## Module roles

| Module | Plain role | Emotional role |
|---|---|---|
| `MV-02` Melancholy Quantizer | chooses allowed notes | keeps the voice in a sorrow-biased pitch world |
| `MV-01` Somber Oscillator | makes the sound | gives the voice its soft sine/sub tone |
| `MV-03` Lingering Voice | shapes loudness | makes the sound breathe, tremble, and fade |
| `MF-01` Desolate Space | adds reverb | places the voice somewhere cold and distant |
| `MF-02` Fading Echoes | adds delay | lets the voice disappear like memory |

## Merrin Link bus

The Merrin Link bus is the rear connection system.

It carries:

- `PITCH_BUS` — quantized pitch from MV-02 to MV-01
- `GATE_BUS` — gate signal to MV-03
- `AUD_A` — oscillator audio to VCA
- `AUD_B` — VCA audio to reverb
- `AUD_C` — reverb audio to delay
- `GND` — shared ground reference

## v0.1 app boundary

The app explains the instrument only.

It does not yet:

- generate sound
- model exact electronics
- simulate patch cables
- save user settings
- manage hardware design files

## Design rule

Keep the first app simple.

Do not add a framework, audio engine, account system, database, or build pipeline until the static explanation app is clearly useful.
