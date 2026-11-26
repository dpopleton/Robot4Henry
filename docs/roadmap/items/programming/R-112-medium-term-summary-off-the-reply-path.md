---
id: R-112
title: "Medium-term summary off the reply path"
phase: 1
status: idea
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-11-26
---
## Goal
Long conversations don't get slower: folding old exchanges into the
medium-term summary never delays a reply.

## Why
Once short-term holds 10 exchanges, every new one pushes the oldest out,
and `medium_term.update()` makes an LLM call inside the turn, before the
reply is returned (`brain/cognition/robot_brain.py`, `_turn`). So every turn
after the 10th costs two model calls. On the robot laptop that's likely
seconds per turn.

## Tasks
- [ ] Evict in batches (e.g. the oldest 4 exchanges at once), so the summary is updated every few turns, not every turn
- [ ] Run the update in the background after the reply, with a lock so two updates never overlap and the prompt reads a consistent summary (one turn behind is fine)
- [ ] Session end waits for (or discards) a running update before medium-term is wiped
- [ ] Measure turn times on the robot laptop before and after, in a 20-turn chat

## Done when
Turn time in a 20-turn conversation on the robot laptop stays flat after the
10th turn.

## Log
- 2026-11-23: created from a review of the memory design with Dan.
- 2026-11-26: Phase 1 grill: stays an idea unless the 20-turn timing in the shoot-out (R-104) shows turn times climbing.
