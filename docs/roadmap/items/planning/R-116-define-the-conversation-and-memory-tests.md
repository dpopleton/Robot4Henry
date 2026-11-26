---
id: R-116
title: "Define the conversation and memory tests"
phase: 1
status: planned
area: brain
kind: planning
depends_on: []
decisions: []
cost_gbp: null
updated: 2026-11-26
---
## Goal
Phase 1's "holds a good conversation" and "remembers key facts reliably"
become tests with a clear pass mark, run on the robot laptop.

## Why
Phase 1 grill (2026-11-26): both were too vague to tell when the phase is
done. The `-m llm` scenario tests exist but don't say what "good" or
"reliable" means, and the small models aren't deterministic, so a single
pass proves little.

## Tasks
- [ ] Write down what a good conversation means for Qbot: stays in character (R-106), answers what was asked, short replies a 7-year-old can follow, asks back, nothing unsafe
- [ ] Turn each point into checks in the scenario tests (string checks where possible, a judge model only if needed)
- [ ] Memory: a fixed set of facts told in one session and asked about in a later one, including corrections ("actually my favourite is…")
- [ ] Define "reliable": how many runs per scenario, and how many must pass (e.g. 9 out of 10)
- [ ] A runner that repeats each scenario and prints a pass rate, so the shoot-out (R-104) can use it

## Done when
The tests and their pass mark are written down here and in the scenario
tests, and the runner prints a pass rate on the dev machine.

## Log
- 2026-11-26: created in the Phase 1 grill.
