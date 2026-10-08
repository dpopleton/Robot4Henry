---
id: D-006
title: Prototype direction-finding in Python on the brain computer first
status: accepted
date: 2026-10-08
area: crown
---
## Context
Direction-finding (GCC-PHAT across mic pairs) is the hardest code in the
hearing system. Debugging DSP code blind on a microcontroller is where
projects like this tend to stall.

## Decision
The crown streams all four raw channels (D-005), and the brain computer
works out direction in Python/numpy. Moving the maths onto the Pico in C is
an optional later step.

## Alternatives considered
- **Direction-finding on the Pico from the start.** Independent of the
  brain computer and slightly faster, but slow to iterate on and hard to
  see inside.

## Consequences
- You can plot the correlations and tweak in seconds.
- Crown firmware shrinks to "capture and stream".
- Direction depends on the brain computer being up, and adds ~10–30 ms of
  buffering — still fast enough for eyes.
- The crown's serial output can stay empty until a C port exists.
