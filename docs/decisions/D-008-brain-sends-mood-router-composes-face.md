---
id: D-008
title: The brain only sends a mood; the router decides what each face part shows
status: accepted
date: 2026-10-08
area: nervous_system
---
## Context
The face will have several parts showing emotion (eyes, mouth, Q colour)
and more may come.

## Decision
The brain emits only a mood (category + intensity) and activity
(listening/thinking/talking/asleep). The router turns it into eyes + mouth
+ lights commands.

## Consequences
- Adding or changing a face part never touches brain code.
- The mapping from mood to each part lives in one place, and can be tested
  with the simulator.
