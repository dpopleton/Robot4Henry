---
id: D-014
title: The crown Pico handles everything on the crown, including the wake button
status: accepted
date: 2026-10-14
area: crown
---
## Context
The wake button is hidden in the crown (R-308) and has to work while Qbot is
asleep, when the crown has stopped streaming audio (D-010). Touch pads sit
around the crown on the top panel (R-313). Something has to read them.

## Decision
The crown's Pico 2 reads the wake button and reports presses over its serial
port (D-005), asleep or awake, alongside the mics and the recording LED.
The touch pads probably go on it too.

## Alternatives considered
- **The lights Pico.** MicroPython is easier than C, but it needs wires run
  from the crown down into the head.
- **A small Pico of its own for the top of the head.** Clean separation, but
  one more board, USB port and enclosure for a single button.

## Consequences
- One board and one connector for the whole crown, which simplifies its
  layout and design.
- The button handling is written in C, in the crown firmware (R-303).
- The crown Pico stays powered while asleep; only streaming stops.
