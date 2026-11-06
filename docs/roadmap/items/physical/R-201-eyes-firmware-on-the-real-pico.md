---
id: R-201
title: "Eyes firmware on the real Pico"
phase: 2
status: next
area: organs/eyes
kind: both
depends_on: []
decisions: [D-001, D-002]
cost_gbp: 0
updated: 2026-11-05
---
## Goal
Run the new eyes firmware (framebuffer drawing, wire format, command listener) on the real Pico and screens.

## Why
The old bring-up test ran on hardware, but none of the new code has. MicroPython-only parts (framebuf.ellipse/poly, polling stdin) are unverified.

## Tasks
- [ ] Flash all firmware files (see organs/eyes/README.md)
- [ ] Check bringup.py still works
- [ ] Check main.py: send lines by hand from a serial terminal (picocom)
- [x] Simulator can drive the real eyes ("Use physical hardware" tick box)
- [ ] Check every mood at intensities 1-3 against the simulator
- [ ] Note how fast it actually redraws

## Done when
Every mood × intensity shows correctly on the real screens, driven from the host driver.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-28: `organs/eyes/simulate.py` gained a "Use physical hardware" tick box that
  sends every button/command to the Pico through the real host driver, for the side-by-side check.
- 2026-11-03: the TS21 iron has arrived; no time to flash or solder this week. Flashing on a breadboard doesn't need the iron.
- 2026-11-05: first side-by-side run with the simulator. The real eyes froze a few
  expressions in: `main.py` crashed because MicroPython's `math` has no `hypot()`
  (used by `_thick_line`, which draws `dead` and `scared` at intensity 2-3). Swapped it
  for `sqrt`, added a test that firmware only uses `math` functions MicroPython has,
  and the Pico ran 100 random commands without crashing.
- 2026-11-05: the simulator now watches the Pico's output while "Use physical hardware"
  is ticked. If `main.py` stops, the error shows under the tick box and the full
  traceback goes to the terminal, so a crash no longer looks like a silent freeze.
  Tested with Ctrl-C on the real eyes.
