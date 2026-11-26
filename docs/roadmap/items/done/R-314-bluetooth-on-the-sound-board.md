---
id: R-314
title: "Bluetooth on the sound board"
phase: 3
status: done
area: head
kind: both
depends_on: [R-306]
decisions: [D-017, D-027]
cost_gbp: 0
updated: 2026-11-26
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
- [x] ~~Find out how the board pairs~~ not needed (D-027)
- [x] ~~Check whether Bluetooth can be turned off~~ not needed (D-027)
- [x] Decide: **off**, because the R30 board isn't used. The Waveshare has no Bluetooth (D-027)

## Done when
There's a decision on Bluetooth that suits unsupervised use.

## Log
- 2026-10-28: created when the soundbar board was adopted; Bluetooth accepted for now while use is supervised.
- 2026-11-26: settled by D-027: the Waveshare sound card replaces the R30 board, so there's no Bluetooth in the head. If the R30 board ever comes back as the fallback, reopen this.
