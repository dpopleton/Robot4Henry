---
id: R-103
title: "Get key facts working"
phase: 1
status: planned
area: brain/memory
kind: code
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-10-08
---
## Goal
A structured store of hard facts (Henry's name, pets, favourite things) that reliably makes it into the prompt — complementing fuzzy long-term memory.

## Why
Dan liked the idea; it just never worked. Worth some time to get right.

## Tasks
- [ ] Rename `tests/brain/tests_key_facts.py` → `test_key_facts.py` — pytest only collects `test_*.py`, so these tests never run in the normal suite. (They pass when run directly — so the store itself works and the problem is in extraction or prompting.)
- [ ] Find out why it never worked (extraction? storage? prompting?) and write it up here
- [ ] Decide how facts get extracted (rest process? per turn?)
- [ ] Re-enable `key_facts.format_for_prompt()` in `robot_brain.py`
- [ ] Scenario test: a fact told in one session is used in the next

## Done when
A fact Henry states is stored, survives a restart, and shows up in a later conversation — covered by a scenario test.

## Open questions
- What exactly went wrong last time?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
