---
id: R-301
title: "Crown hardware: Pico 2 + four I2S mics"
phase: 3
status: planned
area: crown
kind: physical
depends_on: []
decisions: [D-004]
cost_gbp: 0
updated: 2026-11-26
---
## Goal
Buy and breadboard the crown: Pico 2, four INMP441-type I2S MEMS mics (two front stacked vertically, left, right), plus a debug probe.

## Why
Dan wants to build it himself (D-004) and go straight to four mics.

## Tasks
- [x] Buy: **2× Pico 2 bought (£4 each)**; 4× I2S mic boards: **5× INMP441 bought, £7**
- [ ] Only if the C firmware gets hard to debug: flash a spare Pico with `debugprobe` instead of buying the £12 Debug Probe
- [ ] Breadboard: shared clock, two data lines
- [ ] Measure the boards for the crown design

## Done when
Four mics capture in sync on a breadboard.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-22: Henry chose the crown before the speakers; parts to order in the next two weeks.
- 2026-10-22: Debug Probe dropped from the shopping list: BOOTSEL + UF2 to start; a spare Pico running debugprobe if needed.
- 2026-11-03: weekly review: the crown parts are still next to buy, but wait until the speakers and lights are in the head, since those parts are already in hand.
- 2026-11-06: weekly review: the mics and Pico 2 are the next purchase.
- 2026-11-20: weekly review: Dan is buying the Pico 2 and mics next week, with the hub (R-213).
- 2026-11-26: weekly review: 5 INMP441 mic boards bought (£7). Whether the Pico 2 was bought too is still to check.
- 2026-11-26: two Pico 2s bought (£4 each), so all the crown parts are in hand.
