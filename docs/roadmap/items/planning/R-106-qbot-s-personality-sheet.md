---
id: R-106
title: "Qbot's personality sheet"
phase: 1
status: planned
area: brain
kind: planning
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-10-22
---
## Goal
A written character for Qbot — likes, dislikes, catchphrases, backstory — created with Henry, which the personality prompt is built from.

## Why
Currently a few lines of prompt. A proper character makes Qbot feel like someone, and it's a great Henry job.

## Tasks
- [x] Session with Henry to brainstorm the character (answers in docs/henry/personality-questions.md)
- [ ] Write it up (agent drafts, Dan approves): draft in `brain/personality.md`, `henry_text_approved: false`
- [ ] Build `_personality()` from it
- [ ] Check the small model actually sticks to it (scenario test)

## Done when
The personality sheet exists in the repo and the prompt is built from it.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-15: question list ready: docs/henry/personality-questions.md (for 20 Oct).
- 2026-10-22: Henry answered every question. Draft sheet in brain/personality.md: Qbot is a boy, Henry's age, crash-landed from the sun; calls Henry "Popplas". "Never hurt people who are nice" written as "never hurts anyone" (Dan agreed).
