---
id: R-501
title: "Tracked chassis"
phase: 5
status: idea
area: body
kind: both
depends_on: [R-402]
decisions: [D-012, D-020]
cost_gbp: 60
updated: 2026-11-03
---
## Goal
A self-designed, 3D-printed tracked body, larger than the head, holding everything not in the head (including the laptop).

## Why
Movement is a real, long-term goal.

## Tasks
- [ ] Design tracks + drive
- [ ] Motor controller (own Pico, D-009)
- [ ] Sized a bit bigger than the laptop, with brackets so the brain computer can be swapped (R-504)
- [ ] Driven by Qbot itself: voice commands and/or wandering (D-020)
- [ ] Gamepad control for testing
- [ ] Indoor terrain of all sorts, maybe pavement
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Qbot drives itself around indoors, at walking pace or slower, and a gamepad can drive it for testing.

## Open questions
- Voice commands or wandering first? Decided nearer the time.
- Printed tracks (PETG/TPU) or bought rubber tracks with printed wheels? Printed body or aluminium beams like the head? Decided later.
- A first drive on a tether while the laptop sits beside it, or only untethered? Decided when we get there.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-11-03: Phase 5 grill: Qbot drives itself, on voice commands or wandering, with a gamepad only for testing (D-020). Walking pace or slower. The body is sized a bit bigger than the laptop, with a bracket system so the brain computer can be swapped. Starts after the head is finished. Rough cost for motors and driver added.
