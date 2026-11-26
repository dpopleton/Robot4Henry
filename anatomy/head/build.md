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
- [x] Back door hinge pin: the hinge bolt has no room for a nut, so a pin was printed and fitted (2026-11-20)
- [x] Front main panel printed
- [x] Eye panel printed and the eyes mounted (R-202)
- [x] Mouth panel printed (reprinted once: bolt holes were off) and the mouth mounted (R-210)
- [x] Speaker boxes printed (2026-11-26, ~5 × 5 × 7 cm); speakers not fitted yet
- [ ] Speaker panels: designed, printing 2026-11-26
- [ ] Q and camera panels designed
- [ ] Top panel designed (crown sits on it)
- [ ] Bottom panel — designed with the neck (R-401)
- [ ] USB hub, sound card and power inside the head (R-213): hub bought and working (2026-11-24); where it mounts waits on the speaker boxes
- [ ] Crown — designed after the mic boards are in hand (see `../crown/`)

## Electronics layout
No master controller: the router on the brain computer is the master (D-003),
and a powered hub inside the head joins everything to it (D-013). One Pico per
organ (D-009):

| On the hub | Drives | Notes |
|---|---|---|
| Eyes Pico | 2 round screens | working |
| Mouth Pico | mouth screen | R-210 |
| Lights Pico | Q and head glow (two salvaged 9-LED WS2812 U boards on one chain), antenna tip (1 RGB LED, wired down), big wake button on top | R-211, D-015, D-018 |
| Crown Pico (C) | 4 mics, recording LED on the face | R-303 |
| Waveshare USB TO AUDIO (USB sound card + 2.6 W stereo amp; volume set from the laptop) | 2 × 5.5 cm 4 Ω 5 W salvaged speakers in sealed boxes behind the 5 cm face openings | R-306, D-027 (the R30 PLUS board is the fallback, D-017) |
| Camera | video LED on the face, opposite the recording LED | R-601 |

Power: the hub's own adapter (36 W+) is the head's one power lead. Picos run
from USB data ports. The Waveshare sound card takes data and power from a hub port
(measure its draw at full volume), and the 18 LEDs run from the lights Pico's VBUS pin with a hard brightness cap (~300 mA). No
cut-up cables. Rough worst case ~2.5 A (R-213). The large mechanical button on top is the
wake button, and a press while awake can be a pat (R-308, R-313).

## Sound board and speakers (tested 2026-11-22)
**The board** is silkscreened `V18&12-MAIN-V4.0 2023-11-07`, an unbranded
soundbar main board with no published specs. It shows up over USB as
`R30 PLUS` (`5943:3130`).
- **Main chip:** Jieli, marked `AC23BP1X659-55F4`. In Jieli's marking scheme
  `AC23` is the year (2023) and the part after the dash is the model: an
  **AC6955F** (BR23/AC695N family, QSOP24, stereo DAC). The `4` is probably
  4 Mbit flash. The AC6955F datasheet link is dead; the same-family AC6956C
  datasheet gives **VDDIO 3.3 V** (2.2–3.6 V), inputs limited to VDDIO + 0.3 V,
  and **10 kΩ internal pull-ups**. A few pins (PB0, PB2, PB5) can pull up to
  5 V, so still measure the encoder lines before soldering.
- **Amp:** LTK5209 (marked `2458KK`). Stereo class D/AB, rated up to ~7.9 W
  per channel into 3 Ω at 7 V; on USB's 5 V expect roughly 3 W per channel
  into 4 Ω. No volume control, only EN/MODE pins (on/off and mode), with
  over-temperature and short-circuit protection.
- **USB:** the host only gets mute switches. The HID interface is input-only:
  it sends volume keys *to* the laptop, so it can't set the volume.
- **White residue** around some contacts: probably flux. Clean with isopropyl
  alcohol and a toothbrush, then check the joints for corrosion.

**Encoder (volume knob):** 5 pins underneath plus 2 mounting tabs. The row of
3 is A / common / B (common is usually the middle one, to GND); the row of 2
is the push switch. Volume control: A, B and GND to the mouth Pico (GP2,
GP3, GND), open-drain, only ever pulling low (D-017, R-306).

**Measured** with the webcam mic, speakers loose on the desk, at full digital
level:
- Both speakers work; left and right within ~5 dB of each other.
- At the power-on volume, tones were 10–43 dB above the room's noise from
  200 Hz to 8 kHz (loudest at 3 kHz), with nothing at 100 Hz. That's quiet:
  the room level rose only ~2 dB.
- Turning the knob up gave **+38 dB** over the power-on level, in smooth
  steps of ~1–2 dB, and all the way down is silent. Plenty of headroom.

## Waveshare USB TO AUDIO (tested 2026-11-25)
Both 5.5 cm speakers plugged into it, loose on the desk ~30 cm from the
laptop, measured with the webcam mic (through PulseAudio, because raw ALSA
capture from the webcam gave I/O errors).
- **Shows up as** `card N: Device [USB PnP Audio Device]` (Solid State System
  chip, USB ID `0c76:1203`). Address it as `plughw:CARD=Device,DEV=0`. The
  name is generic, so another cheap dongle could clash; pin it by USB path or
  ID later.
- **Volume from the laptop works:** `amixer -c Device -- sset Speaker -20dB`.
  Range 0–1008, labelled −∞ to 0 dB, plus a mute switch. It changes the
  loudness steadily and in order, but each labelled 10 dB step was only ~5–6 dB
  at the mic. From −40 to 0 dB it got ~18 dB louder.
- **Both channels work.** At mixer −20 dB, tones were 35–70 dB above the
  room's noise from 200 Hz to 8 kHz (loudest at 3 kHz), with nothing at
  100 Hz, like the R30 board. Left was ~10–15 dB weaker than right at
  200–500 Hz, probably because of where the loose speakers were lying.
- Already louder at −20 dB than the R30 board at its power-on level.
- **No trim screw** on this model, so the loudest it goes is the amp's own
  maximum. Accepted for now: the software clamp is the limit. If it's ever
  too loud, a resistor in series with each speaker fixes it (D-027, R-306).
- Chosen over the R30 board on 2026-11-26 (D-027).

## Design notes
- **Vibration isolation:** the speaker boxes and the crown both sit on rubber
  grommets or washers, so the speakers don't shake the frame and Qbot's own
  voice doesn't travel through it into the mics (R-306, R-302).
- **Speakers:** each 5.5 cm speaker sits in its own sealed, stuffed box
  (trying **~100–120 ml** instead of ~250 ml, to save space; fine for a voice,
  which needs little bass) behind a 5 cm opening in the 1.5 cm-thick face. The opening is bevelled at
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
| PETG filament | 2 rolls | £22 | bought 2026-W42 and 2026-W48 (£11 each) |
| M2 heat-set inserts + bolts | — | £4 | bought 2026-W42; for mounting electronics |
| M3 heat-set inserts + bolts | — | — | frame (beams to corners) |
| Acrylic sheets | several | £6 | bought 2026-W42; back door window |
| M3 × 20 mm bolts | 100 | £7 | bought 2026-W43 |
| Thin aluminium sheet | — | ~£20 | skin; bought earlier |
| M3 rubber washers | 1 pack | £5 | bought 2026-W48; crown and speaker-box mounts |
| Broken USB/Bluetooth soundbar | 1 | £0 | salvaged 2026-10-28: 2 speakers, R30 PLUS amp board, 2 U-shaped LED boards; case discarded |
| Waveshare USB TO AUDIO (USB sound card + 2.6 W amp) | 1 | ~£8 | bought 2026-11-23; replaces the R30 board (D-027) |
| Powered USB hub | 1 | £25 | bought 2026-11-24, working (R-213) |
| Foam tape, polyester stuffing, speaker cloth | — | ~£3 | speaker boxes and slots |
