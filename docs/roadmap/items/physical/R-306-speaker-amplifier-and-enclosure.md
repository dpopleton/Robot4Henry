---
id: R-306
title: "Speakers, amplifier and enclosures"
phase: 3
status: planned
area: head
kind: both
depends_on: [R-212, R-213]
decisions: [D-013]
cost_gbp: 15
updated: 2026-10-22
---
## Goal
Two speakers in foam-packed compartments in the bottom corners of the front
plate, either side of the mouth screen, driven by a small stereo amp fed from
a USB sound card on the head's hub (D-013).

## Why
Qbot needs a voice. The sealed, foam-packed compartments stop sound carrying
into the head and the crown's mics.

## Tasks
- [ ] Pick two small speakers that fit the front plate's corner compartments
- [ ] Pick a USB sound card (on the head hub) and a stereo amp (PAM8403-type)
- [ ] Foam-pack the compartments; check the shell doesn't buzz
- [ ] Power the amp from the head's supply (R-213)
- [ ] Set the brain computer's default output to the USB sound card

## Done when
Qbot's audio plays clearly from both speakers without buzzing the shell.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-14: speaker moved from bottom centre to two compartments in the
  front plate's bottom corners, either side of the mouth. Audio path decided:
  a USB sound card in the head (D-013).
- 2026-10-22: parts to order in the next two weeks, after the crown parts (Henry chose crown first).
