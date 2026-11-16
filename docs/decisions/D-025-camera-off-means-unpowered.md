---
id: D-025
title: The camera's video LED runs off the camera's own 5V, so "camera off" means the camera has no power
status: accepted
date: 2026-11-06
area: organs/vision
---
## Context
D-007 says the video LED is driven by "the camera's own power or its
Pico". D-016 says the cameras are off while Qbot is asleep. Cheap USB
camera boards often have no LED, or one that software switches. If the
camera stayed powered while asleep and software simply didn't open it,
an LED on its power would stay lit and mean nothing.

## Decision
- The video LED is wired to the camera's 5V supply, so it's lit whenever
  the camera is powered, whatever the camera board does.
- Asleep (D-016) and "not using the camera" both mean **the camera's 5V is
  switched off**, not just that no software has it open.
- How it's switched: whichever is simpler once the parts are in hand. That's
  per-port power switching on the head hub (`uhubctl`) if the hub supports
  it, or else a Pico switching the camera's 5V through a MOSFET/load
  switch. Dan is happy for this to be a Pico if needed.

## Alternatives
- Software-only off (don't open the device): simplest, but then an LED on
  power can't show whether the camera is in use.
- The camera board's own LED: only if it's tied to the hardware, which
  isn't true of many cheap boards and is hard to check.

## Consequences
- R-213's hub choice should prefer per-port power switching.
- The LED can't lie: if it's off, the camera has no power.
- Camera start-up after power-on adds a delay (likely a second or two)
  whenever vision is needed. That's acceptable for now.
