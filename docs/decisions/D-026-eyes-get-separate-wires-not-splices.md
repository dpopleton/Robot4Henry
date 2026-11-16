---
id: D-026
title: Each eye gets its own Pico pins, including a second SPI bus, so only VCC is shared
status: accepted
date: 2026-11-11
area: organs/eyes
---
## Context
The eyes' wiring shared SCK, MOSI, DC, RST, VCC and GND between the two
displays, which meant six splices in the middle of the wires. Dan went
back to his older solid-core wire (fewer colours), and splicing solid
wire neatly is awkward. The eyes' Pico drives nothing else, so most of
its pins are free.

## Decision
- **Left eye** stays on SPI0: CS GP17, SCK GP18, MOSI GP19, DC GP20,
  RST GP21, GND pin 23.
- **Right eye** moves to SPI1: SCK GP10, MOSI GP11, DC GP12, RST GP13,
  CS GP14, GND pin 18.
- **VCC** is the only shared signal: both red wires go into the single
  3V3(OUT) hole (pin 36) and are soldered there together, with no
  mid-wire splice. 5V is still kept off the eyes (D-021).
- Each panel resets itself on start-up. The shared-RST workaround in
  `panels.py` is gone.

## Alternatives considered
- **Keep the shared bus and splice six wires.** Fewer Pico pins, but
  six joints mid-wire, each needing heatshrink and a place to sit.
- **Split only GND, DC and RST, keep one SPI bus.** Still leaves two
  splices (SCK, MOSI); SPI1 is free, so there's no reason to.

## Consequences
- No desync: the eyes move together because the firmware draws them in
  turn each frame, same as before.
- Each SPI bus drives one display over a shorter wire, which should make
  40MHz more reliable, not less.
- Two separate bundles of six wires (plus the shared red), one per eye.
  The same colour can mean the same signal in both bundles.
- Uses 5 more Pico pins (GP10–14). GP16 is now free.
