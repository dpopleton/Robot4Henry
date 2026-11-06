---
id: D-020
title: Qbot drives itself (voice commands or wandering); a gamepad is only for testing
status: accepted
date: 2026-11-03
area: body
---
## Context
Phase 5 said the body "drives safely indoors" without saying who does the
driving, and what "safe" means depends on it.

## Decision
Movement is decided inside Qbot: either on voice commands ("come here") or
by wandering on its own. Which comes first is decided nearer the time. A
gamepad may be used for testing, but it isn't how Qbot is meant to move.
The speed is walking pace or slower.

## Alternatives considered
- **Remote control as the main way to drive.** Simpler and easier to make
  safe, but Qbot is a companion, not an RC car.
- **Gamepad only, autonomy later.** Still possible for testing, but it isn't
  the goal.

## Consequences
- Motion safety (R-503) can't rely on a person holding a controller: the
  speed limit, bump and drop sensors and the stop button have to work
  without one.
- The brain (or router) needs a way to ask the motor Pico to move, which
  joins the nervous system like the other organs.
