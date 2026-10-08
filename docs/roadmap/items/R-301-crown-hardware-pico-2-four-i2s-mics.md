---
id: R-301
title: "Crown hardware: Pico 2 + four I2S mics"
phase: 3
status: planned
area: crown
kind: physical
depends_on: []
decisions: [D-004]
cost_gbp: 30
updated: 2026-10-08
---
## Goal
Buy and breadboard the crown: Pico 2, four INMP441-type I2S MEMS mics (two front stacked vertically, left, right), plus a debug probe.

## Why
Dan wants to build it himself (D-004) and go straight to four mics.

## Tasks
- [ ] Buy: Pico 2 (~£5), 4× I2S mic boards (~£3 each), Raspberry Pi Debug Probe (~£12)
- [ ] Breadboard: shared clock, two data lines
- [ ] Measure the boards for the crown design

## Done when
Four mics capture in sync on a breadboard.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
