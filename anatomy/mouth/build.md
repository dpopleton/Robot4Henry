# Mouth — build notes

The physical side of the mouth: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
A SEENGREAT 2" IPS LCD module (Amazon code X001LUD8NR), on its own Pico
(D-009). Listings for this module say 240×320 with an ST7789V(W)
controller; we use it sideways (320×240). It has a plug-in header and 8
solder holes, including a backlight pin (BL), so brightness can be
controlled. White lines on black: flat when quiet, a mouth-shaped
seismograph while Qbot talks (R-210).

## Status
- [x] Find the display and identify it (2026-11-05)
- [ ] Wiring
- [ ] Mount in the front frame

## Open questions
- Pin order on the board (check the silkscreen): expected VCC, GND, DIN, CLK, CS, DC, RST, BL.
- Sound waves are driven by levels from the laptop (D-024), so no audio wiring to the mouth.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| SEENGREAT 2" IPS LCD (ST7789, 240×320) | 1 | (bought) | X001LUD8NR |
| Raspberry Pi Pico 2 | 1 | ~£5 | |
