---
id: R-210
title: "Mouth display"
phase: 2
status: in-progress
area: organs/mouth
kind: both
depends_on: []
decisions: [D-008, D-009, D-012, D-017, D-023, D-024]
cost_gbp: 5
updated: 2026-11-18
---
## Goal
A 2" display (already bought) showing white lines on black: a flat line
when Qbot is quiet, and while he talks a seismograph in a mouth shape:
spikes up and down from the line, tallest in the middle and fading to the
corners, flickering constantly, their height following his voice.

## Why
Part of the face; shows that Qbot is speaking.

## Tasks
- [x] Find the display and identify it: SEENGREAT 2" IPS module (X001LUD8NR), 8 pins incl. backlight; almost certainly ST7789V(W), 240×320, used landscape 320×240
- [x] Shared Pico code in `organs/pico_common/` (framebuffer, serial line reader) used by eyes and mouth; crash-watch shared by every organ driver
- [x] Firmware drawing + protocol in plain Python: flat line, talking seismograph (`S1`/`S0`, `L0`-`L100`, self-wiggle with no levels — D-024)
- [x] Host driver `organs/mouth/driver.py`
- [x] `virtual_robot/` app, `--only mouth` bench (D-023): talk toggle, fake "say a sentence" levels, real Pico switchable alongside
- [x] ST7789 driver + `main.py`; confirm the controller and resolution on a breadboard; own Pico (D-009), framebuffer approach as the eyes
- [x] Rewire onto the head's Pico and deploy to it
- [x] Whether mood shows on the mouth: no. Henry likes it as it is (2026-11-15)
- [x] Mouth panel printed (reprinted once: the bolt holes were off)
- [x] Mount centre-bottom of the front plate, between the speaker compartments (R-306); Pico on the back of the mount
- [x] Works in the virtual robot (D-012): a mouth panel + controls, and `--only mouth` bench mode with the real Pico switchable alongside (D-023); decide what it fakes as input and what it only displays
- [ ] **Volume knob emulation (D-017):** two GPIO + GND to the R30 PLUS board's encoder A/B lines, open-drain (only ever pull low; transistor per line if the lines are above 3.3 V). A `VOLUME` command sends a fixed number of quadrature clicks; that count is the hardware volume ceiling and lives in the firmware (R-306)
- [ ] Mouth sync: a fixed offset between playback start and the mouth's PLAY trigger, tuned by eye

## Done when
The mouth shows a flat line when Qbot is quiet and moves while he talks, mounted in the head.

## Open questions
- Settled 2026-11-15: no mood on the mouth. Henry played with the bench and wants no changes. The protocol still has room for an `E` field if that ever changes.
- Settled 2026-11-17: 240×320 confirmed; works with the build.md pinout. V vs VW unknown, same commands either way

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: position fixed: centre-bottom, between the two speakers.
- 2026-10-28: the mouth Pico also sets the salvaged sound board's volume by emulating its encoder (D-017), since it sits beside the speakers and already follows speech.
- 2026-11-05: the mouth is the first organ built on per-organ virtual panels with a bench mode (D-023).
- 2026-11-05: plan agreed. Display identified as a SEENGREAT 2" ST7789-type module. White on
  black; flat when quiet, a mouth-shaped seismograph while talking, driven by levels from the
  laptop (D-024). Whether mood shows on the mouth is Henry's to decide.
- 2026-11-05: step 1 done: `organs/pico_common/` (framebuffer + line reader), the
  crash-watch moved to `nervous_system/pico_console.py`, and `organs/deploy.py`
  copies an organ's firmware plus the shared files. The eyes run on it on the real
  Pico (101 random commands and junk lines, no crash).
- 2026-11-05: step 2 done: `organs/mouth/firmware/` (geometry, protocol, `Mouth` with
  the seismograph and self-wiggle) with tests. Timed on the eyes' Pico 2: ~25ms to draw a
  talking frame plus ~31ms to push it at 40MHz, so frames are 80ms (12.5/s), not 50ms.
- 2026-11-05: step 3 done: `MouthOrgan`, the mouth's virtual panel and controls, and the first
  `virtual_robot/` (`python -m virtual_robot --only mouth`) with the Off/Virtual/Real/Both switch
  and crash watch. Checked in the real window, and against the eyes' Pico for Both and a crash.
- 2026-11-05: the bench's "Say it" now speaks in Qbot's real Piper voice through the computer's
  speakers, drives the mouth from levels worked out from that audio (`organs/mouth/levels.py`), shows
  subtitles, and has a Sync slider for tuning lip-sync by eye (the robot needs its own value).
- 2026-11-16: weekly review: Henry played with the bench (typing things for Qbot to say) and wants it as it is, so no mood on the mouth. The mouth panel was printed; the bolt measurements were off, so it was reprinted.
- 2026-11-17: planned pinout added to `anatomy/mouth/build.md` (the left eye's SPI0 pins, backlight on GP16, volume encoder on GP2/GP3), with flashing, running and breadboard test steps. The ST7789 driver and `main.py` should use these pins.
- 2026-11-17: mouth wired. It answered `S0` with a NameError (no `main.py` yet), so wrote `st7789.py`, `mouth_panel.py` (pins as build.md) and `main.py`, deployed: runs and takes commands without crashing. Controller/resolution still to confirm by eye.
- 2026-11-17: Dan checked the screen: works and looks right with the default settings. Left: rewire onto the Pico that goes in the head, and mount on the plate.
- 2026-11-18: virtual-robot task ticked (the `--only mouth` bench covers it); bracket text for Henry approved.
- 2026-11-18: Dan installed the mouth: rewired onto the head's Pico, flashed, mounted in the front frame and tested; all looks good. Bracket drawing and model added to `anatomy/mouth/`. Left: volume knob emulation (R-306) and lip-sync tuning on the robot.
