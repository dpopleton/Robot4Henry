---
id: R-207
title: "Router process"
phase: 2
status: next
area: nervous_system
kind: code
depends_on: []
decisions: [D-003, D-008, D-009]
cost_gbp: null
updated: 2026-10-08
---
## Goal
One always-running process on the brain computer that routes inputs (crown) to outputs (eyes, mouth, lights) and turns the brain's mood into face commands.

## Why
Direction is a reflex and must never wait for the LLM (D-003). The brain should only know moods, not face parts (D-008).

## Tasks
- [ ] Process/thread structure separate from chat()
- [ ] Mood → eyes (+ later mouth, lights) mapping
- [ ] Direction handling: smoothing, hysteresis, hold then return to centre, confidence threshold, mute while Qbot speaks
- [ ] Map 360° bearing to the eyes' ±90° (voice behind → peg to that side)
- [ ] Keep the last voice bearing for the brain to ask about
- [ ] Re-send current state on connect/periodically (the Pico forgets on reboot)
- [ ] Survive an organ being unplugged
- [ ] Ports configured by /dev/serial/by-id

## Done when
A fake direction source moves the simulator eyes smoothly while the brain is mid-reply, and the mood follows the conversation.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
