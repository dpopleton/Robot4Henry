---
id: R-906
title: "Back up Qbot's memories"
phase: ongoing
status: idea
area: storage
kind: code
depends_on: []
decisions: []
cost_gbp: 0
updated: 2026-11-20
---
## Goal
A copy of Qbot's memories kept somewhere other than the robot laptop, so
losing its disk doesn't mean Qbot forgets Henry.

## Why
`storage/robot.db` (conversations, key facts, summaries) and
`storage/chroma_db/` (long-term memory) are gitignored, so they live only
on the robot laptop, whose disk is about 8 years old. Fine for now, while
there's little in them; it matters more once Henry talks to Qbot often.

## Tasks
- [ ] Decide where the copy goes (the dev machine, a USB stick, …) and how often (e.g. as part of the weekly review)
- [ ] A script that copies the database safely while nothing is writing to it
- [ ] Check a restore works

## Done when
A recent copy exists off the robot laptop and has been restored once to prove it works.

## Log
- 2026-11-20: created in the Ongoing grill. Dan: fine for now, a late task.
