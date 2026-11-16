---
id: R-701
title: "Arms with C-shaped grabbers"
phase: 7
status: idea
area: body
kind: both
depends_on: [R-501, R-602]
decisions: [D-012]
cost_gbp: null
updated: 2026-11-16
---
## Goal
Arms with C-shaped grabbers, so Qbot can pick things up for himself:
toys, Lego, a cup, a ball, from the floor or a table. Henry designs the
arms, and we work from his design.

## Why
Long-term goal: picking things up.

## Tasks
- [ ] Henry designs the arms (drawings first; record them in the journal)
- [ ] Work out the heaviest thing to lift from Henry's design, then size the motors and power to match
- [ ] Two arms (one can come first while building)
- [ ] Grip limit: weak motor, current/stall limit in firmware, or slip clutch (decided at the time)
- [ ] The body's stop button stops the arms too (R-503)
- [ ] Qbot finds the object himself, using vision (Phase 6, maybe the low body camera R-603)
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Qbot picks up a named toy from the floor in front of him on a voice command,
by himself, with his two arms, and holds it up. The stop button freezes both arms.

## Open questions
- Heaviest object, and so the motor size: depends on Henry's design and
  the power budget. Probably sturdier than hobby servos; chosen at the time.
- How grip force is limited: decided at the time.
- Cost: unknown until the motors are chosen.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-11-16: Phase 7 grill. Qbot picks things up for himself (so it needs vision, R-602). The body gets a general plan for arms (R-501), but they're added later. The stop
  button covers the arms. Motors are probably heavier than hobby servos. Henry designs the arms.
  A low body camera, for driving and stereo, is an idea for later (R-603). Done-when drafted.
- 2026-11-16: two arms are needed, not one (Dan, after the review).
