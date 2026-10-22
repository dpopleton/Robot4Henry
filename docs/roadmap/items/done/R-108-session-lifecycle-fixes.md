---
id: R-108
title: "Session lifecycle fixes: quitting and slow replies"
phase: 1
status: done
area: brain
kind: code
depends_on: [R-101]
decisions: []
cost_gbp: null
updated: 2026-10-13
---
## Goal
No conversation is lost or cut in two by quitting, a crash, or a slow reply.

## Why
An outside code review found two real bugs:
- Quitting started rest on a background (daemon) thread and then exited,
  killing it part-way. A session killed after being claimed for rest was
  stuck as "processing" and never became memories.
- The inactivity timer kept running during a turn. A message sent just
  before the 5-minute timeout could be rested without its reply, and the
  reply then started a stray new session. On the robot laptop a reply takes
  seconds, so this was likely.

## Tasks
- [x] `SessionManager.begin_turn()`/`end_turn()`: no timeout while a turn is in progress
- [x] One lock shared by turns and session endings in `RobotBrain`
- [x] `shutdown()` rests the last session inline and waits for any background rest
- [x] On startup, recover sessions left unended or stuck mid-rest (`RawLogger.recover_interrupted_sessions`)
- [x] Tests for each case (they all fail on the old code)

## Done when
Done.

## Log
- 2026-10-13: fixed after an outside review; known gap: a rest killed part-way and
  re-run can store some long-term memories twice (see R-110).
