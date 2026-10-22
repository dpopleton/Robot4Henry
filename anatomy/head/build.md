# Head — build notes

The physical side of the head: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
A 25 × 25 × 15 cm (W × H × D) frame holding the eyes, mouth, speakers, Q and
antenna lights, crown mics, pat button and camera, plus its own USB hub and
sound card. The brain computer (an old laptop) sits beside it on one USB lead
until the body exists. For now the head sits flat on the desk.

## Construction
- **Frame:** 25 mm square beams with a star-shaped hollow profile, 8 × 20 cm
  (front and back squares) and 4 × 10 cm (depth). Each joint is an **outside
  corner** (8) whose star-shaped plugs go into the beams. They're held by
  **M3 bolts** through the beams' counterbored holes into **heat-set inserts** in
  the plugs. Drawings: `images/20cmBeam_Diagram.pdf`, `images/10cmBeam_Diagram.pdf`,
  `images/OutsideCorner_Diagram.pdf`; models in `models/`.
- **Side panels (left and right):** 199.4 × 99.4 mm truss panels with a 2.4 mm
  fin. Drawing: `images/SidePanel_Diagram.pdf`.
- **Top panel:** its own design. The aluminium skin covers it and the **crown sits on top** (R-302).
- **Bottom panel:** designed later, together with the neck (R-401): the neck
  mount plus the cable exit for the head's USB and power leads (R-213).
- **Front:** a main panel with **component panels** bolted into it, one per
  part (the eye panel is the first), so a part can be swapped by reprinting its
  panel. It has eyes, the Q, the **mouth screen centre-bottom**, and two **speaker
  compartments in the bottom corners** on either side of the mouth (R-306).
- **Back:** access door with a **clear acrylic panel** (Henry's idea — so he
  can see inside) and plenty of vents.
- **Skin:** thin aluminium sheet (Henry came back round to it; already bought,
  ~£20). The crown sits on top of the skin. Mic holes are cut through it (R-402).

## Status
- [x] Corners (8) and beams printed and test-fitted
- [x] Both side panels printed
- [x] Back and access door printed and test-fitted
- [x] Assembled with Henry (19–21 Oct): frame + front, back and side main panels
- [x] Acrylic window fitted (tight, but works)
- [ ] Back door hinge pin: the hinge bolt has no room for a nut, so print a pin
- [x] Front main panel printed
- [x] Eye panel printed (R-202)
- [ ] Mouth, speaker, Q and camera panels designed
- [ ] Top panel designed (crown sits on it)
- [ ] Bottom panel — designed with the neck (R-401)
- [ ] USB hub, sound card and power inside the head (R-213)
- [ ] Crown — designed after the mic boards are in hand (see `../crown/`)

## Design notes
- Panels bolt into the frame, so one face can be reprinted without touching
  the rest; components bolt into the front plate the same way.
- Each **Pico sits on its own organ** (on the back of the eyes' enclosure, the
  mouth's mount, inside the crown…) with a short USB lead to the hub.
- **One USB lead and one power lead leave the head** through the bottom
  (R-213, R-402).
- The inside is visible through the back door — keep wiring tidy (R-402).
- Re-flashing firmware happens a lot: keep the Picos' USB ports and BOOTSEL
  buttons reachable through the back door.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| PETG filament | 1 roll | £11 | bought 2026-W42 |
| M2 heat-set inserts + bolts | — | £4 | bought 2026-W42; for mounting electronics |
| M3 heat-set inserts + bolts | — | — | frame (beams to corners) |
| Acrylic sheets | several | £6 | bought 2026-W42; back door window |
| M3 × 20 mm bolts | 100 | £7 | bought 2026-W43 |
| Thin aluminium sheet | — | ~£20 | skin; bought earlier |
