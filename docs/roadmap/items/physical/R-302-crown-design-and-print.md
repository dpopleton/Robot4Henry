---
id: R-302
title: "Crown design and print"
phase: 3
status: planned
area: crown
kind: physical
depends_on: [R-301, R-212]
decisions: [D-007, D-015]
cost_gbp: 0
updated: 2026-11-26
---
## Goal
Design the crown around the real mic boards: the full 25 cm width of the head and about 10 cm tall (Henry likes the crown).

## Why
The mics need open sound holes and spacing that makes direction-finding work.

## Tasks
- [ ] Left/right mics at the crown's ends, about 25 cm apart
- [ ] Front pair stacked as far apart vertically as the ~10 cm crown allows (no brow mic needed on the front plate)
- [ ] Crown Pico inside; the recording LED it drives sits on the front face, wired down from the crown (D-007)
- [ ] Henry's shape: sketched 2026-11-26 (a square wave, a gem under each tab; the front tab taller for the front mics, Dan's idea, Henry agreed). Photo of the sketch into anatomy/crown/images/
- [ ] "Gems" (bought, £5): glued into sockets under each tab; keep glue and gems clear of the mic holes
- [ ] Holes a few mm wide, mic board pressed against them from inside, each mic sealed to its hole with a ring of foam so it hears the outside air, not the inside of the head
- [ ] Mic boards sit on a bit of foam rather than bolted hard to the crown
- [ ] Isolate from the head: mount the crown on rubber grommets or washers so the bolts don't make a hard path from the head to the crown: rubber on both sides of each mounting tab (under the bolt head and against the heat insert), bolt not touching the tab's hole (oversized hole or sleeved grommet); snug, with the rubber only slightly squashed
- [ ] Seal or stuff any gaps between the inside of the head and the crown, so sound inside the head can't leak straight up to the mics
- [ ] Room for the recording LED (D-007)
- [ ] Sits on the aluminium skin over the top panel (R-212, R-402); leave room for the big wake button on top of the head (R-308)

## Done when
The crown is printed, holds the mics, and direction-finding works through it.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: the crown sits on the top panel and hides the wake button.
- 2026-10-14: Phase 3 grill: crown is 25 cm wide and ~10 cm tall; both front mics fit in it; one Pico for everything on the crown (D-014).
- 2026-10-22: Henry chose crown first (before speakers), decided its shape, and wants gems in it.
- 2026-10-22: head electronics review: the recording LED moved to the front face (opposite the video LED); the antenna light is on the lights Pico, not the crown.
- 2026-10-22: no wake button in the crown any more: it's the big button on top, read by the lights Pico (D-015).
- 2026-10-22: rubber isolation between the crown and the head (and between the speaker boxes and the head, R-306).
- 2026-11-26: sound from the speakers to the mics: air is the main path (handled in software, R-309), the bolts a smaller one. Added rubber on both sides of each mount, sealing each mic to its hole, foam under the mic boards, and sealing the head-to-crown gaps.
- 2026-11-26: weekly review: Henry sketched the crown: a square wave (tabs up and down along the 25 cm), with a gem under each tab. Dan suggested the front tab goes higher so the two front mics can be stacked further apart, and Henry happily agreed. Gems (£5) and M3 rubber washers (£5) bought.
