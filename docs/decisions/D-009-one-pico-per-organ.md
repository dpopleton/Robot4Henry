---
id: D-009
title: One microcontroller per organ
status: accepted
date: 2026-10-08
area: organs
---
## Context
Dan prefers distributing tasks and having independent computing where
possible.

## Decision
By default each organ (eyes, crown, mouth, lights, and later neck and
motors) gets its own Pico on its own USB port. Combine only if USB ports
or space actually run out.

## Consequences
- Organs can be built, flashed and tested independently.
- Needs a powered USB hub. `/dev/ttyACM*` numbers move around, so
  configure ports by `/dev/serial/by-id/…`.
