---
week: 2026-W47
written: 2026-11-16
---
# Suggestions for next week (2026-W47)

A menu to pick from rather than a plan: do whatever you fancy. There are
about 5 computer hours and maybe more at the bench. What actually happened
goes in the journal.

## If you only do one thing
**The mouth on its real screen**
([R-210](roadmap/items/in_progress/R-210-mouth-display.md)). It's the eyes'
path again, and it uses both kinds of time:
- **Computer:** the ST7789 driver and `main.py`. Everything above the driver
  is already built and tested, and Henry has signed off the look.
- **Bench:** a breadboard check of the pin order and controller, then solder
  it onto the panel you've just printed.

It would make the mouth the second face part in the head.

## Code
- **Move the eyes onto a virtual-robot panel**
  ([R-209](roadmap/items/in_progress/R-209-virtual-robot.md)), so
  `simulate.py` can go (D-023). R-207 (router) has been blocked on this since
  October, and the router is what lets the brain's mood reach the face.
- **Build `_personality()` from the approved sheet**
  ([R-106](roadmap/items/planning/R-106-qbot-s-personality-sheet.md)), plus a
  scenario test. Qbot still isn't the boy from the sun in conversation.
- **Finish R-110**
  ([R-110](roadmap/items/in_progress/R-110-tidy-up-storage-threading.md)):
  stable long-term memory ids and a concurrency test.

## Physical
- **Solder and mount the mouth** onto its printed panel (R-210). Breadboard
  it first, as with the eyes.
- **Photos of the eyes in the head** for `anatomy/eyes/images/` (R-202). They
  make good slideshow frames for Henry.
- **Speaker box CAD**
  ([R-306](roadmap/items/physical/R-306-speaker-amplifier-and-enclosure.md)):
  the mouth panel's position now fixes the space the speakers sit in on
  either side.

## With Henry
- **Show him the eyes in the head**, ideally with a photo session, and check
  the Henry text for the eye plate in `anatomy/eyes/manifest.yaml`.
- **Start him on the arms** (R-701), if he's keen: drawings of what he
  imagines. They're a long way off, but his design is what Phase 7 works from.

## To buy
- **Crown: Pico 2 and four I2S mics** (~£18,
  [R-301](roadmap/items/physical/R-301-crown-hardware-pico-2-four-i2s-mics.md)).
  November's budget is untouched, and the parts take a while to arrive.
