---
id: R-601
title: "Camera and video LED"
phase: 6
status: idea
area: organs/vision
kind: both
depends_on: []
decisions: [D-007, D-010, D-012]
cost_gbp: null
updated: 2026-10-14
---
## Goal
A camera at the top of the front face, above the Q, with a video indicator LED driven by the camera hardware.

## Why
Vision is needed for faces and objects.

## Tasks
- [ ] Space reserved in the front frame now (R-212)
- [ ] Video LED wired per D-007
- [ ] Off while asleep (D-010)
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
The camera streams to the brain computer, and the video LED is lit exactly while it does.

## Open questions
- Which camera? A USB webcam board would plug into the head hub (R-213), and
  many have their own hardware LED, which would satisfy D-007.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: camera type still undecided.
