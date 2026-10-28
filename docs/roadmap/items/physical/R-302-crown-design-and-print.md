---
id: R-302
title: "Crown design and print"
phase: 3
status: planned
area: crown
kind: physical
depends_on: [R-301, R-212]
decisions: [D-007, D-015]
cost_gbp: 3
updated: 2026-10-22
---
## Goal
Design the crown around the real mic boards: the full 25 cm width of the head and about 10 cm tall (Henry likes the crown).

## Why
The mics need open sound holes and spacing that makes direction-finding work.

## Tasks
- [ ] Left/right mics at the crown's ends, about 25 cm apart
- [ ] Front pair stacked as far apart vertically as the ~10 cm crown allows (no brow mic needed on the front plate)
- [ ] Crown Pico inside; the recording LED it drives sits on the front face, wired down from the crown (D-007)
- [ ] Henry's shape (he's decided it) — sketch or photo into anatomy/crown/images/
- [ ] "Gems": cheap plastic gems glued into sockets; keep glue and gems clear of the mic holes
- [ ] Holes a few mm wide, mic board pressed against them from inside
- [ ] Isolate from the head: mount the crown on rubber grommets or washers so the bolts don't make a hard path from the head to the crown; don't overtighten
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
