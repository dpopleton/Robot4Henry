---
id: R-202
title: "Eyes enclosure and soldering"
phase: 2
status: next
area: organs/eyes
kind: physical
depends_on: [R-201, R-212]
decisions: [D-021, D-022]
cost_gbp: 3
updated: 2026-11-04
---
## Goal
Build the eyes' enclosure and solder the screens and Pico permanently, mounted in the head's front frame.

## Why
Breadboard jumpers are fragile and noisy at 40MHz SPI.

## Tasks
- [x] Design the eye panel to bolt into the front main panel (R-212)
- [ ] Pico mounted on the back of the enclosure, short USB lead to the head hub (R-213)
- [x] Print
- [ ] Check the new firmware on the breadboard before soldering (R-201)
- [ ] Solder the wires straight into the Pico's holes, no header pins or Dupont (D-022); on the displays, solder to their existing pins
- [ ] Heatshrink every joint; hot glue or a cable tie holds each bundle near the board
- [ ] Check wiring against anatomy/eyes/build.md
- [ ] Photos into anatomy/eyes/images/

## Done when
The eyes are soldered, mounted in the head, and pass R-201's checks again.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: front plate is modelled; Pico sits on the enclosure.
- 2026-10-14: weekly review: enclosure to be designed by Friday so the eyes go in at next week's head assembly with Henry. Designing doesn't need R-201; soldering does.
- 2026-10-22: eye panel printed. Soldering stopped: the old iron wasn't up to it; a Miniware TS21 is on its way.
- 2026-11-03: the TS21 iron arrived; soldering not started yet (no time).
- 2026-11-04: bought wire was too thick for the connectors; using thinner spare wire in ten colours. Wiring colours updated so every eyes wire has its own colour and 5V gets orange (D-021, supersedes D-019).
- 2026-11-04: no Dupont: wires are soldered straight to the boards, with heatshrink and strain relief, after a breadboard firmware check (D-022). Tasks split out to match.
