---
id: D-002
title: Eyes draw into a RAM framebuffer and push one SPI write per eye
status: accepted
date: 2026-10-07
area: organs/eyes
---
## Context
Drawing straight to the GC9A01 panels set a window and wrote pixels per
scanline, from Python. That's slow, and the panel showed every half-drawn
step (flicker). Fast eye movement needs cheap redraws.

## Decision
`firmware/framebuffer.py` draws shapes with MicroPython's built-in
`framebuf` (C code) into a 115KB RAM buffer, then sends the whole frame in
one SPI write (~23ms per eye at 40MHz). Both eyes share one buffer, each
rendering and sending in turn.

## Alternatives considered
- **Keep per-scanline drawing.** Simple, but slow and flickery.
- **Two separate buffers.** Fits in the Pico 2's RAM, but wastes 115KB for
  no gain, since the eyes are drawn one after the other anyway.

## Consequences
- Redraw cost is roughly fixed, whatever the expression.
- Colours are byte-swapped in the driver (framebuf stores little-endian,
  the panel reads big-endian).
- Needs MicroPython ≥ 1.20 for `framebuf.ellipse` and `framebuf.poly`.
- **Not yet verified on hardware** — see R-201.
