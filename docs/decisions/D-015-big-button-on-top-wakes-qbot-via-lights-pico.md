---
id: D-015
title: The big button on top of the head is the wake button, read by the lights Pico
status: accepted
date: 2026-10-22
area: head
supersedes: D-014
---
## Context
D-014 put a hidden wake button in the crown, read by the crown Pico. Since
then the head plan has a large 3D-printed mechanical button on top of the
head (R-313), the antenna light is wired down to the lights Pico, and the
crown's C firmware is the slowest part of the project to arrive.

## Decision
The **large button on top of the head is the wake button**; there's no
hidden button in the crown. The **lights Pico** reads it and reports presses
over serial, asleep or awake. The crown Pico keeps the mics and the recording
LED (D-007), and starts or stops streaming when the router tells it to.

## Alternatives considered
- **The crown Pico (D-014).** It's right on top, but the button would wait for
  the C firmware, and the crown would hold two buttons' worth of wiring.
- **Keep two buttons:** a hidden wake button plus a pat button. One button is
  simpler for a 3-year-old and for the design.

## Consequences
- Waking works as soon as the lights Pico (MicroPython) does, long before the crown firmware.
- The lights Pico must stay running while Qbot is asleep.
- Wake goes button → lights Pico → router → crown starts streaming.
- The crown firmware no longer handles a button; its layout is just mics,
  Pico and the wire down to the recording LED.
- The same button also puts Qbot to sleep (D-010), so what a press means
  while awake has to be decided (R-308).
