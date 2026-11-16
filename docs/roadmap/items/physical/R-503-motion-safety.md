---
id: R-503
title: "Motion safety"
phase: 5
status: idea
area: body
kind: both
depends_on: [R-501]
decisions: []
cost_gbp: 15
updated: 2026-11-16
---
## Goal
Speed limits, bump sensors, drop sensors (stairs), and an easy-to-reach stop button.

## Why
A heavy tracked robot around a 3-year-old is the most concrete safety risk in the project.

## Tasks
- [ ] Speed limit: walking pace or slower
- [ ] Bump sensors
- [ ] Drop sensors at the front edge
- [ ] Stop button, which also stops the neck and, later, the arms (R-701)

## Done when
Part of Phase 5's definition of done: the body can't drive off a step or push hard into someone.

## Open questions
- What a bump sensor does (stop, back off, or both): decided at the time.
- Stop button: cut motor power in hardware, or ask the motor Pico to stop? Decided later. Either way it must reach every moving part: a hardware cut has to include the arm motors' power, and a software stop needs every motion Pico to listen.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-11-03: Phase 5 grill: the speed limit is walking pace or slower. What a bump does, and whether the stop button cuts power in hardware or asks the Pico to stop, are decided at the time. Rough cost for sensors and button added.
- 2026-11-16: Phase 7 grill: the stop button covers the arms too.
