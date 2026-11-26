---
id: R-114
title: "Long-term memories in robot.db instead of ChromaDB"
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
All of Qbot's memory lives in one SQLite file, `storage/robot.db`.

## Why
Optional tidy-up, not a fix: ChromaDB works. But it's a second database
plus its own runtime for what will be a few thousand short sentences at
most, small enough to search directly. One file means:
- one thing to back up (R-906);
- storing a session's memories and marking it processed can be one
  transaction, so the R-110 duplicate problem can't happen at all;
- less RAM next to the LLM on an 8GB laptop.

## Tasks
- [ ] Decide: `sqlite-vec`, or a plain table with vectors searched in numpy
- [ ] Keep an embedding model (Chroma's MiniLM ONNX model can be used directly, or one via Ollama); check RAM and speed on the robot laptop
- [ ] Same `LongTermMemory` interface, so the brain and rest don't change
- [ ] One-off migration of existing ChromaDB memories
- [ ] Update `docs/disk-space.md` and the memory README

## Done when
Qbot runs without ChromaDB, existing memories are carried over, and the
tests pass.

## Log
- 2026-11-23: created from a review of the memory design with Dan.
- 2026-11-26: Phase 1 grill: Dan expects ChromaDB's RAM to be small enough; checked during the shoot-out (R-104) and only picked up if he's wrong.
