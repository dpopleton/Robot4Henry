---
id: R-401
title: "Neck: looking around"
phase: 5
status: idea
area: organs/neck
kind: both
depends_on: [R-501, R-305]
decisions: [D-012]
cost_gbp: 25
updated: 2026-10-22
---
## Goal
The head (~2–2.5 kg) turns left/right and tilts up/down, about like a person's (roughly 90° each way, tilt about 30° up and down; not fixed), turning towards voices beyond the eyes' range. Built with the body's frame and sitting directly on it.

## Why
Dan: the head will eventually be able to look around.

## Tasks
- [ ] Weigh the finished head → bearing and motor choice (the motor shouldn't carry the weight on its own shaft)
- [ ] Design the head's bottom panel with the neck: the mount plus the cable exit for the USB and power leads (D-013)
- [ ] Cables through the neck within the turning range (no slip ring needed at ±90°)
- [ ] Firm mechanical stops plus software limits on angle and speed
- [ ] Router: turn the head when the voice is past the eyes' range
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
Qbot turns its head towards someone behind it.

## Open questions
- Exact ranges and how tilt is built: engineered when we get there.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: the neck mount is designed here; the bottom panel only leaves room for it.
- 2026-10-22: Phase 4 grill: the neck is part of the body (its second step), built with its frame and sitting directly on it, so it moves to Phase 5. Pan and tilt; firm stops and motion limits; the head's bottom panel is designed here.
