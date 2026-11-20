---
id: R-209
title: "Virtual robot (framework + eyes)"
phase: 2
status: in-progress
area: virtual_robot
kind: code
depends_on: []
decisions: [D-003, D-009, D-012, D-023]
cost_gbp: null
updated: 2026-11-20
---
## Goal
A virtual Qbot in a window on the dev machine. The brain and router run
exactly as they do on the robot; only the organ bytes go to the window
instead of a Pico. It starts with the eyes, and every later organ adds
itself (D-012).

## Why
The whole brain → router → organs chain can then be tested anywhere,
without the hardware being built, plugged in or even at hand. This will
come up again and again: R-207's demo, R-208's "mood follows the
conversation", and every organ after the eyes.

## Tasks
- [x] Per-organ virtual panels + controls, and the off/virtual/real/both switch per organ (D-023; first built with the mouth, R-210)
- [x] Move the eyes onto a panel; `simulate.py` becomes `--only eyes` bench mode, then goes
- [ ] Virtual robot window as its own process, hosting one panel per virtual organ
- [ ] `VirtualTransport` with the same `connect()`/`write()`/`close()` as `SerialTransport`, talking to the window over a local socket
- [ ] Each organ's port setting accepts `virtual` as well as `/dev/serial/by-id/...` (e.g. `QBOT_EYES_PORT=virtual`)
- [x] Virtual eyes: reuse the simulator's drawing (`organs/eyes/firmware/` code unchanged) and the real wire format
- [ ] Closing/reopening the window behaves like unplugging/replugging a Pico (the router keeps running and resends its state)
- [ ] First fake input, voice direction, needed for R-207's demo (other inputs are decided one by one, per organ)
- [ ] `python main.py` runs against the virtual robot
- [ ] README for the new code area; document how to run it (bench part done: `virtual_robot/README.md`; the process/socket part still to write)
- [ ] Check eyes and mouth on their real Picos at once (both benches on Real/Both)

## Done when
- A fake direction source moves the virtual eyes smoothly through the real
  router while the brain is mid-reply (finishes R-207).
- `python main.py` with `QBOT_EYES_PORT=virtual` shows the mood changing on screen.

## Open questions
- Socket message format: the real organ wire lines tagged with the organ name, or one socket per organ?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41)
  as "Simulator transport for testing without hardware".
- 2026-10-12: grown into the virtual robot framework after the R-207 review:
  separate window process over a socket; every organ ships a virtual
  version (D-012); which inputs get faked is decided organ by organ.
- 2026-11-05: panels + bench mode decided (D-023): one app, a switch per organ
  (off/virtual/real/both), `--only <organ>` replaces `simulate.py`. The panels come
  first with the mouth; the process/socket part still waits for R-207.
- 2026-11-05: the app lives in `virtual_robot/` at the top level (it isn't an organ).
- 2026-11-05: `virtual_robot/` started with the mouth bench: panels, controls, the switch and crash watch. Next: the eyes move over.
- 2026-11-18: the mouth (R-210) is done in the virtual robot and is the only organ in it so far; the eyes are next (task above).
- 2026-11-20: eyes moved in (`organs/eyes/virtual.py`), `simulate.py` removed. Panels now declare `SCREENS` (the eyes have two) and get a canvas driver per screen; `--only` takes several organs; benches won't share a Pico port and default to a free one. Eyes and mouth run side by side, each with its own switch. Adding a body part is now a `virtual.py` plus one `ORGANS` entry (checklist in `virtual_robot/README.md`).
- 2026-11-20: Ongoing grill: R-207's router demo waits for the `VirtualTransport` link here (no in-window shortcut), so that link is the next code step for the virtual robot.
