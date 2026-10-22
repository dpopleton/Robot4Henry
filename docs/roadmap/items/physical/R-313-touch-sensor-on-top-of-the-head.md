---
id: R-313
title: "Pat button on top of the head"
phase: 3
status: idea
area: head
kind: both
depends_on: [R-212]
decisions: [D-009, D-012, D-014]
cost_gbp: 2
updated: 2026-10-22
---
## Goal
A big button on top of the head, read by a Pico, so Qbot notices a pat on the
head and reacts to it. A button instead of touch pads, since the aluminium skin
would block capacitive pads.

## Why
Dan wants Qbot to feel it when someone touches it, not only hear them.

## Tasks
- [ ] Pick a big button that works through (or sits in) the aluminium skin
- [ ] Probably read by the crown Pico, which handles everything on top (D-014)
- [ ] Send a "touched" event to the router; decide what Qbot does with it
- [ ] Works in the virtual robot (D-012): fakes a touch as input (a click on the top of the head)

## Done when
Patting the top of the head reliably makes Qbot react.

## Log
- 2026-10-14: created in the head grilling session.
- 2026-10-22: Phase 4 grill: a big button instead of touch pads — the aluminium skin rules out capacitive pads.
