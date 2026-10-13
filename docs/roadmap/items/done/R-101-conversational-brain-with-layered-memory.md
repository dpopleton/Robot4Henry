---
id: R-101
title: "Conversational brain with layered memory"
phase: 1
status: done
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-10-13
---
## Goal
Qbot holds a friendly conversation and remembers across sessions: short-term (verbatim), medium-term (rolling summary), long-term (ChromaDB, built during rest).

## Why
The core of Qbot — everything else hangs off it.

## Tasks
- [x] Short, medium and long-term memory
- [x] Session timeout + rest process
- [x] Raw logging to SQLite
- [x] Scenario tests against the real model

## Done when
Done — see docs/architecture.md for how it works.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: made rest processing single-claim, retained raw logs for weekly review,
  and made session shutdown/recovery idempotent.
- 2026-10-13: quitting and slow-reply session bugs fixed in R-108.
