---
id: R-304
title: "Speech-to-text"
phase: 3
status: planned
area: organs/ears
kind: code
depends_on: []
decisions: [D-010]
cost_gbp: null
updated: 2026-10-14
---
## Goal
Speech recognition on the brain computer (Whisper-family, CPU) from the crown's audio, feeding chat().

## Why
So Henry can talk instead of type.

## Tasks
- [ ] Pick a model/runtime that's fast enough on the robot laptop (R-104/R-105)
- [ ] In the virtual robot, listen through the machine's own mic (D-012), so speech-to-text is built and tested before the crown exists; the same code then reads the crown
- [ ] Voice activity detection — only transcribe speech
- [ ] Transcripts logged, audio only with a debug setting (D-010)

## Done when
Henry speaks and the words reach chat() quickly enough.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: Phase 3 grill: no longer waits for the crown firmware — built against the machine's own mic in the virtual robot first.
