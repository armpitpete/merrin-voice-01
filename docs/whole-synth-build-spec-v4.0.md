# V4.0 — Whole Synth Build Spec

## Purpose

V4.0 defines what the completed Merrin Grief Synth is meant to become.

This is a planning/specification lane, not a demo lane and not a sound-expansion lane.

The current browser instrument already proves the core Constrained Grief voice. V4.0 exists to define the whole synth around that proven voice before any final demo media is made.

## Current foundation

Merrin Voice 01 currently exists as:

```text
Merrin Grief Synth — Constrained Grief
```

Current accepted foundation:

- browser-first Web Audio instrument
- one focused emotional voice
- on-screen keyboard
- computer keyboard input
- MIDI keyboard input
- active note display
- MIDI diagnostics and panic controls
- live oscilloscope
- Constrained Grief control language
- Scale / Tone / Envelope / Room / Memory signal-path idea

This means the project is not at first-build stage.

It is at whole-synth definition stage.

## Important boundary

Do not make final demo media during this lane.

A real audio/video demo belongs after the whole synth has been built and accepted.

V4.0 should not make the existing browser proof look like the final finished instrument.

## Whole synth definition

The whole synth is the completed instrument built around the existing Constrained Grief voice.

It must answer these questions:

1. What is the final playable instrument?
2. What is the final signal path?
3. What controls belong on the main surface?
4. Which controls are performance controls and which are diagnostics?
5. What emotional behaviours are required?
6. What is deliberately out of scope?
7. What counts as complete before a final demo is recorded?

## Core identity

The whole synth should remain:

```text
small, specific, emotional, constrained, playable
```

It should not become:

```text
a general-purpose synth, workstation, modular playground, sequencer, or plugin framework
```

Its value is the focused emotional voice and the grief-shaped behaviour around it.

## Working product sentence

Merrin Grief Synth is a small emotional synth built around one constrained voice: dark, slow, weighted, fragile, lingering, and remembered.

The whole synth extends that voice into a finished playable instrument without losing the one-emotion focus.

## Signal path

The existing signal path should remain the spine:

```text
MV-02 Scale
  ↓
MV-01 Tone
  ↓
MV-03 Envelope
  ↓
MF-01 Room
  ↓
MF-02 Memory
```

Plain meaning:

```text
pitch field
  ↓
voice source and tone
  ↓
arrival, hold, and release
  ↓
space around the voice
  ↓
remembered echo / fading trace
```

## Main surface controls

The whole synth should keep the current emotional control model unless a later test proves a control is weak.

### Playable controls

| Control | Purpose |
|---|---|
| Tone | darkness / softness / permitted brightness |
| Fade | arrival and disappearance of the note |
| Echo | remembered or distant quality |
| Amplitude | safe output level |

### Voice-shaping controls

| Control | Purpose |
|---|---|
| Shape | Pure / Hollow / Pressed voice character |
| Sub | weight without bass boom |
| Overtone | ache without shine |
| Drift | small instability |

### Emotion-shaped controls

| Control | Purpose |
|---|---|
| Scale | constrained pitch field |
| Glide | how hard it is to move |
| Weight | heaviness under the voice |
| Wither | fragile movement in the fade |

## Diagnostic controls

Diagnostic controls are allowed, but they should not feel like the instrument surface.

Diagnostics belong behind a test or advanced section.

Current diagnostic/tool controls include:

- All effects off
- Normal voice
- effect test switches
- Wither delay
- MIDI diagnostics
- raw MIDI monitor
- MIDI panic
- oscilloscope

V4.0 should decide which diagnostics remain visible and which move behind a simple mode.

## Required whole-synth behaviours

The completed synth should support these behaviours:

### 1. Constrained pitch

The pitch world should feel bounded.

The player should not feel like they are playing a normal chromatic keyboard unless they choose the chromatic test mode.

### 2. Lingering envelope

Notes should arrive and leave with emotional weight.

Fast plucks may exist for testing, but the core identity is lingering.

### 3. Weight without boom

Low content should add body, not become a bass feature.

### 4. Ache without brightness

Overtone content should add pain, pressure, or edge without becoming shiny or triumphant.

### 5. Wither

The voice should be able to tremble or weaken after it has begun.

This should feel fragile rather than decorative.

### 6. Room

Space should support the voice without swallowing it.

### 7. Memory

Echo should feel like a remembered trace, not a normal delay effect added for fun.

### 8. Safe release

The synth should recover safely from note releases, page focus changes, MIDI panic, and scale changes.

## Possible whole-synth additions

These are candidates only. They are not approved automatically.

### HOME

A return control that brings the voice back to a safe tonal/emotional centre.

Use only if it strengthens Constrained Grief rather than turning the synth into a performance toy.

### RITUAL

A controlled gesture or event that briefly intensifies the grief behaviour and then settles.

Use only if it is repeatable, understandable, and not random feature creep.

### Simple mode

A normal performance view that hides diagnostics until needed.

This is likely useful because the current browser proof contains development/test controls that may make the instrument look less finished.

## Explicit non-goals

Do not add these in V4.0:

- final demo media
- fake demo media
- sequencer behaviour
- presets
- recording
- MIDI output
- pitch bend
- modulation wheel
- sustain pedal behaviour
- MIDI channel routing
- VST framework work
- VCV Rack framework work
- DAW instrument work
- general synth expansion
- extra controls just because they are possible
- Sample Hold Lab merging
- Radio Ghost merging
- M A C controller work
- DBHT-1 expansion work unless explicitly opened as a separate lane

## Completion criteria for V4.0

V4.0 is complete when the repo contains a clear answer to:

```text
What is the whole Merrin Grief Synth?
What exists now?
What is missing before final demo?
What is forbidden until the whole synth is accepted?
```

No audio demo is required for V4.0.

No code change is required for V4.0.

No new sound behaviour is required for V4.0.

## Later finish-demo lane

Only after the whole synth is built and accepted, open a separate finish-demo lane.

That later lane may include:

- real audio/video demo
- screenshots
- GIFs
- release page
- public portfolio text
- final GitHub release notes

That later lane must use the finished synth, not the partial proof stage.
