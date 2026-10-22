---
id: R-109
title: "Check what goes back into memory"
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
Long-term memories and key facts are checked before they are stored, so one
unsuitable reply can't keep coming back in later prompts.

## Why
Rest builds long-term memories from both sides of the conversation,
including what Qbot said, and they go back into the system prompt unfiltered.
Safety today is the prompt plus supervised use and weekly log review
(phases.md); this is the place where one slip could keep coming back.

## Tasks
- [ ] Decide on the check: a word list, a second model pass, or both (on the robot laptop's budget)
- [ ] Apply it to memories and key facts before storing
- [ ] Show rejected memories in the weekly log review (R-901)

## Done when
An unsuitable line in a conversation never comes back as a stored memory.

## Log
- 2026-10-13: created from an outside code review.
