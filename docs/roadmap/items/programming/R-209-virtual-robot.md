---
id: R-209
title: "Virtual robot (framework + eyes)"
phase: 2
status: planned
area: virtual_robot
kind: code
depends_on: []
decisions: [D-003, D-009, D-012]
cost_gbp: null
updated: 2026-10-12
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
- [ ] Virtual robot window as its own process, hosting one panel per virtual organ
- [ ] `VirtualTransport` with the same `connect()`/`write()`/`close()` as `SerialTransport`, talking to the window over a local socket
- [ ] Each organ's port setting accepts `virtual` as well as `/dev/serial/by-id/...` (e.g. `QBOT_EYES_PORT=virtual`)
- [ ] Virtual eyes: reuse the simulator's drawing (`organs/eyes/firmware/` code unchanged) and the real wire format
- [ ] Closing/reopening the window behaves like unplugging/replugging a Pico (the router keeps running and resends its state)
- [ ] First fake input, voice direction, needed for R-207's demo (other inputs are decided one by one, per organ)
- [ ] `python main.py` runs against the virtual robot
- [ ] README for the new code area; document how to run it

## Done when
- A fake direction source moves the virtual eyes smoothly through the real
  router while the brain is mid-reply (finishes R-207).
- `python main.py` with `QBOT_EYES_PORT=virtual` shows the mood changing on screen.

## Open questions
- Where does the code live: `virtual_robot/` at the top level, or `organs/virtual/`?
- Socket message format: the real organ wire lines tagged with the organ name, or one socket per organ?
- Does `organs/eyes/simulate.py` stay as a standalone eyes preview, or become the virtual eyes panel?

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41)
  as "Simulator transport for testing without hardware".
- 2026-10-12: grown into the virtual robot framework after the R-207 review:
  separate window process over a socket; every organ ships a virtual
  version (D-012); which inputs get faked is decided organ by organ.
