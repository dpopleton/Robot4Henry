---
id: R-210
title: "Mouth display"
phase: 2
status: planned
area: organs/mouth
kind: both
depends_on: []
decisions: [D-008, D-009]
cost_gbp: 5
updated: 2026-10-08
---
## Goal
A rectangular display (already bought) showing a flat-line mouth, sound-wave shapes while Qbot talks, and mood when quiet.

## Why
Part of the face; shows that Qbot is speaking.

## Tasks
- [ ] Find the display and identify it (ST7789?)
- [ ] Own Pico (D-009); reuse the eyes' framebuffer approach
- [ ] Flat line + mood shapes
- [ ] Sound waves while talking
- [ ] Mount in the front frame

## Done when
The mouth shows mood when quiet and moves while Qbot talks, mounted in the head.

## Open questions
- How are the sound waves driven — levels from the laptop, or the mouth Pico listening to the speaker signal on an ADC pin? (Decide when we get there.)
- Which display is it exactly?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
