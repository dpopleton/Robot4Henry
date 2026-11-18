# Mouth — build notes

The physical side of the mouth: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
A SEENGREAT 2" IPS LCD module (Amazon code X001LUD8NR), on its own Pico
(D-009). Listings for this module say 240×320 with an ST7789V(W)
controller; we use it sideways (320×240). It has a plug-in header and 8
solder holes, including a backlight pin (BL), so brightness can be
controlled. White lines on black: flat when quiet, a mouth-shaped
seismograph while Qbot talks (R-210).

## Status
- [x] Find the display and identify it (2026-11-05)
- [x] Wiring (2026-11-17)
- [x] Firmware deployed and working on the breadboard Pico (2026-11-17): white line on black, the right way up, moving with speech from the bench. Defaults were right first time (240×320, inversion on, `rotation=90`, 40MHz)
- [x] Rewired onto the Pico that goes in the head (same pins as the table below), flashed and tested (2026-11-18)
- [x] Mouth panel printed (2026-11-15). The first print's bolt holes were in the wrong place, so it was reprinted
- [x] Mounted in the front frame (2026-11-18), Pico on the back of the bracket, and tested in place

## Drawings and models
- `images/Mouth Bracket Drawing 1.pdf`: the bracket drawing (79.6 × 49.6 × 15 mm; Ø3.8 corner holes bolt it to the plate, Ø3 holes for the screen).
- `models/MouthInsert - Mouth Bracket.3mf`: the printed bracket.

## Wiring
The pins are set in `organs/mouth/firmware/mouth_panel.py`; keep the
two the same. It uses exactly the left eye's pins (SPI0), so the
mouth's code and the eyes' code read the same, and either Pico can be
tried with either screen on a breadboard. The ST7789 is write-only, so
no MISO.

| Signal (module silkscreen) | Pico 2 pin      | Wire colour (D-021) |
|----------------------------|-----------------|---------------------|
| CLK (SCK)                  | GP18 (pin 24)   | Yellow              |
| DIN (MOSI)                 | GP19 (pin 25)   | Blue                |
| DC                         | GP20 (pin 26)   | Green               |
| RST                        | GP21 (pin 27)   | Purple              |
| CS                         | GP22 (pin 29)   | White               |
| BL (backlight, PWM)        | GP16 (pin 21)   | Grey                |
| GND                        | GND (pin 23)    | Black               |
| VCC                        | 3V3(OUT) (pin 36) | Red               |

Later, for the sound board's volume (D-017, R-306), not wired yet:

| Signal | Pico 2 pin | Notes |
|---|---|---|
| Encoder A | GP2 (pin 4) | Open-drain: only ever pulled low |
| Encoder B | GP3 (pin 5) | Same; a transistor per line if the board's lines are above 3.3 V |
| GND | GND (pin 3) | Shared with the R30 PLUS board |

Notes:
- **Check the silkscreen first.** The pin order above is the expected
  one (see Open questions); match by name, not by position.
- **VCC on 3.3V, not 5V.** Some of these modules take 5V through an
  onboard regulator, but 3.3V is safe either way and matches the logic
  level. No orange wire goes to the mouth.
- **Backlight wired from the start** (unlike the eyes, R-206): grey,
  because it's the mouth's second "enable" line and it only has one CS.
  `mouth_panel.py` has its own copy of the eyes' `Backlight` (one module
  name per organ, so it can't share `backlight.py`).
- **40MHz SPI**, as the eyes. The 80ms frame (`TICK_MS` in
  `firmware/mouth.py`) was measured at 40MHz: ~31ms to push a 320×240
  frame. If the picture is garbled, drop to 20MHz: the push then takes
  ~62ms, so with drawing a frame takes ~90ms and `TICK_MS` would need
  raising to about 100.
- **Sideways:** the panel is 240×320 portrait; the firmware draws
  320×240 (`firmware/mouth_geometry.py`), so `st7789.py` uses
  `rotation=90`. If the picture is upside down, use 270 in
  `mouth_panel.py`, not a re-mount (as the eyes did). If the line is
  black on white, pass `invert=False`.
- **Soldered, not plugged** (D-022), heatshrink on every joint, as the
  eyes.

## Flashing, running and testing
**Flashing the Pico**
1. Install MicroPython: hold BOOTSEL, plug the Pico 2 in over USB, and
   drag the Pico 2 `.uf2` (from
   [micropython.org/download/RPI_PICO2](https://micropython.org/download/RPI_PICO2/))
   onto the drive that appears.
2. Copy the mouth firmware and the shared `organs/pico_common/` files and
   restart the Pico (close Thonny/picocom first; the user needs to be in
   `dialout`):
   ```bash
   python organs/deploy.py mouth --dry-run        # lists: framebuffer, line_reader, mouth, mouth_geometry, mouth_protocol
   python organs/deploy.py mouth                  # or --port /dev/ttyACM1 if the eyes' Pico is plugged in too
   ```
   If the Pico answers commands with `NameError: name 'S0' isn't defined`,
   it has no `main.py` and is sitting at its Python prompt: deploy again.

**Running**
- On power-up `main.py` shows a flat line and waits for
  commands over USB serial.
- **Typing commands by hand:** `picocom /dev/ttyACM0`, then `S1` (talk:
  it wiggles by itself), `S1 L80` (loud), `L20` (quiet), `S0` (back to
  flat). Use picocom, not mpremote, which stops `main.py` when it connects.
- **From the bench:** `python -m virtual_robot --only mouth`, set the
  switch to **Both**, pick the port, and press **Say it**: the screen
  and the on-screen mouth should move together.

**Testing**
- Without hardware: `python -m pytest tests/organs/test_mouth_*.py`
  (protocol, drawing, levels, driver; also `test_micropython_compat.py`).
- On the breadboard, in order:
  1. Screen lights up (backlight) and shows a flat white line, centred,
     the right way up, not mirrored.
  2. `S1` wiggles; `S1 L100` reaches near the top and bottom without
     going off screen; `S0` settles to flat within a second.
  3. Random junk lines in picocom don't crash it.
  4. Note the controller (ST7789V or VW) and resolution, and tick them
     off in Open questions and R-210.

## Open questions
- Settled 2026-11-17: the screen works with the wiring below (matched by silkscreen name), at 240×320, so the listing was right. ST7789V or VW is still unknown and doesn't matter: same commands.
- Sound waves are driven by levels from the laptop (D-024), so no audio wiring to the mouth.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| SEENGREAT 2" IPS LCD (ST7789, 240×320) | 1 | (bought) | X001LUD8NR |
| Raspberry Pi Pico 2 | 1 | ~£5 | |
