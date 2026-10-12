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
updated: 2026-10-08
---
## Goal
Run the new eyes firmware (framebuffer drawing, wire format, command listener) on the real Pico and screens.

## Why
The old bring-up test ran on hardware, but none of the new code has. MicroPython-only parts (framebuf.ellipse/poly, polling stdin) are unverified.

## Tasks
- [ ] Flash all firmware files (see organs/eyes/README.md)
- [ ] Check bringup.py still works
- [ ] Check main.py: send lines by hand from a serial terminal (picocom)
- [ ] Check every mood at intensities 1-3 against the simulator
- [ ] Note how fast it actually redraws

## Done when
Every mood × intensity shows correctly on the real screens, driven from the host driver.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
