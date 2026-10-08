# Mouth — build notes

The physical side of the mouth: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
A rectangular display (already bought — probably an ST7789-type TFT), on its
own Pico (D-009). Shows a flat-line mouth, mood shapes when quiet, and
sound-wave shapes while Qbot talks.

## Status
- [ ] Find the display and identify it
- [ ] Wiring
- [ ] Mount in the front frame

## Open questions
- How are the sound waves driven? Levels from the laptop, or the mouth Pico
  reading the speaker signal on an ADC pin?

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| Rectangular TFT display | 1 | (bought) | find it |
| Raspberry Pi Pico 2 | 1 | ~£5 | |
