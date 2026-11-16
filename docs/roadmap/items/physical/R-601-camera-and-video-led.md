---
id: R-601
title: "Camera and video LED"
phase: 4
status: idea
area: organs/vision
kind: both
depends_on: [R-213]
decisions: [D-007, D-016, D-012, D-025]
cost_gbp: null
updated: 2026-11-06
---
## Goal
A camera at the top of the front face, above the Q, with a video indicator LED driven by the camera hardware.

## Why
Vision is needed for faces and objects.

## Tasks
- [x] Space reserved in the front frame: a 2.5 × 10 cm hole above the Q for an insert panel (R-212)
- [ ] Pick the camera (when we get there) and design its insert for the 2.5 × 10 cm hole
- [ ] Video LED on the front face, opposite the recording LED, wired to the camera's own 5V (D-007, D-025)
- [ ] Switch the camera's 5V off when it isn't in use: hub per-port switching (`uhubctl`) or a Pico + MOSFET, whichever is simpler (D-025)
- [ ] Shield the lens from the Q and head glow (R-211)
- [ ] Plugs into the head's hub (R-213)
- [ ] Off (unpowered) while asleep (D-016, D-025)
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
The camera streams to the brain computer, and the video LED is lit exactly while it does.

## Open questions
- Which camera? Decided when we get there. A USB webcam board would plug into the head hub (R-213), and
  many have their own hardware LED, which would satisfy D-007.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: camera type still undecided.
- 2026-10-22: head electronics review: the camera is still planned for the head; video LED sits on the face opposite the recording LED.
- 2026-11-06: Phase 6 grill: moved to Phase 4 so the camera goes into the head before the skin (Dan is fine opening the head earlier). The insert hole is 2.5 × 10 cm above the Q. The LED is on the camera's 5V, and off = unpowered (D-025). Try it on the current laptop before any upgrade (R-902).
