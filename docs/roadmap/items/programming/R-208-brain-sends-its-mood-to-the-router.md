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
updated: 2026-10-12
---
## Goal
RobotBrain gets a nervous system injected and reports mood at wake, after each turn, and at session end — plus activity (thinking/talking/asleep).

## Why
The final link between the brain and the face.

## Tasks
- [x] EYES_PORT etc. in config/settings.py (None = mock)
- [ ] A bad QBOT_*_PORT value warns and falls back to mock instead of stopping the chat starting
- [ ] Build `RobotRouter` + `RouterProcess` in main.py; the brain calls `router.set_mood()`, never organs directly
- [ ] Build the nervous system in main.py, pass it into RobotBrain
- [ ] Hooks: limbic.wake(), after limbic.react(), _handle_session_end()
- [ ] Organ errors are logged, never crash the conversation
- [ ] Close ports in shutdown()

## Done when
Chatting in the terminal changes the eyes' expression, so the mood follows the conversation; unplugging the Pico mid-chat doesn't break the conversation.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: R-207 added `EYES_PORT`/`CROWN_PORT`/`MOUTH_PORT`/`LIGHTS_PORT`
  (read from `QBOT_*_PORT`, must be `/dev/serial/by-id/...`).  Right now a bad
  value raises an error when `config.settings` is imported, so it needs softening.
  Took over "mood follows the conversation" from R-207's Done when.
