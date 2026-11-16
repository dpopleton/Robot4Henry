# Eyes — build notes

The physical side of the eyes: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
Two 1.28" round GC9A01 SPI TFT displays driven by one Raspberry Pi Pico 2.
The code that runs on it is in `organs/eyes/` (see its README).

## Status
- [x] Running on a breadboard (bring-up test)
- [x] New firmware tested on the Pico: every mood at every intensity (R-201, 2026-11-06)
- [x] Eye panel designed and printed to bolt into the front main panel (R-202)
- [x] Soldered and mounted (R-202, 2026-11-16): no connectors (D-022), eye plate bolted into the head

## Wiring
Each eye has its own wires, on its own SPI bus, so nothing is spliced
mid-wire (D-026). Only VCC is shared: both red wires go into the one
3V3(OUT) hole and are soldered there together. GC9A01 is write-only, so
no MISO connection is needed.

| Signal     | Left eye (SPI0)  | Right eye (SPI1) | Wire colour (D-021) |
|------------|------------------|------------------|---------------------|
| SCK (SCL)  | GP18 (pin 24)    | GP10 (pin 14)    | Yellow              |
| MOSI (SDA) | GP19 (pin 25)    | GP11 (pin 15)    | Blue                |
| DC         | GP20 (pin 26)    | GP12 (pin 16)    | Green               |
| RST        | GP21 (pin 27)    | GP13 (pin 17)    | Purple              |
| CS         | GP22 (pin 29)    | GP14 (pin 19)    | White               |
| GND        | GND (pin 23)     | GND (pin 18)     | Black               |
| VCC        | 3V3(OUT) (pin 36), shared hole | same hole | Red          |

Notes:
- Pico's `3V3(OUT)` pin (physical pin 36) can supply ~300mA — two
  GC9A01 boards typically draw well under that at bring-up brightness,
  but if you see resets/brownouts, move VCC to a separate 3.3V supply
  rather than the Pico's onboard regulator.
- Colours follow the project scheme in
  [D-021](../../docs/decisions/D-021-ten-wire-colours-5v-gets-orange.md).
  The same colour means the same signal in both bundles; the bundles
  themselves tell the eyes apart. Swapping the two bundles just swaps the
  eyes; swapping green and purple gives a blank screen. Neither does any
  damage. No 5V (orange) goes to the eyes.
- **Wire:** the wire bought for this was too thick for the displays'
  connectors, so the eyes use thinner wire that was already lying around
  (2026-11-04). It's fine for these short runs and the small current.
  On 2026-11-11 Dan went back to his older solid-core wire, which has
  fewer colours. Splicing solid wire is awkward, so the shared lines
  were split onto separate pins (D-026).
- **Left CS moved to GP22** (2026-11-16): there wasn't room to reach
  GP17, so the left eye's CS went to GP22 instead. The unconnected
  backlight PWM moved from GP22 to GP16 to make way.
- **Panels mounted a quarter-turn round** (2026-11-16): fixed in the
  firmware, not by re-mounting. `panels.py` turns the left picture 90°
  anticlockwise and the right one 90° clockwise (`rotation` in `gc9a01.py`).
- **Soldered, not plugged** (D-022): the wires go straight into the
  Pico's holes (no header pins), and onto the displays' existing pins.
  Heatshrink on every joint, and the bundle is held near each board so
  flexing doesn't land on the joints. No Dupont connectors.
- **No backlight wire.** BLK is left unconnected, which on these boards
  normally means the backlight stays on at full brightness. The firmware
  still drives GP16 (pin 21) with PWM (`firmware/backlight.py`), but nothing is
  connected to it, so there's no dimming for now (see R-206).
- Both panels run at 40MHz SPI. If the picture is garbled or noisy
  (common on breadboard jumpers), the first thing to try is dropping
  `baudrate` in `panels.py` to `20_000_000` or `10_000_000`.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| GC9A01 1.28" round display | 2 | (bought) | |
| Raspberry Pi Pico 2 | 1 | (bought) | |
