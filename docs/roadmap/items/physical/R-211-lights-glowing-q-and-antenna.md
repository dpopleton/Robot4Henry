---
id: R-211
title: "Lights: glowing Q, head glow and antenna"
phase: 2
status: planned
area: organs/lights
kind: both
depends_on: []
decisions: [D-007, D-008, D-009, D-012, D-015, D-018]
cost_gbp: 3
updated: 2026-10-28
---
## Goal
Multi-colour light for the Q on the forehead, the inside of the head
(glowing through the clear back panel), and the antenna tip.

## Why
A second way to show mood/activity, and part of the look.

## Tasks
- [x] LEDs for the Q and glow: the soundbar's two U-shaped WS2812-type boards (9 LEDs each, ~35 × 60 mm), salvaged and working (D-018)
- [ ] Chain the boards DOUT → DIN on one 3-wire connector (5V, GND, data) to the lights Pico: board 1 (LEDs 0–8) = Q, board 2 (LEDs 9–17) = glow. Don't cut or desolder the boards
- [ ] **Q:** mount board 1 behind a diffuser for the 30 × 30 mm Q, so no hotspots show
- [ ] **Head glow:** cardboard/printed mock-up first (board near the top pointing down, or set back), and show Henry for approval before designing mounts
- [ ] Glow: light-coloured inside surfaces for an even bounce; aim/diffuse the board so it doesn't hotspot through the back window; check the display edges for leaks
- [ ] Glow: recording and video LEDs in their own sealed light boxes so their status stays unambiguous (D-007); shield the camera from the glow (R-601)
- [ ] **Antenna tip:** one ordinary common-cathode RGB LED on three PWM pins with resistors, wired down from the top; if blue/green are too dim at 3.3V, switch it with transistors from 5V, or swap in a WS2812B
- [ ] Own Pico (D-009), MicroPython
- [ ] If the WS2812s flicker on 3.3V data, add a 74AHCT125 level shifter (~£1)
- [ ] **Hard brightness cap in firmware:** all 18 LEDs run from the Pico's VBUS pin, so cap their total at ~300 mA (well under the USB port's limit), whatever the router asks for (D-018)
- [ ] Read the big wake button on top of the head and report presses over serial, asleep or awake (D-015, R-308)
- [ ] Colour meanings: a small, easily extended table of state → colour with a few defaults for now (Henry wants colours to match actions once Qbot can do more than talk); the Q and glow can match or differ
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
The Q, the head glow and the antenna light up from the router, mounted in
the head, with the recording/video LEDs still clearly readable.

## Open questions
- Colour meanings: Henry decided they'll match actions, later. For now, defaults (e.g. Q = mood, antenna = listening/talking).
- Where the glow board sits: decided by the mock-up.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: LEDs powered from the head supply; may share a Pico with the wake button/touch.
- 2026-10-22: Henry: colours should match actions once Qbot can do more; build the setup with defaults and grow it.
- 2026-10-22: head electronics review: own Pico confirmed (an extra £5 Pico is fine); Q = 4–5 LEDs + diffuser, antenna tip = 1 LED wired down from the top.
- 2026-10-22: the lights Pico also reads the wake button (D-015) and stays running while Qbot is asleep.
- 2026-10-22: LED choice: a mix for now — WS2812B for the Q, a plain RGB LED for the antenna (for the PWM/transistor learning). Extra LEDs bought in case Henry wants more lights; may go all-WS2812B once started.
- 2026-10-28: the soundbar's two U-shaped LED boards replace the loose WS2812Bs: one behind the Q, one lighting the inside of the head through the clear back, chained on one connector (connectors already in hand). Still powered from VBUS, with a hard brightness cap for all 18 LEDs (D-018). The 2026-10-14 "head supply" note is superseded.
