---
id: R-314
title: "Bluetooth on the sound board"
phase: 3
status: idea
area: head
kind: both
depends_on: [R-306]
decisions: [D-017]
cost_gbp: 0
updated: 2026-10-28
---
## Goal
Decide what to do about the R30 PLUS board's Bluetooth: keep it open, put
it behind a pairing button, switch it off, or turn it into a feature.

## Why
The salvaged sound board (D-017) accepts Bluetooth audio, so anyone nearby
can pair a phone and play sound through Qbot's speakers. That's fine while
use is supervised, but it matters before the kids use Qbot on their own.
It could also be a feature later (playing music through Qbot), probably not
through the main speaker path.

## Tasks
- [ ] Find out how the board pairs (always discoverable? a pairing pin or button?)
- [ ] Check whether Bluetooth can be turned off (pin, antenna, mode button) without losing USB audio
- [ ] Decide: open / pairing button / off / feature

## Done when
There's a decision on Bluetooth that suits unsupervised use.

## Log
- 2026-10-28: created when the soundbar board was adopted; Bluetooth accepted for now while use is supervised.
