---
id: D-003
title: The brain computer is the hub, with the router as its own process
status: accepted
date: 2026-10-08
area: nervous_system
---
## Context
Direction (from the crown's mics) is a fast reflex — tens of
milliseconds. Mood comes from the LLM — seconds, once per turn. Signals
have to flow between several Picos and the brain. We considered a
dedicated small Pi as a router, and wiring Picos directly to each other.

## Decision
Every Pico plugs into the brain computer by USB (through a hub). A
**router** process runs on the brain computer, separate from
`RobotBrain.chat()`. It reads inputs (crown), drives outputs (eyes, mouth,
lights), and passes the brain's mood through.

## Alternatives considered
- **A separate router Pi.** Worth it if the brain computer came and went,
  but it will always live inside the robot. It adds an OS, power and
  another hop to debug.
- **Crown Pico wired straight to the eyes Pico (UART).** Fastest, and
  works even if the brain crashes, but the "how to look" logic gets stuck
  in firmware and the brain never learns where a voice came from.

## Consequences
- The router must never wait on the LLM — it's a separate process or
  thread.
- Smoothing, hold/return-to-centre, confidence thresholds and muting
  Qbot's own voice all live in the router.
- If a router Pi is ever needed, the same process moves onto it.
