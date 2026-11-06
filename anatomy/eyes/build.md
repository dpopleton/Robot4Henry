# Eyes — build notes

The physical side of the eyes: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
Two 1.28" round GC9A01 SPI TFT displays driven by one Raspberry Pi Pico 2.
The code that runs on it is in `organs/eyes/` (see its README).

## Status
- [x] Running on a breadboard (bring-up test)
- [ ] New firmware tested on the Pico (R-201)
- [x] Eye panel designed and printed to bolt into the front main panel (R-202)
- [ ] Soldered and mounted (waiting on the new TS21 iron)

## Wiring
Both displays share the SPI bus, DC, and RST lines — only chip-select
is per-display. GC9A01 is write-only, so no MISO connection is needed.

| Signal     | Pico pin | Left display | Right display | Wire colour (D-021) |
|------------|----------|--------------|---------------|---------------------|
| SCK (SCL)  | GP18     | SCK          | SCK           | Yellow              |
| MOSI (SDA) | GP19     | SDA          | SDA           | Blue                |
| DC         | GP20     | DC           | DC            | Green               |
| RST        | GP21     | RST          | RST           | Purple              |
| CS         | GP17     | CS           | —             | White               |
| CS         | GP16     | —            | CS            | Grey                |
| VCC        | 3V3(OUT) | VCC          | VCC           | Red                 |
| GND        | GND      | GND          | GND           | Black               |

Notes:
- Pico's `3V3(OUT)` pin (physical pin 36) can supply ~300mA — two
  GC9A01 boards typically draw well under that at bring-up brightness,
  but if you see resets/brownouts, move VCC to a separate 3.3V supply
  rather than the Pico's onboard regulator.
- Colours follow the project scheme in
  [D-021](../../docs/decisions/D-021-ten-wire-colours-5v-gets-orange.md).
  Every wire has its own colour, so nothing needs marking. Swapping white
  and grey just swaps the eyes; swapping green and purple gives a blank
  screen. Neither does any damage. No 5V (orange) goes to the eyes.
- **Wire:** the wire bought for this was too thick for the displays'
  connectors, so the eyes use thinner wire that was already lying around
  (2026-11-04). It's fine for these short runs and the small current.
- **Soldered, not plugged** (D-022): the wires go straight into the
  Pico's holes (no header pins), and onto the displays' existing pins.
  Heatshrink on every joint, and the bundle is held near each board so
  flexing doesn't land on the joints. No Dupont connectors.
- **No backlight wire.** BLK is left unconnected, which on these boards
  normally means the backlight stays on at full brightness. The firmware
  still drives GP22 with PWM (`firmware/backlight.py`), but nothing is
  connected to it, so there's no dimming for now (see R-206).
- Both panels run at 40MHz SPI. If the picture is garbled or noisy
  (common on breadboard jumpers), the first thing to try is dropping
  `baudrate` in `panels.py` to `20_000_000` or `10_000_000`.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| GC9A01 1.28" round display | 2 | (bought) | |
| Raspberry Pi Pico 2 | 1 | (bought) | |
