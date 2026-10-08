---
id: R-308
title: "Wake and sleep"
phase: 3
status: planned
area: brain
kind: both
depends_on: []
decisions: [D-010]
cost_gbp: 2
updated: 2026-10-08
---
## Goal
A button on top of the head wakes Qbot. Button, "goodnight" or a silence timeout puts it to sleep. Asleep = mics and cameras off.

## Why
Qbot won't run 24/7, and listening is limited to when someone woke it (D-010).

## Tasks
- [ ] Button + which Pico reads it
- [ ] Sleep triggers: button, "goodnight", timeout (existing 5-minute session timeout)
- [ ] Asleep: crown stops streaming, eyes show sleeping

## Done when
Pressing the button wakes Qbot and it listens; going to sleep turns the mics off and the recording LED goes out.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
