---
id: R-207
title: "Router process"
phase: 2
status: blocked
area: nervous_system
kind: code
depends_on: [R-209]
decisions: [D-003, D-008, D-009, D-012]
cost_gbp: null
updated: 2026-10-12
---
## Goal
One always-running process on the brain computer that routes inputs (crown) to outputs (eyes, mouth, lights) and turns the brain's mood into face commands.

## Why
Direction is a reflex and must never wait for the LLM (D-003). The brain should only know moods, not face parts (D-008).

## Tasks
- [x] Process/thread structure separate from chat()
- [x] Mood → eyes (+ later mouth, lights) mapping
- [x] Direction handling: smoothing, hysteresis, hold then return to centre, confidence threshold, mute while Qbot speaks
- [x] Map 360° bearing to the eyes' ±90° (voice behind → peg to that side)
- [x] Keep the last voice bearing for the brain to ask about
- [x] Re-send current state on connect/periodically (the Pico forgets on reboot)
- [x] Survive an organ being unplugged
- [x] Ports configured by /dev/serial/by-id
- [ ] Demo: a fake direction source drives the virtual robot's eyes through the router (needs R-209)

## Done when
A fake direction source moves the virtual robot's eyes (R-209) smoothly while the brain is mid-reply. (The mood following the conversation needs the brain wired in, so it moved to R-208.)

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: implemented the standalone router loop and deterministic
  direction-reflex tests.  Serial ports remain supplied by the application
  (R-208), using stable `/dev/serial/by-id/...` paths.
- 2026-10-12: verified.  Fixed Qbot's own voice (heard while speaking)
  overwriting `last_voice_bearing`, with a test.  Back to in-progress: the
  router isn't started anywhere yet, so the simulator demo is still to do;
  "mood follows the conversation" moved to R-208's Done when.
- 2026-10-12: blocked on R-209: the demo runs in the virtual robot rather than
  a one-off script.
