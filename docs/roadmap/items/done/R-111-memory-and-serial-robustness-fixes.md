---
id: R-111
title: "Memory and serial robustness fixes"
phase: 1
status: done
area: brain
kind: code
depends_on: []
decisions: []
cost_gbp: 0
updated: 2026-11-03
---
## Goal
Small fixes that came out of several agent code reviews (Dan testing agents
as a work side project), checked and kept.

## Why
Each one fixed a real way a session or memory could be lost or a start-up could fail.

## Tasks
- [x] Rest: a reply that merely contains the word "none" no longer throws away the whole session's long-term memories (`tests/brain/test_rest_long_term.py`)
- [x] Medium-term: a failed or empty summary keeps the previous summary
- [x] Error path: the evicted turn still reaches medium-term memory when the LLM fails
- [x] `LongTermMemory.store()` no longer has a shared mutable default; `retrieve()` copes with an empty result
- [x] `DB_PATH` / `CHROMA_PATH` are absolute (work from any directory) and can be overridden with `QBOT_DB_PATH` / `QBOT_CHROMA_PATH`
- [x] A port setting that isn't `/dev/serial/by-id/...` warns and falls back to the fake port, instead of stopping start-up
- [x] `SerialTransport.receive()` returns `None` on a malformed line (noise at Pico start-up) instead of raising (`tests/nervous_system/test_protocol.py`)
- [x] Tests can't touch the real storage: `tests/conftest.py` points `QBOT_DB_PATH` / `QBOT_CHROMA_PATH` at a temp directory (`tests/test_storage_isolation.py`)
- [x] Removed unused code: `LLMClient.complete_json`, `wipe_memory.wipe_sqlite`

## Done when
The fast tests pass (215 on 2026-11-03).

## Log
- 2026-11-03: written up at the weekly review; the fixes were made in the week of 2026-10-26, uncommitted.
- 2026-11-03: Dan: isolate the tests (done), and deleted the stray test session from `storage/robot.db`. A bad port setting keeps its warning and falls back to the fake port.
