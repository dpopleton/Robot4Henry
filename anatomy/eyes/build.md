# Eyes — build notes

The physical side of the eyes: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
Two 1.28" round GC9A01 SPI TFT displays driven by one Raspberry Pi Pico 2.
The code that runs on it is in `organs/eyes/` (see its README).

## Status
- [x] Running on a breadboard (bring-up test)
- [ ] New firmware tested on the Pico (R-201)
- [ ] Enclosure designed and printed to bolt into the front frame (R-202)
- [ ] Soldered and mounted

## Wiring
Both displays share the SPI bus, DC, and RST lines — only chip-select
is per-display. GC9A01 is write-only, so no MISO connection is needed.

| Signal            | Pico pin | Left display | Right display |
|-------------------|----------|--------------|----------------|
| SCK (SCL)         | GP18     | SCK          | SCK            |
| MOSI (SDA)        | GP19     | SDA          | SDA            |
| DC                | GP20     | DC           | DC             |
| RST               | GP21     | RST          | RST            |
| CS                | GP17     | CS           | —              |
| CS                | GP16     | —            | CS             |
| VCC               | 3V3(OUT) | VCC          | VCC            |
| GND               | GND      | GND          | GND            |
| BLK (backlight)   | GP22     | BLK          | BLK            |

Notes:
- Pico's `3V3(OUT)` pin (physical pin 36) can supply ~300mA — two
  GC9A01 boards typically draw well under that at bring-up brightness,
  but if you see resets/brownouts, move VCC to a separate 3.3V supply
  rather than the Pico's onboard regulator.
- BLK is now driven by GP22 with PWM (`firmware/backlight.py`) instead
  of being hard-wired to 3V3, so brightness is software-adjustable —
  handy for dimming for sleepy/night expressions later. Both panels'
  BLK pins still tie together to this one GPIO, so it's one shared
  brightness, not per-eye. Before wiring this up, check your specific
  breakout's BLK circuitry: most round GC9A01 modules already have an
  onboard transistor driving the backlight LED, so the pin is a normal
  logic input safe to drive from a GPIO — but if yours wires BLK
  straight to the LED with no onboard driver, don't connect it directly
  to a GPIO (check the LED's current draw against the GPIO's ~12mA
  recommended limit first, or drive it through a transistor instead).
- Both panels run at 40MHz SPI. If the picture is garbled or noisy
  (common on breadboard jumpers), the first thing to try is dropping
  `baudrate` in `panels.py` to `20_000_000` or `10_000_000`.

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| GC9A01 1.28" round display | 2 | (bought) | |
| Raspberry Pi Pico 2 | 1 | (bought) | |
