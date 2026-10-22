---
id: R-110
title: "Tidy up storage threading"
phase: 1
status: idea
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-10-13
---
## Goal
SQLite and ChromaDB use stays safe when rest runs alongside a conversation,
and a rest re-run doesn't duplicate memories.

## Why
`RawLogger` and `KeyFactsStore` each share one SQLite connection between the
chat thread and rest threads. Each write commits straight away and SQLite
waits up to 5s for a lock, so failures are unlikely but possible. And a rest
killed part-way and re-run after recovery (R-108) can store some long-term
memories twice.

## Tasks
- [ ] WAL mode and/or a lock around writes (or a connection per thread)
- [ ] Give long-term memories stable ids per session so a re-run replaces rather than duplicates

## Done when
A concurrency test (rest during a conversation) passes reliably, and
re-resting a session leaves the same memories.

## Log
- 2026-10-13: created from an outside code review (rated lower than the review did).
