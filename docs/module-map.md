# Merrin Voice 01 — Module Map

## Very simple version

Merrin Voice 01 is a single sad mono voice.

```text
Pitch choice → Sound → Loudness shape → Space → Echo memory
```

## 1. MV-02 — Melancholy Quantizer

**Plain job:** chooses which notes are allowed.

**Input:** unquantized pitch CV.

**Output:** quantized 1V/oct pitch CV.

**Emotional job:** keeps the voice inside a sorrow-biased pitch world.

**Allowed modes:**

- Natural minor
- Harmonic minor
- Chromatic

**Simple line:**

> You can move, but only inside this sad musical space.

## 2. MV-01 — Somber Oscillator

**Plain job:** makes the actual sound.

**Input:** 1V/oct pitch from MV-02.

**Output:** sine/sub audio.

**Emotional job:** gives the voice a soft, low, slightly unstable tone.

**Core behaviours:**

- sine tone
- sub tone
- glide
- subtle Sigh pitch movement
- subtle Wobble drift

**Simple line:**

> The voice itself: soft, low, unstable, and unable to jump sharply.

## 3. MV-03 — Lingering Voice

**Plain job:** controls how the sound appears and disappears.

**Input:** oscillator audio and gate signal.

**Output:** shaped audio.

**Emotional job:** makes the sound breathe, tremble, and fade.

**Core behaviours:**

- slow attack
- long decay/sustain behaviour
- slow release
- Wither amplitude tremble

**Simple line:**

> The sound must breathe in, linger, tremble, and fade away.

## 4. MF-01 — Desolate Space

**Plain job:** adds dark reverb.

**Input:** shaped voice audio.

**Output:** voice in a dark space.

**Emotional job:** places the sound somewhere cold, distant, and heavy.

**Core behaviours:**

- dark reverb
- high-frequency damping
- diffuse smear
- distance through pre-delay

**Simple line:**

> This voice is not in a normal room. It is somewhere empty.

## 5. MF-02 — Fading Echoes

**Plain job:** adds dark delay.

**Input:** reverbed audio.

**Output:** final voice output.

**Emotional job:** lets the sound fade like memory.

**Core behaviours:**

- slow delay
- filtered repeats
- capped feedback
- no bright rhythmic trick behaviour

**Simple line:**

> The sound has gone, but traces of it remain.
