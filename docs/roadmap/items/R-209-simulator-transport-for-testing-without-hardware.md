---
id: R-209
title: "Simulator transport for testing without hardware"
phase: 2
status: planned
area: organs/eyes
kind: code
depends_on: [R-207]
decisions: []
cost_gbp: null
updated: 2026-10-08
---
## Goal
A transport that drives the Tk simulator instead of the Pico, so you can chat in the terminal and watch the simulated eyes react.

## Why
Lets the whole brain → router → eyes chain be tested anywhere.

## Tasks
- [ ] Transport that feeds lines into simulate.py (pipe/socket)
- [ ] Document how to run it

## Done when
`python main.py` with the simulator transport shows the mood changing on screen.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
