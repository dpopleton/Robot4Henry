---
id: R-211
title: "Lights: glowing Q and antenna"
phase: 2
status: planned
area: organs/lights
kind: both
depends_on: []
decisions: [D-008, D-009, D-012]
cost_gbp: 12
updated: 2026-10-22
---
## Goal
Multi-colour LEDs behind diffusers for the Q on the forehead and the antenna tip.

## Why
A second way to show mood/activity, and part of the look.

## Tasks
- [ ] Pick LEDs (WS2812-type, one data wire)
- [ ] Own Pico, probably (D-009)
- [ ] Diffusers in the shell
- [ ] Power the LEDs from the head's supply, not the Pico (R-213)
- [ ] Colour meanings: a small, easily extended table of state → colour with a few defaults for now (Henry wants colours to match actions once Qbot can do more than talk)
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
The Q and antenna light up from the router, mounted in the head.

## Open questions
- Colour meanings: Henry decided they'll match actions, later. For now, defaults (e.g. Q = mood, antenna = listening/talking).
- Own Pico or share one? (Not firm.)

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: LEDs powered from the head supply; may share a Pico with the wake button/touch.
- 2026-10-22: Henry: colours should match actions once Qbot can do more; build the setup with defaults and grow it.
