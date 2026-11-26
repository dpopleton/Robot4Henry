---
id: R-110
title: "Tidy up storage threading"
phase: 1
status: done
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-11-23
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
- [x] WAL mode and/or a lock around writes (or a connection per thread): an `RLock` around every connection use
- [x] Concurrency test: rest running during a conversation (`tests/brain/test_rest_concurrency.py`)
- [x] Give long-term memories stable ids per session so a re-run replaces rather than duplicates (`LongTermMemory.replace_session`)

## Done when
A concurrency test (rest during a conversation) passes reliably, and
re-resting a session leaves the same memories.

## Log
- 2026-10-13: created from an outside code review (rated lower than the review did).
- 2026-11-03: weekly review: half done, uncommitted. An agent code review (Dan testing agents) added an `RLock` around every use of the shared SQLite connection in `RawLogger` and `KeyFactsStore`, plus `close()` and context managers. Stable long-term memory ids and the concurrency test are still to do.
- 2026-11-20: weekly review: still wanted; no time this week.
- 2026-11-23: done. Rest now replaces a session's long-term memories (deletes that session's set, then adds with ids `<session_id>-<n>`), since a re-run can word them differently or list fewer. New tests against real SQLite and ChromaDB with a fake embedding: rest during a conversation, two rests at once, and a re-rest after a crash leaving the same memories. 313 tests pass.
