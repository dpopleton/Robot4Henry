---
id: D-023
title: One virtual robot app built from per-organ panels; a single-organ bench mode replaces the per-organ simulators
status: accepted
date: 2026-11-05
area: virtual_robot
---
## Context
D-012 settled that every organ gets a virtual version inside one virtual
robot (R-209), but left open whether `organs/eyes/simulate.py` stays as a
standalone preview. The mouth (R-210) is next and needs the same testing as
the eyes: drawing with the real firmware code, the real wire format,
side-by-side with the real Pico, and seeing the Pico's crashes (added to the
eyes simulator on 2026-11-05 after a silent `math.hypot` crash). Only the
buttons for poking one organ differ between organs.

## Decision
- **Each organ ships a virtual panel** (`organs/<organ>/virtual.py`): wire
  bytes in, the organ's firmware drawing code run unchanged, drawn on a
  canvas. Plus an optional **controls** widget with that organ's own buttons.
- **One app hosts the panels.** Each organ has one switch: **off**,
  **virtual**, **real** (a Pico port), or **both** (window and Pico together,
  for side-by-side checks). Port picking, sending to the real Pico and
  watching it for crashes are written once, in the app, for every organ.
- **Two ways to start it:**
  - **Bench** (`--only <organ>`): one organ with its controls and no brain.
    This replaces the per-organ simulators: `simulate.py` keeps working
    until the eyes have moved over, then goes.
  - **Whole robot** (no `--only`): every panel, driven by the router and
    brain as R-209 describes.
- **Build order:** the panels, controls and switch first (with the mouth),
  then move the eyes over. The process/socket/router part of R-209 waits
  for R-207, and slots in as a new source of bytes for the same panels.

## Alternatives considered
- **A separate in-depth simulator per organ, plus one combined app for
  testing them together.** Each simulator would copy the eyes' ~270 lines,
  including the hardware mirror and crash watch, so every fix would be made
  once per organ, and the combined app would be a second copy again.
- **Whole-robot app only.** Testing one expression would mean running the
  brain, or clicking through a crowded window. The bench mode costs almost
  nothing once the panels exist.

## Consequences
- Organ code splits into firmware (drawing + protocol, unchanged on the
  desktop), a virtual panel, and optional controls. Tests can drive a panel
  without opening a window.
- "Works in the virtual robot" on an organ item now means "has a panel, and
  its bench mode works with the real Pico ticked as well".
- R-209's open question about `simulate.py` is answered: it becomes the
  eyes' bench mode.
