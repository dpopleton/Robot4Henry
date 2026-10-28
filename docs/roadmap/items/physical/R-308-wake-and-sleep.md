---
id: R-308
title: "Wake and sleep"
phase: 3
status: planned
area: brain
kind: both
depends_on: []
decisions: [D-016, D-012, D-015]
cost_gbp: 2
updated: 2026-10-22
---
## Goal
The big button on top of the head wakes Qbot (D-015). "Goodnight" or a silence timeout puts it to sleep; the button never does (D-016). Asleep = mics and cameras off.

## Why
Qbot won't run 24/7, and listening is limited to when someone woke it (D-016).

## Tasks
- [ ] Large 3D-printed mechanical button cap over a microswitch, on top of the head through the aluminium skin
- [ ] Lights Pico reads it and reports presses over serial, even while asleep (D-015, R-211)
- [ ] Router tells the crown to start/stop streaming on wake/sleep
- [ ] Sleep triggers: "goodnight" and the silence timeout (existing 5-minute session timeout). No sleep button
- [ ] While awake, a press is passed on as a pat (R-313)
- [ ] Asleep: crown stops streaming, eyes show sleeping
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Pressing the button wakes Qbot and it listens; saying "goodnight" or going quiet long enough puts it to sleep, the mics go off and the recording LED goes out.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: button hidden in the crown; which Pico reads it is open (shared with R-313).
- 2026-10-14: Phase 3 grill: the crown Pico reads the button (D-014).
- 2026-10-22: the big button on top is the wake button, read by the lights Pico (D-015, supersedes D-014). No hidden button in the crown.
- 2026-10-22: no sleep button: the button only wakes (a press while awake is a pat); sleep is "goodnight" or the timeout; on/off switch on the body (D-016).
