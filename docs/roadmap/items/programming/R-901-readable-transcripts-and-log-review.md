---
id: R-901
title: "Readable transcripts and log review"
phase: ongoing
status: planned
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-11-26
---
## Goal
Make the raw logs easy to read through, and review them regularly (part of the weekly review).

## Why
Safety policy: supervised use plus regular log review (see docs/roadmap/phases.md).

## Tasks
- [ ] Log everything needed to debug a session, not just the words: errors and tracebacks, mood changes, reply times, which model answered, and anything the safety checks caught
- [ ] A script that prints a session as a readable transcript, with those events in line
- [ ] Add a transcript skim to /weekly-review

## Done when
Reviewing a week's conversations takes a few minutes.

## When
Before Henry's first chat with the robot itself (a Phase 1 safety need,
phases.md). Henry doesn't type, so that's when voice arrives in Phase 3.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-11-20: Ongoing grill: the logs should hold everything needed to debug, not just the words. Whether this gates Henry's next chat is still open.
- 2026-11-26: Phase 1 grill: yes, it must be done before Henry's first chat with the robot, and it's part of Phase 1's safety needs.
