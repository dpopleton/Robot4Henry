---
id: R-202
title: "Eyes enclosure and soldering"
phase: 2
status: next
area: organs/eyes
kind: physical
depends_on: [R-201, R-212]
decisions: []
cost_gbp: 3
updated: 2026-10-22
---
## Goal
Build the eyes' enclosure and solder the screens and Pico permanently, mounted in the head's front frame.

## Why
Breadboard jumpers are fragile and noisy at 40MHz SPI.

## Tasks
- [x] Design the eye panel to bolt into the front main panel (R-212)
- [ ] Pico mounted on the back of the enclosure, short USB lead to the head hub (R-213)
- [x] Print
- [ ] Solder and check wiring against anatomy/eyes/build.md
- [ ] Photos into anatomy/eyes/images/

## Done when
The eyes are soldered, mounted in the head, and pass R-201's checks again.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: front plate is modelled; Pico sits on the enclosure.
- 2026-10-14: weekly review: enclosure to be designed by Friday so the eyes go in at next week's head assembly with Henry. Designing doesn't need R-201; soldering does.
- 2026-10-22: eye panel printed. Soldering stopped: the old iron wasn't up to it; a Miniware TS21 is on its way.
