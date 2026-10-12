---
id: R-401
title: "Neck: looking around"
phase: 4
status: idea
area: organs/neck
kind: both
depends_on: [R-305]
decisions: [D-012]
cost_gbp: null
updated: 2026-10-12
---
## Goal
The head turns left/right (and maybe tilts) on servos, turning towards voices beyond the eyes' range.

## Why
Dan: the head will eventually be able to look around.

## Tasks
- [ ] Head weight → servo choice
- [ ] Router: turn the head when the voice is past the eyes' range
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Qbot turns its head towards someone behind it.

## Open questions
- Tilt as well as pan? (Figure out at the time.)

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
