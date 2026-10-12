---
id: D-012
title: Every organ ships a virtual version that runs in the virtual robot
status: accepted
date: 2026-10-12
area: virtual_robot
---
## Context
Verifying R-207 (the router) needed the eyes driven from a fake voice
direction while the brain was mid-reply. Nothing could do that without
hardware: the eyes simulator only takes clicks and typed commands. This
will happen for every organ (mouth, lights, crown, speaker, neck, tracks,
arms), and much of the hardware won't exist yet when its code is written.

## Decision
A virtual robot (R-209) runs as its own window process. The software
reaches it through a `VirtualTransport` over a local socket, chosen per
organ in the port setting (`virtual` instead of a `/dev/serial/by-id/...`
path), so brain, router and drivers run unchanged. Every organ item has a
"works in the virtual robot" task. What each virtual organ fakes as an
input, rather than only displaying, is decided organ by organ on its item.

## Alternatives considered
- **Tk inside `main.py`.** Simpler, but Tk wants the main thread, which
  fights the terminal chat loop. It also isn't like real hardware: you
  can't unplug it.
- **A separate simulator per organ.** It never shows the whole robot
  reacting at once, and each one gets wired up differently.
- **Building virtual organs only when needed.** It gets skipped, and then
  testing needs hardware again.

## Consequences
- Every organ item has one more task, and the virtual robot grows with the real one.
- Drawing and protocol code must keep running unchanged on the desktop
  (already the firmware rule in CLAUDE.md).
- The transport boundary has to stay bytes-in, bytes-out, so real and
  virtual organs can't drift apart.
