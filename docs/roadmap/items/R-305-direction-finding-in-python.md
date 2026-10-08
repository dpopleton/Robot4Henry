---
id: R-305
title: "Direction-finding in Python"
phase: 3
status: planned
area: nervous_system
kind: code
depends_on: [R-303, R-207]
decisions: [D-006]
cost_gbp: null
updated: 2026-10-08
---
## Goal
Work out the speaker's direction from the four raw channels (GCC-PHAT) on the brain computer and feed it to the router.

## Why
Prototype where it's easy to see and tweak (D-006).

## Tasks
- [ ] Left/right from the L/R pair
- [ ] Front/back from the front mic
- [ ] Coarse up/level/down from the vertical pair
- [ ] Confidence + voice-active output
- [ ] Plots for tuning
- [ ] Feed the router (R-207)

## Done when
The eyes turn towards whoever is talking.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
