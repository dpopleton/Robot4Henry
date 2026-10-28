---
id: R-306
title: "Speakers, amplifier and enclosures"
phase: 3
status: planned
area: head
kind: both
depends_on: [R-212, R-213, R-210]
decisions: [D-013, D-017]
cost_gbp: 3
updated: 2026-10-28
---
## Goal
Two speakers salvaged from a broken soundbar (**5.5 cm, 4 Ω, 5 W**), each in
its own sealed box behind the bottom-corner openings of the front plate,
either side of the mouth screen. They're driven by the soundbar's own
**Jieli R30 PLUS** board, a USB sound card and stereo amp in one, on the
head's hub (D-013, D-017).

## Why
Qbot needs a voice. Sealed, stuffed boxes stop sound carrying into the head
and the crown's mics.

## What we know (tested 2026-10-28)
- On Ubuntu the board shows up as a standard USB sound card with no drivers:
  `card N: PLUS [R30 PLUS]`, USB ID `5943:3130` (Jieli Technology).
- `speaker-test -D plughw:CARD=PLUS,DEV=0 -c 2 -t wav` plays cleanly on both
  channels. The "Bad address" error on Ctrl+C is harmless.
- `amixer -c PLUS` offers only mute switches, so **the host can't set the
  hardware volume**. Volume lives inside the Jieli chip and is set by an
  endless rotary encoder (not a pot).
- The chip **forgets the volume at power-off**, and its power-on default is
  too quiet to use. Fix: the mouth Pico turns the "knob" itself (D-017).
- It has **Bluetooth**, which stays on for now (R-314).

## Tasks
### Speakers and boxes
- [x] Speakers and amp board salvaged and tested working (soundbar enclosure discarded)
- [ ] Measure the cone and surround diameter; the front opening must clear the surround
- [ ] Onshape: speaker panel with the 5 cm opening bevelled/flared at the back to take the 5.5 cm frame, through the 1.5 cm-thick face; nothing sticks out
- [ ] Design and print a sealed box per speaker: solid 2–3 mm walls, seams and wire hole sealed with hot glue
- [ ] Closed-cell foam gasket between the speaker rim/box and the plate; mount the boxes on rubber/foam washers
- [ ] Fill each box loosely (half to two-thirds) with polyester fibre stuffing, kept off the back of the cone
- [ ] Check whether the soundbar had a passive radiator worth reusing in a box
- [ ] Aluminium skin: parallel slots over each speaker, roughly a third to a half open over the cone, speaker cloth/mesh behind, and the aluminium fixed firmly around the speakers so it doesn't buzz (with R-402)
- [ ] Speakers each on their own +/− pair (never a speaker − to ground), both the same way round
- [ ] Check the shell doesn't buzz at the volume ceiling

### Volume (D-017)
- [ ] Find the encoder's A/B pins on the R30 board and measure their voltage. ≤3.3 V: wire them straight to the mouth Pico. Higher: one transistor/MOSFET per line. **Only ever pull the lines low, never drive them high** (open-drain)
- [ ] Count the clicks from the power-on default to a usable level, and to the loudest level that's OK for the kids
- [ ] Mouth Pico firmware: a `VOLUME` command that sends a fixed number of quadrature clicks. That count is the **hardware volume ceiling** and lives in the firmware, not the brain (R-210)
- [ ] Brain: notice the R30 PLUS appearing (udev rule or polling for `CARD=PLUS`), wait ~1 s, then tell the mouth Pico to set the volume, after every power-up or USB re-plug
- [ ] Software volume below the ceiling: scale samples in Python (or ALSA softvol), clamped at a maximum (R-307)
- [ ] Always address the device by name (`plughw:CARD=PLUS,DEV=0`), never by card number; make it the brain computer's default output
- [ ] If the encoder trick proves unreliable, fall back to a USB audio dongle + PAM8403 amp board (a few £, no Bluetooth), and note it in D-017

### Power
- [ ] Start on a hub port that can give ~1 A with data (R-213); the volume ceiling keeps the draw down. Measure it at the ceiling, and only add a separate 5V feed if it browns out or hums. Watch for motor noise later (R-502)

## Done when
Qbot's audio plays clearly from both speakers at a usable volume straight
after power-up, can't go above the firmware ceiling, and doesn't buzz the shell.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: speaker moved from bottom centre to two compartments in the
  front plate's bottom corners, either side of the mouth. Audio path decided:
  a USB sound card in the head (D-013).
- 2026-10-22: parts to order in the next two weeks, after the crown parts (Henry chose crown first).
- 2026-10-22: head electronics review: compartments are 5 × 5 cm on the face, with room behind; 40 mm 3 W 4 Ω drivers suggested.
- 2026-10-22: USB-C powered amp instead of cutting a cable; separate sound card unless the hub's charging port carries data.
- 2026-10-22: considered a combined sound card + amp board (Pimoroni Picade Max USB Audio); chose separate sound card + USB-C amp so the inside looks like a robot through the clear back panel.
- 2026-10-22: final choice: Picade Max USB Audio — one board, one USB-C lead, no extra mic, and it looks and works best behind the clear back. Replaces the separate sound card + PAM8403 plan.
- 2026-10-22: speakers: bare 40 mm 4 Ω 2–3 W drivers in our own printed boxes (for fun), rather than pre-boxed ones.
- 2026-10-28: salvaged a broken soundbar: two 5.5 cm 4 Ω 5 W speakers and its Jieli R30 PLUS USB/Bluetooth amp board, all tested working on Ubuntu. They replace the Picade Max and the 40 mm drivers, so nothing to buy except foam, stuffing and cloth (D-017). The power-on volume is too quiet and the host can't set it, so the mouth Pico will emulate the volume encoder. Bluetooth accepted for now (R-314).
