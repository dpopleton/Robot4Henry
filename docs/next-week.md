---
week: 2026-W42
written: 2026-10-12
---
# Suggestions for next week (2026-W42)

A menu to pick from rather than a plan: do whatever you fancy. Rewritten at
each `/weekly-review`; what actually happened goes in the journal.

## If you only do one thing
**Flash the new eyes firmware onto the Pico** ([R-201](roadmap/items/physical/R-201-eyes-firmware-on-the-real-pico.md)).
It's the only `next` item, costs nothing, and the framebuffer drawing (D-002)
has never run on real hardware. Everything else in the face builds on it.

## Code
- **Virtual robot** ([R-209](roadmap/items/programming/R-209-virtual-robot.md)): unblocks
  the router ([R-207](roadmap/items/blocked/R-207-router-process.md)) and is what
  [R-208](roadmap/items/programming/R-208-brain-sends-its-mood-to-the-router.md) is
  tested against. Settle its three open questions first.
- **Brain sends its mood to the router** ([R-208](roadmap/items/programming/R-208-brain-sends-its-mood-to-the-router.md)):
  can start before R-209 is finished, using `MockOrgan`. A quick first win
  is the task that stops a bad `QBOT_*_PORT` value from stopping the chat starting.
- **Commit the working tree:** the key-facts fix (R-103), the router (R-207)
  and the ticket folders are all still uncommitted.

## Physical
- **Head shell** ([R-212](roadmap/items/in_progress/R-212-head-shell.md)): print,
  assemble and test the back; then model the front frame.
- **Eyes enclosure and soldering** ([R-202](roadmap/items/physical/R-202-eyes-enclosure-and-soldering.md)):
  after R-201, and once the front frame exists to bolt it into.

## With Henry
- **Draw the placeholder moods** ([R-204](roadmap/items/planning/R-204-henry-draws-the-placeholder-moods.md)):
  calm, curious, excited and scared, ideally at a little / quite / very.
- **Qbot's personality** ([R-106](roadmap/items/planning/R-106-qbot-s-personality-sheet.md)):
  a brainstorm session about who Qbot is.

## On the robot laptop
- **Model shoot-out** ([R-104](roadmap/items/programming/R-104-model-shoot-out-on-the-robot-laptop.md)):
  speed only counts there, and the scenario tests make a ready-made test set.

## To buy (budget £40–50/month)
- **Crown parts, about £30** ([R-301](roadmap/items/physical/R-301-crown-hardware-pico-2-four-i2s-mics.md)):
  a Pico 2, four I2S mic boards and a debug probe. Phase 3 is grilled at the
  next weekly review, so it may be worth waiting for that first.
