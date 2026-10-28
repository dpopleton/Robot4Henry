---
id: R-313
title: "Qbot reacts to a pat"
phase: 3
status: idea
area: head
kind: both
depends_on: [R-308]
decisions: [D-012, D-015, D-016]
cost_gbp: 0
updated: 2026-10-22
---
## Goal
Pressing the big button on top of the head while Qbot is awake counts as a pat
on the head, and he reacts to it.

## Why
Dan wants Qbot to feel it when someone touches him, not only hear them. The
button itself is the wake button (R-308, D-015), so this item is only about
what a pat does.

## Tasks
- [ ] Send a "patted" event from the router to the brain; decide what Qbot does with it
- [ ] Works in the virtual robot (D-012): fakes a press as input (a click on the top of the head)

## Done when
Patting the top of the head while Qbot is awake reliably makes him react.

## Log
- 2026-10-14: created in the head grilling session.
- 2026-10-22: Phase 4 grill: a big button instead of touch pads — the aluminium skin rules out capacitive pads.
- 2026-10-22: head electronics review: a large 3D-printed mechanical button.
- 2026-10-22: the big button is the wake button (D-015); hardware moved to R-308, this item is just the pat reaction.
- 2026-10-22: any press while awake is a pat; the button never means sleep (D-016).
