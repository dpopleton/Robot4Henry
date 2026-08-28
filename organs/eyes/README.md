# Eyes

Two 1.28" round GC9A01 SPI TFT displays on a Raspberry Pi Pico, standing
in as "eyes" — a look direction and a blink, nothing fancier yet.

**Current status:** standalone hardware bring-up test. `firmware/main.py`
animates both eyes on its own; it does not yet listen for commands over
`nervous_system` (that integration comes once this actually needs to be
driven by the brain — see `driver.py`, which is the future host-side
half of that, not used by the bring-up test).

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
| BLK (backlight)   | 3V3(OUT) | BLK          | BLK            |

Notes:
- Pico's `3V3(OUT)` pin (physical pin 36) can supply ~300mA — two
  GC9A01 boards typically draw well under that at bring-up brightness,
  but if you see resets/brownouts, move VCC/BLK to a separate 3.3V
  supply rather than the Pico's onboard regulator.
- `main.py` runs both panels at 40MHz SPI. If the picture is garbled or
  noisy (common on breadboard jumpers), the first thing to try is
  dropping `baudrate` in `main.py` to `20_000_000` or `10_000_000`.

## Flashing

1. Install MicroPython on the Pico: hold BOOTSEL, plug in over USB, drag
   the `.uf2` from [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/)
   onto the mounted drive.
2. Open the project in [Thonny](https://thonny.org), set the interpreter
   to "MicroPython (Raspberry Pi Pico)".
3. Copy `firmware/gc9a01.py`, `firmware/eyes.py`, and `firmware/main.py`
   onto the Pico (File → Save As → Raspberry Pi Pico) — keep the same
   filenames, they import each other.
4. Power-cycle the Pico. `main.py` runs automatically and both eyes
   should start looking around within a couple of seconds.

## What the bring-up test does

Both eyes look in the same random direction together most of the time.
Every 5th cycle, one or both blink independently instead — that's
deliberate: if a CS pin is wired to the wrong display, this is where
you'll see the *wrong* eye react, telling you which wire to swap. If
one eye's pupil looks mirrored relative to the other once both are
mounted, toggle `mirror_x` on that display's `GC9A01(...)` call in
`main.py`.

## Protocol (future)

Once this is wired into `nervous_system` (see `driver.py`), it will
speak the shared protocol from `nervous_system/protocol.py`:

| cmd              | payload                  |
|-------------------|---------------------------|
| `blink`           | `{}`                       |
| `look`            | `{"direction": "left"}`    |
| `set_expression`  | `{"mood": "curious"}`      |
