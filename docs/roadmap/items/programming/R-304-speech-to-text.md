---
id: R-304
title: "Speech-to-text"
phase: 3
status: planned
area: organs/ears
kind: code
depends_on: [R-303]
decisions: [D-010]
cost_gbp: null
updated: 2026-10-08
---
## Goal
Speech recognition on the brain computer (Whisper-family, CPU) from the crown's audio, feeding chat().

## Why
So Henry can talk instead of type.

## Tasks
- [ ] Pick a model/runtime that's fast enough on the robot laptop (R-104/R-105)
- [ ] Use the laptop's own mic for testing until the crown works
- [ ] Voice activity detection — only transcribe speech
- [ ] Transcripts logged, audio only with a debug setting (D-010)

## Done when
Henry speaks and the words reach chat() quickly enough.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
