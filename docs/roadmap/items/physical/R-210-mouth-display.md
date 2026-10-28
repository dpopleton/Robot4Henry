---
id: R-210
title: "Mouth display"
phase: 2
status: planned
area: organs/mouth
kind: both
depends_on: []
decisions: [D-008, D-009, D-012, D-017]
cost_gbp: 5
updated: 2026-10-28
---
## Goal
A rectangular display (already bought) showing a flat-line mouth, sound-wave shapes while Qbot talks, and mood when quiet.

## Why
Part of the face; shows that Qbot is speaking.

## Tasks
- [ ] Find the display and identify it (ST7789?)
- [ ] Own Pico (D-009); reuse the eyes' framebuffer approach
- [ ] Flat line + mood shapes
- [ ] Sound waves while talking
- [ ] Mount centre-bottom of the front plate, between the speaker compartments (R-306); Pico on the back of the mount
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays
- [ ] **Volume knob emulation (D-017):** two GPIO + GND to the R30 PLUS board's encoder A/B lines, open-drain (only ever pull low; transistor per line if the lines are above 3.3 V). A `VOLUME` command sends a fixed number of quadrature clicks; that count is the hardware volume ceiling and lives in the firmware (R-306)
- [ ] Mouth sync: a fixed offset between playback start and the mouth's PLAY trigger, tuned by eye

## Done when
The mouth shows mood when quiet and moves while Qbot talks, mounted in the head.

## Open questions
- How are the sound waves driven — levels from the laptop, or the mouth Pico listening to the speaker signal on an ADC pin? (Decide when we get there.)
- Which display is it exactly?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: position fixed: centre-bottom, between the two speakers.
- 2026-10-28: the mouth Pico also sets the salvaged sound board's volume by emulating its encoder (D-017), since it sits beside the speakers and already follows speech.
