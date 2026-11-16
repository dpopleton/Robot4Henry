---
id: R-602
title: "First vision task"
phase: 6
status: idea
area: organs/vision
kind: code
depends_on: [R-601]
decisions: []
cost_gbp: null
updated: 2026-11-06
---
## Goal
Decide and build the first thing vision does.

## Why
Henry wants Qbot to "see everything". The two candidates are recognising who he's talking to (R-311) and recognising objects; both would be very cool, and the choice is made when we get there. Following faces with the eyes is dropped: the mics already point the eyes (R-305). Vision will also feed the body's movement (D-020), so it may run in parallel with the body (Phase 5); the order is decided at the time.

## Tasks
- [ ] Decide: who's talking (R-311) or objects
- [ ] Get it running on the current robot laptop before considering an upgrade (R-902); measure the cost alongside the LLM, speech-to-text and TTS
- [ ] Decide what gets stored (photos are fine, the robot is air-gapped; keep only what a feature needs) and add it to `docs/disk-space.md`

## Done when
To be defined.

## Open questions
- What should vision do first: who's talking, or objects?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-11-06: Phase 6 grill: face-following dropped; R-311 or objects, decided later. Storing photos is fine (air-gapped). Try it on the current laptop first. Henry wants it to "see everything".
