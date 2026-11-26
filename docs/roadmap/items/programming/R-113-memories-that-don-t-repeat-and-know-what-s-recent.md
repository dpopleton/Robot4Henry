---
id: R-113
title: "Memories that don't repeat and know what's recent"
phase: 1
status: idea
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-11-23
---
## Goal
The 3 memories that go into each prompt are different from each other, and
favour what's recent and what Henry keeps coming back to.

## Why
Rest stores every memorable sentence from every session. A fact Henry
mentions in ten chats ("Henry has a cat") is stored ten times, and since
retrieval is by similarity alone, the 3 prompt slots can fill with copies of
it. Old and new memories also count the same.

## Tasks
- [ ] On store, look for a near-identical memory (embedding distance under a threshold, tuned on real examples); if found, update its `last_seen` and bump a `mentions` count instead of adding a copy
- [ ] Keep this working with `replace_session` (R-110): a re-rest mustn't double-count mentions
- [ ] Retrieve more candidates (e.g. 10) and rank by a mix of similarity, recency and mentions; take the top 3
- [ ] Drop near-duplicates from the final 3
- [ ] Tests with a fake embedding, as `tests/brain/test_long_term.py`

## Done when
After several sessions repeating the same fact, it's stored once, and the
prompt's 3 memories are three different things.

## Log
- 2026-11-23: created from a review of the memory design with Dan.
