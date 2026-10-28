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

## Electronics layout
No master controller: the router on the brain computer is the master (D-003),
and a powered hub inside the head joins everything to it (D-013). One Pico per
organ (D-009):

| On the hub | Drives | Notes |
|---|---|---|
| Eyes Pico | 2 round screens | working |
| Mouth Pico | mouth screen; sets the sound board's volume by emulating its encoder | R-210, D-017 |
| Lights Pico | Q and head glow (two salvaged 9-LED WS2812 U boards on one chain), antenna tip (1 RGB LED, wired down), big wake button on top | R-211, D-015, D-018 |
| Crown Pico (C) | 4 mics, recording LED on the face | R-303 |
| Jieli R30 PLUS (salvaged soundbar board: USB sound card + stereo amp + Bluetooth) | 2 × 5.5 cm 4 Ω 5 W salvaged speakers in sealed boxes behind the 5 cm face openings | R-306, D-017 |
| Camera | video LED on the face, opposite the recording LED | R-601 |

Power: the hub's own adapter (36 W+) is the head's one power lead. Picos run
from USB data ports. The R30 PLUS sound board takes data and power from a hub port
that can give ~1 A (measure at the volume ceiling), and the 18 LEDs run from the lights Pico's VBUS pin with a hard brightness cap (~300 mA). No
cut-up cables. Rough worst case ~2.5 A (R-213). The large mechanical button on top is the
wake button, and a press while awake can be a pat (R-308, R-313).

## Design notes
- **Vibration isolation:** the speaker boxes and the crown both sit on rubber
  grommets or washers, so the speakers don't shake the frame and Qbot's own
  voice doesn't travel through it into the mics (R-306, R-302).
- **Speakers:** each 5.5 cm speaker sits in its own sealed, stuffed box
  behind a 5 cm opening in the 1.5 cm-thick face. The opening is bevelled at
  the back to take the bigger frame, with a foam gasket, and nothing sticks
  out. The aluminium skin stays flush, with parallel slots over each speaker
  (a third to a half open) and cloth behind, fixed firmly so it doesn't buzz.
- **Head glow:** one LED board lights the inside so it glows through the
  clear back (D-018). The recording/video LEDs get sealed light boxes, and the
  camera is shielded from the glow. Mock it up before designing mounts.
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
| M3 rubber grommets/washers | 1 pack | ~£3 | crown and speaker-box mounts |
| Broken USB/Bluetooth soundbar | 1 | £0 | salvaged 2026-10-28: 2 speakers, R30 PLUS amp board, 2 U-shaped LED boards; case discarded |
| Foam tape, polyester stuffing, speaker cloth | — | ~£3 | speaker boxes and slots |
