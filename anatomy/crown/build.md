# Crown — build notes

The physical side of the crown: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
A crown on top of the head hiding a four-mic array: **two at the front
stacked vertically** (for height), **one left, one right**. A Pico 2 reads
the four I2S MEMS mics in sync and appears to the brain computer as a USB
microphone plus a serial port (D-004, D-005). A **recording LED** is driven
by the crown Pico itself whenever it's streaming (D-007).

## Status
- [ ] Buy the parts (R-301)
- [ ] Breadboard and measure the mic boards
- [ ] Design the crown around them (R-302)

## Design rules
- Left/right mics as far apart as the head allows.
- Front pair as far apart **vertically** as possible (crown top + brow?) —
  close together, height can only be guessed coarsely.
- Each mic needs an open hole (a few mm) with the board pressed against it
  from inside. Don't cover it with crown material.
- Mount on foam, away from the speaker.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| Raspberry Pi Pico 2 | 1 | ~£5 | |
| INMP441-type I2S MEMS mic board | 4 | ~£3 each | |
| Raspberry Pi Debug Probe | 1 | ~£12 | for C firmware debugging |
