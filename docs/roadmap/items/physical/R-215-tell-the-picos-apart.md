---
id: R-215
title: "Tell the Picos apart"
phase: 2
status: planned
area: nervous_system
kind: both
depends_on: [R-213]
decisions: [D-009]
cost_gbp: 0
updated: 2026-11-20
---
## Goal
The laptop always knows which Pico is the eyes, which is the mouth (and
later the lights and the crown), whatever order they're plugged in and
whichever hub socket they're in. On the robot, the config names them as
`/dev/qbot-eyes`, `/dev/qbot-mouth`, …; on the bench, the port picker
shows which Pico each port is.

## Why
Each Pico has its own USB channel, so commands never go to the wrong one
once the port is right. But Linux numbers the ports `ttyACM0`, `ttyACM1`, …
in the order it finds them, so the numbers change with plug order, resets
and replugs. With one Pico per organ (D-009) on one hub (R-213), guessing
isn't good enough. Every Pico has a unique serial number in its flash
chip, which Linux shows as a stable name under `/dev/serial/by-id/`.

## Tasks
- [ ] With the hub in and every Pico plugged in, run `ls -l /dev/serial/by-id/` and note which serial number is which organ (in each `anatomy/<part>/build.md`)
- [ ] udev rule on the robot laptop (`/etc/udev/rules.d/99-qbot.rules`, a copy kept in the repo): match each Pico's serial number and add a `SYMLINK+="qbot-<organ>"`, so the config reads `/dev/qbot-eyes`
- [ ] `config/settings.py`: accept `/dev/qbot-*` (and `virtual`, R-209) as well as `/dev/serial/by-id/…`; today anything else is rejected with a warning
- [ ] Set `QBOT_<ORGAN>_PORT` for every organ on the robot laptop
- [ ] Virtual robot bench: show the organ name next to a port the udev rule knows (e.g. `/dev/ttyACM1 (mouth)`), and pick the organ's own Pico by default
- [ ] Document it: how to add a new organ's Pico to the rule, and what to do after swapping a Pico (new serial number, so update the rule)

## Done when
Every organ's Pico is found by name after a reboot and after replugging in
any order, and the virtual robot's benches each pick their own Pico.

## Open questions
- By serial number (follows the Pico, needs updating after a swap) or by hub socket (`/dev/serial/by-path/`, follows the socket, survives a swap)? Serial number is the plan, since the Picos get hard-wired into the hub (R-213) and swaps should be rare.
- Later, maybe: the Pico says what it is when asked (`?` → `mouth`). It would survive swaps, but today the Picos never send anything back, and the crash watch (`nervous_system/pico_console.py`) treats any output as a crash, so that rule would need changing first.

## Log
- 2026-11-20: created after adding the eyes to the virtual robot (R-209): with two Picos plugged in, the bench can't tell which is which. Waiting for the USB hub (R-213).
