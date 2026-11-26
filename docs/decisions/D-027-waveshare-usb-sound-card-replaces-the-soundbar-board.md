---
id: D-027
title: A Waveshare USB sound card drives the speakers instead of the soundbar's board; the laptop sets the volume
status: accepted
date: 2026-11-26
area: head
---
## Context
D-017 made the salvaged soundbar's R30 PLUS board the head's sound card. Its
volume can only be changed with its rotary encoder, so the mouth Pico was
going to pretend to turn the knob after every power-up, and that click count
was to be the hardware volume ceiling.

Measuring the board (2026-11-22) showed the trick would work (3.3 V lines,
+38 dB available), but Dan wasn't keen on soldering to its trimmed encoder
pins, or on how much firmware and brain work the trick needed. He bought a
**Waveshare USB TO AUDIO** (~£8: USB sound card plus a 2.6 W amp into 4 Ω)
and tested it with both salvaged speakers on 2026-11-25. Both channels play,
and it has a real playback volume the laptop can set
(`amixer -c Device -- sset Speaker …`). This model has **no trim screw**.

## Decision
- **The Waveshare drives the two salvaged 5.5 cm speakers.** D-013 still
  holds: it's a USB sound card on the head's hub.
- **The laptop sets the volume** through ALSA. No encoder emulation, no
  `VOLUME` command on the mouth Pico.
- **No Bluetooth:** the Waveshare has none, so R-314's question goes away.
- The R30 PLUS board is kept in the parts box as a **fallback**, with
  D-017's plan still on file.
- Address it by name (`plughw:CARD=Device,DEV=0`) and, because the name is
  generic, pin it by USB ID (`0c76:1203`) or USB path once it's on the hub.
- **No hardware volume ceiling for now.** With no trim screw, the loudest
  it can go is the amp's own maximum. The software clamp in the brain is the
  limit, and the aim is simply not to have bugs there. If over-loud audio
  ever actually comes up, the fix is a resistor in series with each speaker
  (R-306), but that isn't planned work.

## Alternatives considered
- **Keep D-017** (the R30 board with the mouth Pico turning the knob). It
  was free, louder, and gave a ceiling in firmware, but it meant soldering to
  the encoder pins, a firmware command, and a "sound card appeared" trigger
  in the brain. It also kept the open Bluetooth.
- **Picade Max USB Audio** (~£16.50): open firmware, screw terminals and a
  host-set volume. It was next in line if the Waveshare failed.
- **PAM8403 amp + USB dongle:** cheap, but more wiring for the same result.
- **ReSpeaker Lite:** more than the head needs, since the crown has the mics.

## Consequences
- R-210 loses its volume-knob task, and R-306 no longer depends on it.
- R-307 plays through `CARD=Device` and scales volume in software.
- R-314 is settled: there's no Bluetooth to worry about.
- Phase 3 loses its "hardware volume ceiling" safety need: the volume
  limit is in software, with a resistor per speaker kept as a fix if needed.
- It's quieter than the R30 board can be (~2.6 W against ~3 W per channel),
  but already louder at −20 dB than the R30 at its power-on level.
- Draw from the hub port is lower than the R30's (R-213).
