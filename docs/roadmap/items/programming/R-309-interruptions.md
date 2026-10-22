---
id: R-309
title: "Interruptions"
phase: 3
status: idea
area: organs/ears
kind: code
depends_on: [R-304, R-307]
decisions: []
cost_gbp: null
updated: 2026-10-14
---
## Goal
Henry can interrupt Qbot mid-sentence.

## Why
Feels much more natural.

## Tasks
- [ ] Tell Qbot's own voice apart from Henry's (echo cancellation — maybe a reason to revisit D-004's plan B)

## Done when
Talking over Qbot makes it stop and listen.

## Open questions
- Is Phase 3 half-duplex (mics ignored while Qbot speaks)? Dan: try it and
  see when we get there.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: Phase 3 grill: half-duplex vs not is decided by playing with it.
