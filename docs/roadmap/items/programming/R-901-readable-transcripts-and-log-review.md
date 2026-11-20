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
updated: 2026-11-20
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

## Open questions
- Must this be done before Henry's next chat session (so the weekly log review is real), or can that wait? Dan isn't sure yet (2026-11-20). No sessions have been logged since 3 Nov.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-11-20: Ongoing grill: the logs should hold everything needed to debug, not just the words. Whether this gates Henry's next chat is still open.
