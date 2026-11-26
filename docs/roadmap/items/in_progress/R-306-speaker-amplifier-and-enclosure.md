---
id: R-306
title: "Speakers, amplifier and enclosures"
phase: 3
status: in-progress
area: head
kind: both
depends_on: [R-212, R-213]
decisions: [D-013, D-017, D-027]
cost_gbp: 3
updated: 2026-11-26
---
## Goal
Two speakers salvaged from a broken soundbar (**5.5 cm, 4 Ω, 5 W**), each in
its own sealed box behind the bottom-corner openings of the front plate,
either side of the mouth screen. They're driven by a **Waveshare USB TO
AUDIO** (USB sound card + 2.6 W stereo amp) on the head's hub, with the
volume set from the laptop (D-013, D-027).

## Why
Qbot needs a voice. Sealed, stuffed boxes stop sound carrying into the head
and the crown's mics.

## What we know
**Waveshare USB TO AUDIO (tested 2026-11-25):** full notes in
`anatomy/head/build.md`.
- Shows up as `USB PnP Audio Device` (`CARD=Device`, USB ID `0c76:1203`).
- `amixer -c Device -- sset Speaker -20dB` sets a real playback volume
  (0–1008, −∞ to 0 dB, plus mute). Each labelled 10 dB step is ~5–6 dB at the mic.
- Both channels work; at −20 dB it's already louder than the R30 board at
  its power-on level.
- **No trim screw** on this model, so there's no hardware ceiling below the
  amp's own maximum. That's accepted for now (D-027): the software clamp is
  the limit. If over-loud audio ever comes up, put a resistor (a few ohms,
  a couple of watts) in series with each speaker. Not an action item.

**R30 PLUS board (the fallback, D-017):** measured 2026-11-22. Jieli AC6955F
(3.3 V IO) and an LTK5209 amp; host can only mute it; the knob gives +38 dB.
It also has Bluetooth. Kept in the parts box.

## Tasks
### Speakers and boxes
- [x] Speakers and amp board salvaged and tested working (soundbar enclosure discarded)
- [ ] Measure the cone and surround diameter; the front opening must clear the surround
- [x] Onshape: speaker panel with the 5 cm opening bevelled/flared at the back to take the 5.5 cm frame, through the 1.5 cm-thick face; nothing sticks out (printing 2026-11-26)
- [x] ~~Trial a ~100–120 ml box against ~250 ml~~ dropped 2026-11-26: it's only for a voice, so straight to the ~5 × 5 × 7 cm box
- [x] Design and print a sealed box per speaker (~5 × 5 × 7 cm outside, ~110–130 ml inside): both printed 2026-11-26
- [ ] Fit the speakers into the boxes: solid 2–3 mm walls, seams and wire hole sealed with hot glue
- [ ] Closed-cell foam gasket between the speaker rim/box and the plate; mount the boxes on rubber/foam washers: rubber on both sides of each mounting tab (the head side has heat inserts), bolt not touching the tab's hole (oversized hole or sleeved grommet); snug, with the rubber only slightly squashed
- [ ] Fill each box loosely (half to two-thirds) with fluffed-up yarn (cut short, untwisted; wool best), kept off the back of the cone
- [ ] Aluminium skin: parallel slots over each speaker, roughly a third to a half open over the cone, speaker cloth/mesh behind, and the aluminium fixed firmly around the speakers so it doesn't buzz (with R-402)
- [ ] Speakers each on their own +/− pair (never a speaker − to ground), both the same way round
- [ ] Check the shell doesn't buzz at full volume

### Waveshare USB TO AUDIO (bought 2026-11-23, chosen 2026-11-26: D-027)
- [x] Check whether it drives one speaker or two, and whether the speakers' plug fits
- [x] Play the tone sweep through it with the webcam mic, as for the R30 board, and check `amixer` gives a real playback volume
- [x] ~~Set the inside trim screw as the hardware volume ceiling~~: this model has no trim screw
- [x] Decision superseding D-017 (D-027); R-210, R-307 and R-314 updated

### Volume and safety (D-027)
- [ ] Software volume below that: scale samples in Python (or ALSA softvol), clamped at a maximum (R-307)
- [ ] Always address the device by name (`plughw:CARD=Device,DEV=0`), never by card number; pin it by USB ID or path (the name is generic); make it the brain computer's default output
- [ ] Set the mixer to a known level at startup, since a re-plug may reset it

### Power
- [ ] Start on a hub port that gives ~0.5–1 A with data (R-213). Measure the draw at full volume, and only add a separate 5V feed if it browns out or hums. Watch for motor noise later (R-502)

## Done when
Qbot's audio plays clearly from both speakers at a usable volume straight
after power-up, stays under the software volume clamp, and doesn't buzz the
shell.

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
- 2026-11-20: weekly review: speaker boxes and panels are next week's main design work; the mouth is mounted, so the space either side of it is fixed.
- 2026-11-22: measured the board and speakers with the webcam mic: both work, quiet at power-on, +38 dB available from the knob. Chips identified (AC6955F, LTK5209): 3.3 V IO, so the encoder wires go straight to the Pico. ~250 ml boxes took too much room, so a ~100–120 ml box is being tried first (smaller drivers considered, not needed yet). The white residue on the board is probably flux; to clean and check.
- 2026-11-23: unsure about soldering to the R30 board's trimmed encoder pins, and about how much work the encoder trick would be, so bought a Waveshare USB TO AUDIO (~£8: USB sound card + 2.6 W amp into 4 Ω, laptop-set volume, trim screw ceiling, JST-PH speaker plug). Compared against the Picade Max USB Audio (open firmware, screw terminals, UAC volume), PAM8403 + dongle, and ReSpeaker Lite. The R30 board stays as the fallback.
- 2026-11-25: Waveshare tested with both speakers plugged in, ~30 cm from the laptop's webcam mic: both channels play, 200 Hz–8 kHz clearly heard (nothing at 100 Hz, as with the R30, loose drivers). It shows up as `USB PnP Audio Device` (`CARD=Device`) with a real `Speaker` playback volume (0–1008, −∞ to 0 dB) that changes the loudness steadily. Its dB labels are about twice as steep as what the mic heard (~5–6 dB per 10 dB step). Next: the trim screw by ear, then the decision superseding D-017.
- 2026-11-26: first speaker box built, about 5 × 5 × 7 cm outside (~110–130 ml inside). No box-size trial or temporary sealing test: it's only for a voice, so the speakers go straight in, stuffed with fluffed-up yarn instead of polyester fibre.
- 2026-11-26: box mounts: rubber on both sides of each tab and the bolt clear of the hole, so the bolts into the heat inserts don't make a hard path to the head (crown side: R-302).
- 2026-11-26: weekly review: both boxes printed (speakers not in yet); speaker panels printing. The Waveshare has no trim screw. Dan is happy with it, so it replaces the R30 board (D-027); the encoder emulation is dropped. The hardware volume ceiling is still to settle: measure full volume, then a resistor per speaker if needed. R-210 no longer a dependency.
- 2026-11-26: Dan: no hardware ceiling for now; avoid bugs in the software clamp. The resistor per speaker is a fix to reach for only if it comes up.
