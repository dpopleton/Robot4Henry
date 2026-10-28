---
id: R-213
title: "Head power and USB hub"
phase: 2
status: planned
area: head
kind: physical
depends_on: [R-212]
decisions: [D-009, D-013, D-017, D-018]
cost_gbp: 20
updated: 2026-10-28
---
## Goal
A powered USB hub inside the head that every Pico, the USB sound card and
(probably) the camera plug into, plus a power supply for the hub, the
speakers' amp and the WS2812 LEDs. One USB lead and one power lead leave the
head through the bottom panel.

## Why
One Pico per organ (D-009) means 4–6 USB devices, and the amp, screens and
LEDs together draw more than the laptop's USB can supply. Nothing on the
roadmap covered this before. Putting the hub in the head keeps it to one
cable bundle (D-013).

## Tasks
- [x] Rough power budget (2026-10-22, estimates, measure for real later):
      | Part | Typical | Worst |
      |---|---|---|
      | Eyes: 2 screens + Pico | 0.1 A | 0.15 A |
      | Mouth screen + Pico | 0.1 A | 0.15 A |
      | Lights: Pico + 18 WS2812 + antenna | 0.05 A | 0.35 A (capped in firmware; ~1 A uncapped) |
      | Crown: Pico + 4 mics + rec LED | 0.05 A | 0.1 A |
      | R30 PLUS sound board + 2 × 5 W speakers | 0.3 A | 1.5 A at the volume ceiling (more if uncapped) |
      | Camera | 0.15 A | 0.25 A |
      | **Total at 5V** | **~0.75 A** | **~2.5 A** |
- [ ] Measure the real draw once the parts are in
- [ ] Decide how the head is powered (see open questions)
- [ ] Pick a **7-port** powered hub (eyes, mouth, lights and crown Picos, R30 PLUS sound board, camera, one spare) with a **36 W+ adapter**, and either USB 3 ports (0.9 A) or a charging port that also carries data, for the sound board
- [ ] The R30 PLUS sound board (D-017) takes data and power from one port that can give ~1 A; measure its draw at the volume ceiling and only add a separate 5V feed if it browns out or hums. The 18 LEDs run from the lights Pico's VBUS pin with a hard firmware cap (~300 mA, D-018). No cut-up cables
- [ ] Hard-wire the Picos' USB into the hub (no plug-in leads) once it all works
- [ ] Mount the hub and power distribution inside, reachable through the back door
- [ ] Configure every organ's port by `/dev/serial/by-id/…`
- [ ] Route both leads out through the bottom panel's cable exit

## Done when
Every organ in the head runs from the hub at once (eyes animating, LEDs at
full brightness, Qbot speaking loudly) with no resets or brownouts, and only
one USB and one power lead leave the head.

## Open questions
- Decided 2026-10-22: the hub's own adapter is the head's one power lead; no separate
  5V distribution unless the amp hums. Later the body battery (R-502) replaces it.

## Log
- 2026-10-14: created in the head grilling session — power and the hub weren't
  on the roadmap. Hub inside the head decided; power supply still open.
- 2026-10-22: head electronics review: 4 Picos (D-009 holds), no master controller — the router on the brain computer is the master and the hub joins it all. Rough budget ~2.5 A worst case; 7-port hub.
- 2026-10-22: power plan: the hub alone, with a 36 W+ adapter and a charging port feeding the amp and LEDs; no separate 5V distribution unless it hums.
- 2026-10-22: no cut-up cables: USB-C amp in the charging port, LEDs from the lights Pico's VBUS.
- 2026-10-22: audio is now one Picade Max USB Audio board, so the hub needs a port that gives ~1 A with data.
- 2026-10-28: audio is now the salvaged soundbar's R30 PLUS board (D-017), still on one ~1 A port, measured before adding any 5V feed. Lights are now 18 LEDs on VBUS with a hard cap (D-018).
