---
id: D-018
title: The Q and the inside of the head are lit by the soundbar's two LED boards on one chain
status: accepted
date: 2026-10-28
area: organs/lights
---
## Context
R-211 planned 4–5 loose WS2812Bs behind a diffuser for the forehead Q. The
salvaged soundbar (D-017) had two U-shaped WS2812-type boards, each with
9 LEDs and about 35 × 60 mm. The head's back panel is clear acrylic, so
lighting the inside would make the whole head glow through it.

## Decision
- **One U board lights the Q, the other lights the inside of the head.**
- They're **chained DOUT → DIN** on the lights Pico's single 3-wire LED
  connector (5V, GND, data). Dan already has the connectors. The firmware
  treats them as LEDs 0–8 and 9–17, so the Q and the glow can show the same
  thing or different things.
- The boards are used whole: no cutting or desoldering.
- Power still comes from the lights Pico's **VBUS**, with a **hard brightness
  cap in firmware** that keeps all 18 LEDs together well under the port's
  limit (~300 mA). No cut-up cables.

## Alternatives considered
- **A WS2812 ring (8 or 12 LEDs) for the Q**, sized to the 30 × 30 mm Q. A
  neater fit, but it's another purchase when a board is already in hand.
- **Both U boards for the interior glow** and loose LEDs for the Q. Uses
  more pins or a longer chain, for little gain.
- **4–5 loose WS2812Bs** (the old plan): more soldering, and no glow.
- **Feed the LEDs from the head's 5V supply.** Full brightness, but it needs
  power distribution that the head doesn't otherwise have (R-213).

## Consequences
- The Q's diffuser and mount must take a 35 × 60 mm board behind a 30 × 30 mm Q.
- The glow must not make the recording and video LEDs ambiguous: they go
  in their own sealed light boxes (D-007). The camera needs shielding from
  the glow, and the display edges need checking for leaks.
- The cap limits how bright the head can get. If that's too dim, revisit
  the power feed (R-213).
- The loose WS2812Bs already bought become spares.
