---
id: D-001
title: Eyes use a compact ASCII line protocol, not JSON or binary
status: accepted
date: 2026-10-07
area: organs/eyes
---
## Context
The eyes need two inputs — look direction and expression (+ intensity) —
sent independently or together, updating as fast as possible over USB
serial to a Pico running MicroPython. Direction will eventually stream
10–30 times a second from the crown's microphone array.

## Decision
One ASCII line per update with optional space-separated fields:
`D<dx>,<dy>` (integers −100..100), `E<name>[:<1-3>]`, `B` (blink). For
example `Ehappy:3 D-40,25`. Implemented once in
`organs/eyes/firmware/eye_protocol.py` and imported by both the Pico and
the host driver.

## Alternatives considered
- **JSON via `nervous_system/protocol.py`.** About 70 bytes per direction
  update vs at most 11 here, and more parsing work on the Pico.
- **Raw binary.** Smallest, but MicroPython treats a `0x03` byte on stdin
  as Ctrl-C and would kill `main.py` mid-stream. Also unreadable in a
  serial terminal.

## Consequences
- You can type commands by hand in a serial terminal to test.
- Malformed fields are skipped rather than crashing the eyes.
- The Pico drains every waiting line and merges them before drawing, so
  only the newest state is ever drawn (see D-002).
- Other organs don't have to use this format — each picks what suits it.
