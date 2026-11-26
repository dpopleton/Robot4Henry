---
id: R-311
title: "Know who it's talking to"
phase: 3
status: idea
area: brain
kind: code
depends_on: [R-304]
decisions: []
cost_gbp: null
updated: 2026-11-26
---
## Goal
Qbot recognises Henry vs his sister (and grown-ups), with separate memories.

## Why
Dan: it should know who it's talking to.

## Tasks
- [ ] Voice-based (speaker recognition) or face-based (R-602)?
- [ ] Per-person memory: raw logs, key facts and long-term memories all scoped to a person
- [ ] Key facts are one global table keyed by the model's own wording, so
      "favourite animal" and "favorite animal" are separate facts, and the
      sister saying her name would overwrite "name: Henry". Normalise keys
      and record which session each fact came from
- [ ] The storage side can come first, before recognition: a `person` on facts and memories, set by hand or a setting for now, so the sister's first chats don't overwrite Henry's facts

## Done when
Qbot greets each child by name and remembers their own things.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-13: added key-fact notes from an outside code review.
- 2026-10-14: Phase 3 grill: it must handle several speakers at some point (Henry, his sister, grown-ups); when is open.
- 2026-11-23: memory design review: do the per-person storage before Henry's sister starts using Qbot, even if recognition comes later.
- 2026-11-26: Phase 1 grill: Henry's sister can't type, so she starts with voice: the per-person storage is needed before her first spoken chat, which keeps it in Phase 3.
