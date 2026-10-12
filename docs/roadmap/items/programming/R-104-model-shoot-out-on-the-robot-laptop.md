---
id: R-104
title: "Model shoot-out on the robot laptop"
phase: 1
status: planned
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-10-08
---
## Goal
Pick the best model for Qbot by testing several small models on the actual robot laptop (8 years old, 8GB RAM, no GPU) — for both reply quality and speed.

## Why
Dan: "the current models are too stupid", and few have been tried. The dev machine (i7-1355U, 32GB) is much faster than the robot laptop, so only tests on the real hardware count.

## Tasks
- [ ] Shortlist candidate models that fit in 8GB alongside Whisper + TTS
- [ ] Reuse the scenario conversations as a fixed test set
- [ ] Record per model: time to first token, tokens/s, RAM, JSON-schema reliability, quality notes
- [ ] Write up the results here and pick a default

## Done when
A results table exists here and `PRIMARY_MODEL` is set from it.

## Open questions
- What CPU is in the robot laptop? (`lscpu` on it)

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
