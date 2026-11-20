---
week: 2026-W48
written: 2026-11-20
---
# Suggestions for next week (2026-W48)

A menu to pick from rather than a plan: do whatever you fancy. There are
about 10–20 hours, mostly for design. What actually happened goes in the
journal.

## If you only do one thing
**Speaker boxes and their panels**
([R-306](roadmap/items/physical/R-306-speaker-amplifier-and-enclosure.md)).
The mouth is mounted, so the space either side of it is now fixed, and the
speakers and their board are already in hand. In order:
- Measure the cone and surround, so the front opening clears the surround.
- Design the speaker panel: a 5 cm opening, flared at the back to take the
  5.5 cm frame, inside the 1.5 cm face.
- Design a sealed box per speaker: solid 2–3 mm walls, a wire hole, and
  room for the foam gasket and rubber washers.

Printing a test box and playing `speaker-test` through it would show
whether it buzzes before any more design goes in.

## Physical
- **Top plate** ([R-212](roadmap/items/in_progress/R-212-head-shell.md)):
  the last big shell panel. It needs bolt holes for the crown on rubber
  washers ([R-302](roadmap/items/physical/R-302-crown-design-and-print.md)),
  the big wake button's hole ([R-308](roadmap/items/physical/R-308-wake-and-sleep.md)),
  and a cable path for the crown Pico's USB lead and the recording LED.
- **Crown shape** (R-302): Henry has decided the shape, so it can be
  sketched now. The mic holes and spacing wait for the mic boards to arrive
  and be measured (R-301).
- **Head diagrams** into `anatomy/head/images/` (R-212): front, back, top
  and bottom, while the CAD is open anyway.

## Code
Only if there's time spare from design:
- **Finish R-110**
  ([R-110](roadmap/items/in_progress/R-110-tidy-up-storage-threading.md)):
  stable long-term memory ids and a concurrency test. It's small.

## With Henry
- **The crown sketch:** get his shape onto paper (or a photo of it) for
  `anatomy/crown/images/`, so the CAD follows his design.
- **Photos of the face so far** (eyes and mouth in the head) for the
  anatomy slideshows.

## To buy
- **Crown: Pico 2 and four I2S mics** (~£18,
  [R-301](roadmap/items/physical/R-301-crown-hardware-pico-2-four-i2s-mics.md)).
- **Head USB hub and adapter** (~£20,
  [R-213](roadmap/items/physical/R-213-head-power-and-usb-hub.md)): 7 ports,
  36 W+ adapter, one port giving ~1 A with data for the sound board, and
  ideally per-port power switching (`uhubctl`) for the camera (D-025).
  Once it's here, R-215 (telling the Picos apart) can be done.

Together about £38, inside the month's £40–50.
