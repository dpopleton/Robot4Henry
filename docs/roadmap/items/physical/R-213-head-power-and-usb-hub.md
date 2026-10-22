---
id: R-213
title: "Head power and USB hub"
phase: 2
status: planned
area: head
kind: physical
depends_on: [R-212]
decisions: [D-009, D-013]
cost_gbp: 20
updated: 2026-10-14
---
## Goal
A powered USB hub inside the head that every Pico, the USB sound card and
(probably) the camera plug into, plus a power supply for the hub, the
speakers' amp and the WS2812 LEDs. One USB lead and one power lead leave the
head through the bottom panel.

## Why
One Pico per organ (D-009) means 4–6 USB devices, and the amp, screens and
LEDs together draw more than the laptop's USB can supply. Nothing on the
roadmap covered this before. Putting the hub in the head keeps it to one
cable bundle (D-013).

## Tasks
- [ ] Add up the power budget: screens + backlights, WS2812s at full white,
      amp at the volume Qbot will actually use, Picos, camera
- [ ] Decide how the head is powered (see open questions)
- [ ] Pick a powered hub with enough ports and a small enough board to fit
- [ ] Mount the hub and power distribution inside, reachable through the back door
- [ ] Configure every organ's port by `/dev/serial/by-id/…`
- [ ] Route both leads out through the bottom panel's cable exit

## Done when
Every organ in the head runs from the hub at once (eyes animating, LEDs at
full brightness, Qbot speaking loudly) with no resets or brownouts, and only
one USB and one power lead leave the head.

## Open questions
- How is the head powered? A 5V supply (~4A) with a small distribution board
  feeding the hub, amp and LEDs is one option. Another is powering it all
  through the hub's ports. Or design around the future body battery (R-502).
- Which ports does the hub need: count of organs + sound card + camera + a spare?

## Log
- 2026-10-14: created in the head grilling session — power and the hub weren't
  on the roadmap. Hub inside the head decided; power supply still open.
