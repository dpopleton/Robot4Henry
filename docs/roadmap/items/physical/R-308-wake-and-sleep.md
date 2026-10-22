---
id: R-308
title: "Wake and sleep"
phase: 3
status: planned
area: brain
kind: both
depends_on: []
decisions: [D-010, D-012, D-014]
cost_gbp: 2
updated: 2026-10-14
---
## Goal
A button hidden in the crown wakes Qbot. Button, "goodnight" or a silence timeout puts it to sleep. Asleep = mics and cameras off.

## Why
Qbot won't run 24/7, and listening is limited to when someone woke it (D-010).

## Tasks
- [ ] Button hidden in the crown (R-302)
- [ ] Crown Pico reads it and reports presses over serial, even while asleep (D-014)
- [ ] Sleep triggers: button, "goodnight", timeout (existing 5-minute session timeout)
- [ ] Asleep: crown stops streaming, eyes show sleeping
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Pressing the button wakes Qbot and it listens; going to sleep turns the mics off and the recording LED goes out.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: button hidden in the crown; which Pico reads it is open (shared with R-313).
- 2026-10-14: Phase 3 grill: the crown Pico reads the button (D-014).
