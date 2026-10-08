---
id: R-208
title: "Brain sends its mood to the router"
phase: 2
status: planned
area: brain
kind: code
depends_on: [R-207]
decisions: [D-008]
cost_gbp: null
updated: 2026-10-08
---
## Goal
RobotBrain gets a nervous system injected and reports mood at wake, after each turn, and at session end — plus activity (thinking/talking/asleep).

## Why
The final link between the brain and the face.

## Tasks
- [ ] EYES_PORT etc. in config/settings.py (None = mock)
- [ ] Build the nervous system in main.py, pass it into RobotBrain
- [ ] Hooks: limbic.wake(), after limbic.react(), _handle_session_end()
- [ ] Organ errors are logged, never crash the conversation
- [ ] Close ports in shutdown()

## Done when
Chatting in the terminal changes the eyes' expression; unplugging the Pico mid-chat doesn't break the conversation.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
