---
id: R-103
title: "Get key facts working"
phase: 1
status: done
area: brain/memory
kind: code
depends_on: []
decisions: [D-011]
cost_gbp: null
updated: 2026-10-12
---
## Goal
A structured store of hard facts (Henry's name, pets, favourite things) that reliably makes it into the prompt — complementing fuzzy long-term memory.

## Why
Dan liked the idea; it just never worked. Worth some time to get right.

## Tasks
- [x] Rename `tests/brain/tests_key_facts.py` → `test_key_facts.py` — pytest only collects `test_*.py`, so these tests never run in the normal suite. (They pass when run directly — so the store itself works and the problem is in extraction or prompting.)
- [x] Find out why it never worked (extraction? storage? prompting?) and write it up here
- [x] Decide how facts get extracted (rest process? per turn?)
- [x] Re-enable `key_facts.format_for_prompt()` in `robot_brain.py`
- [x] Scenario test: a fact told in one session is used in the next
- [x] Make the scenario pass against the real model — extraction currently returns `None`
- [x] Don't throw away the whole extraction when one line contains "none" (e.g. `pets: none`)

## Done when
A fact Henry states is stored, survives a restart, and shows up in a later conversation — covered by a scenario test.

## Open questions
- What exactly went wrong last time? Resolved: the SQLite store was sound, but
  its tests were named `tests_key_facts.py` and were skipped by normal pytest
  discovery. More importantly, both the call to `_extract_key_facts()` in the
  rest process and `format_for_prompt()` in `RobotBrain` had been commented
  out, so no fact could be written or supplied to the model.

## Decision

Facts are extracted during the rest process, not per turn. This keeps the
conversation path fast, lets extraction work from a completed durable
transcript, and naturally persists facts for the next process/session. The
extractor reads user lines only, runs at temperature 0, and a fact is kept
only if every word of its value appears in what the user said — a plain code
check that replaced asking the model "is this true?" (D-011).

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: re-enabled rest extraction and prompt injection; added durable
  restart coverage.
- 2026-10-12: verification — fast suite passes, but `pytest -m llm` fails
  `remembers_name_across_sessions` (3/3 runs): given "My name is Henry", the
  extraction prompt returns `None`, so no fact is stored. Back to in-progress.
- 2026-10-12: fixed. Probing llama3.2:1b showed 8/12 replies padded with
  `pets: NONE` lines (which discarded the whole reply), 2/12 a bare NONE, and
  frequent invented favourites; the YES/NO verify pass rejected the true
  "dinosaur" fact 5/6 times. Now: temperature 0, per-line parsing, and a word
  grounding check instead of the LLM verify (D-011). `pytest -m llm` passes
  4/4 runs; unit tests in `tests/brain/test_rest_key_facts.py`.
