---
id: D-024
title: The talking mouth follows voice levels sent from the laptop, not a signal the mouth Pico listens to
status: accepted
date: 2026-11-05
area: organs/mouth
---
## Context
While Qbot talks, the mouth (R-210) shows a seismograph-style wave whose
height follows the voice. Something has to measure how loud the voice is
moment to moment. R-210 left open whether that's the laptop or the mouth Pico.

## Decision
The laptop works out the levels from the text-to-speech audio (R-307) and
sends them as `L0`–`L100` lines, about 25 a second, in step with playback.
`S1`/`S0` mark talking on and off. With `S1` and no levels, the mouth
wiggles by itself, so it works before text-to-speech does and if levels
stop arriving.

## Alternatives considered
- **The mouth Pico reads the speaker signal on an ADC pin.** Exactly in
  time with what plays, but it needs an analog circuit beside the amp board
  (D-017), and the virtual robot (D-012, D-023) couldn't fake it.

## Consequences
- The voice audio is known before it plays, so levels can be computed in
  advance and sent alongside it. Lip-sync is tuned with the fixed offset
  already on R-210, by eye.
- The virtual robot and the real mouth get the same bytes, so lip-sync can
  be judged on the dev machine.
- If the sound board ever plays something the laptop didn't send (e.g.
  Bluetooth from a phone, R-314), the mouth won't move. That's fine.
