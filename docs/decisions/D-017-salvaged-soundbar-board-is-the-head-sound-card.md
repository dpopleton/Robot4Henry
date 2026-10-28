---
id: D-017
title: The salvaged soundbar's board is the head's sound card; the mouth Pico sets its volume ceiling
status: accepted
date: 2026-10-28
area: head
---
## Context
D-013 put a USB sound card and amp in the head, and R-306 had settled on
buying a Pimoroni Picade Max with two 40 mm drivers. Then Dan found a broken
USB/Bluetooth soundbar. Only its case was damaged. The parts tested fine:
two 5.5 cm 4 Ω 5 W speakers and a **Jieli R30 PLUS** amp board that shows up
on Ubuntu as a standard USB sound card (`CARD=PLUS`, USB ID `5943:3130`).

The catch: the host can only mute it, not set its volume. Volume lives in
the chip and is changed with an endless rotary encoder. The chip forgets it
at power-off, and the power-on default is too quiet.

## Decision
- **Use the soundbar's board and speakers** instead of the Picade Max and
  40 mm drivers. D-013 still holds: it's a USB sound card on the head's hub.
- **The mouth Pico emulates the volume encoder.** Its two GPIO lines sit on
  the encoder's A/B lines and only ever pull them low (open-drain, through a
  transistor if the lines are above 3.3 V). After every power-up or USB
  re-plug, the brain notices the card appear, waits ~1 s, and tells the mouth
  Pico to send a fixed number of clicks.
- **That click count is the hardware volume ceiling** and lives in the
  firmware, so a brain bug can't make Qbot louder than it. Quieter levels
  are done by scaling samples in software, clamped at a maximum.
- The device is always addressed by name (`CARD=PLUS`), never by card number.
- **Bluetooth stays** on the board for now (R-314).

## Alternatives considered
- **Picade Max USB Audio** (the previous plan). Volume can be set from the
  host, but it costs ~£21 with drivers, and these parts are free and already
  work.
- **USB audio dongle + PAM8403 amp.** A few pounds, and the volume is
  controllable, but it loses Bluetooth. Kept as the **fallback** if the
  encoder trick is unreliable.
- **Leave the encoder as a knob and turn it by hand after each power-up.**
  Easy to forget, and there's no ceiling.
- **Lights Pico for the encoder.** It's also in the head and stays on while
  asleep, but the mouth Pico sits next to the speakers and already ties
  itself to speech (mouth sync).

## Consequences
- The mouth Pico gains a `VOLUME` command and two GPIO + ground to the amp
  board (R-210), and R-306 now depends on the mouth.
- The brain needs a "sound card appeared" trigger (udev or polling).
- The ceiling is set by counting clicks on the real board, by ear.
- Two 5 W speakers can draw more than a hub port gives. The ceiling keeps the
  draw down; measure it before deciding on a separate 5V feed (R-213).
- Anyone nearby can pair a phone over Bluetooth and play audio through Qbot.
  That's acceptable while use is supervised (R-314).
