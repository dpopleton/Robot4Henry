# Eyes

Two 1.28" round GC9A01 SPI TFT displays on a Raspberry Pi Pico, standing
in as "eyes" — look direction, blinking, and a set of named mood/activity
expressions (see `firmware/expressions.py`), based on Henry's drawings.

**Current status:** standalone hardware bring-up test. `firmware/main.py`
animates both eyes on its own; it does not yet listen for commands over
`nervous_system` (that integration comes once this actually needs to be
driven by the brain — see `driver.py`, which is the future host-side
half of that, not used by the bring-up test).

## Files

- `firmware/eye_geometry.py`, `firmware/expressions.py`, `firmware/eyes.py`
  — the actual eye-drawing logic. Pure Python, no MicroPython-only calls,
  so the same code runs unmodified on the Pico and in `simulate.py`.
- `firmware/gc9a01.py` — the real SPI panel driver (MicroPython/`machine`
  only). `simulate.py`'s `SimDriver` is a drop-in stand-in for this.
- `firmware/backlight.py`, `firmware/main.py` — Pico-only; not usable
  from the desktop simulator.
- `simulate.py` — desktop preview, see below. Not flashed to the Pico.

## Previewing expressions without hardware

```bash
python organs/eyes/simulate.py
```

Opens a window with both eyes, a button per expression, look-direction
arrows, and a Blink button — the same `eyes.py`/`expressions.py` code
that runs on the Pico, just drawn to a Tkinter canvas instead of the
real panels over SPI. Good for iterating on how an expression should
look before wiring anything up or flashing.

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
- `main.py` runs both panels at 40MHz SPI. If the picture is garbled or
  noisy (common on breadboard jumpers), the first thing to try is
  dropping `baudrate` in `main.py` to `20_000_000` or `10_000_000`.

## Flashing

1. Install MicroPython on the Pico: hold BOOTSEL, plug in over USB, drag
   the `.uf2` from [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/)
   onto the mounted drive.
2. It should boot into MicroPython REPL
2. Copy `firmware/gc9a01.py`, `firmware/eyes.py`, `firmware/backlight.py`,
   and `firmware/main.py` onto the Pico, keeping the same filenames —
   they import each other — with either [Thonny](https://thonny.org)
   (File → Save As → Raspberry Pi Pico) or the command line, below.
3. Power-cycle the Pico. `main.py` runs automatically and both eyes
   should start looking around within a couple of seconds.

### Command line, instead of Thonny

[`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html)
is the official MicroPython CLI tool:

```bash
pip install mpremote

# find the Pico — usually /dev/ttyACM0 on Linux
ls /dev/ttyACM*

# copy the files onto the Pico's root filesystem
mpremote connect auto fs cp organs/eyes/firmware/gc9a01.py :gc9a01.py
mpremote connect auto fs cp organs/eyes/firmware/eyes.py :eyes.py
mpremote connect auto fs cp organs/eyes/firmware/backlight.py :backlight.py
mpremote connect auto fs cp organs/eyes/firmware/main.py :main.py

# soft-reset so it boots into the freshly copied main.py
mpremote connect /dev/ttyACM0 reset
```

Drop `connect /dev/ttyACM0` from each command if only one Pico is
plugged in — `mpremote` auto-detects it.

**Faster iteration while wiring/debugging:** `mpremote mount organs/eyes/firmware`
runs code straight off your laptop's filesystem over the serial
connection, without copying anything onto the Pico's flash. Handy for
tweaking a color or a pin and re-running immediately; do a real `fs cp`
once you're happy with it so it survives a power cycle standalone.

## What the bring-up test does

Both eyes look in the same random direction together most of the time.
Every 5th cycle, one or both blink independently instead — that's
deliberate: if a CS pin is wired to the wrong display, this is where
you'll see the *wrong* eye react, telling you which wire to swap.

Both panels are plain, non-handed GC9A01 boards, mounted the same way
— don't set `mirror_x` on either one. Feeding both eyes the same
`(dx, dy)` already makes them look the same direction; mirroring only
one flips its horizontal axis, so the two converge/diverge instead of
tracking together (cross-eyed).

## Protocol (future)

Once this is wired into `nervous_system` (see `driver.py`), it will
speak the shared protocol from `nervous_system/protocol.py`:

| cmd              | payload                  |
|-------------------|---------------------------|
| `blink`           | `{}`                       |
| `look`            | `{"direction": "left"}`    |
| `set_expression`  | `{"mood": "curious"}`      |

`set_expression`'s mood/activity names are whatever's registered in
`firmware/expressions.py` (`EXPRESSIONS`) — currently: `happy`, `singing`,
`sad`, `mad` (alias `angry`), `serious`, `sleepy`, `sleeping`, `dead`,
`zombie`, `spy`. Anything else (including the `brain/limbic/mood.py`
categories with no artwork yet — `calm`, `curious`, `excited`, `scared`)
falls back to the plain neutral eye. "Pointing" isn't an expression —
it's just `look()` aimed wherever the robot is pointing.
