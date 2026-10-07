# Eyes

Two 1.28" round GC9A01 SPI TFT displays on a Raspberry Pi Pico, standing
in as "eyes" — look direction, blinking, and a set of named mood/activity
expressions (see `firmware/expressions.py`), based on Henry's drawings.

**Current status:** `firmware/main.py` listens on USB serial for two
inputs — **direction** and **expression** (with intensity 1-3) — sent
separately or together by `driver.py`, and idles naturally in between.
Every `brain/limbic/mood.py` category has an expression at all three
intensities (calm/curious/excited/scared are placeholder art until
Henry draws them). Not yet wired into the brain itself: nothing calls
`EyesOrgan.show_mood()` yet. The original standalone wiring test is
`firmware/bringup.py`.

## Files

- `firmware/eye_geometry.py`, `firmware/expressions.py`, `firmware/eyes.py`
  — the actual eye-drawing logic. Pure Python, no MicroPython-only calls,
  so the same code runs unmodified on the Pico and in `simulate.py`.
- `firmware/gc9a01.py` — the real SPI panel driver (MicroPython/`machine`
  only). `simulate.py`'s `SimDriver` is a drop-in stand-in for this.
- `firmware/eye_protocol.py` — the compact wire format (see "Protocol"
  below). Pure Python, imported by both the Pico and `driver.py`.
- `firmware/framebuffer.py` — draws into RAM with MicroPython's
  `framebuf`, then sends each eye to its panel in one SPI write.
- `firmware/panels.py`, `firmware/backlight.py`, `firmware/main.py`,
  `firmware/bringup.py` — Pico-only; not usable from the desktop
  simulator.
- `simulate.py` — desktop preview, see below. Not flashed to the Pico.
- `expression_status.py` / `EXPRESSIONS.md` — see "Tracking expressions"
  below.

## How expressions move

`Eye` tracks a look direction (`dx, dy`) and a current expression
together — calling `look()` moves the pupil (or whatever stands in for
it) under whatever expression is showing, rather than the two being
separate modes. `Face` (also in `eyes.py`) coordinates a left/right
`Eye` pair so they always look the same way, and drives idle motion via
`tick()`: mostly holding still on `look_at()`'s target — the long-term
hook for "look at whoever's talking" — with brief glances away and
occasional blinks, plus per-expression flourishes like a twitching
eyebrow or dripping tears (`animates` in the registry below).

Not every expression moves the same way — `firmware/expressions.py`'s
`REGISTRY` declares, per expression, whether it's `trackable` (can look
around at all), `blinks`, and `animates`. "dead" and "sleeping" are
`trackable=False`: their render functions ignore `dx`/`dy` outright, so
they're fully static by design, not just idle-still.

## Tracking expressions

```bash
python organs/eyes/expression_status.py   # regenerates EXPRESSIONS.md
```

`firmware/expressions.py`'s `REGISTRY` is the single source of truth
for every expression — implemented or not — including which drawing
it's based on, what's still unclear, and what Henry needs to redraw.
`EXPRESSIONS.md` is generated from it, so it can't drift out of sync
with the code; re-run the script after editing `REGISTRY` (new
expression, changed behavior, a drawing finally deciphered) rather than
hand-editing the `.md`.

## Previewing expressions without hardware

```bash
python organs/eyes/simulate.py
```

Opens a window with both eyes, a button per expression, intensity 1-3,
look-direction arrows, a Blink button, and a "Command" box that takes
the exact lines the host sends the Pico (e.g. `Ehappy:3 D-40,25`) — the same `eyes.py`/`expressions.py` code
that runs on the Pico, just drawn to a Tkinter canvas instead of the
real panels over SPI. Idle movement runs automatically (uncheck "Idle
movement" to freeze a frame for a close look). Good for iterating on
how an expression should look before wiring anything up or flashing.

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

## Flashing

1. Install MicroPython on the Pico: hold BOOTSEL, plug in over USB, drag
   the `.uf2` from [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/)
   onto the mounted drive.
2. It should boot into MicroPython REPL
2. Copy every `.py` in `firmware/` except `__init__.py` onto the Pico,
   keeping the same filenames —
   they import each other — with either [Thonny](https://thonny.org)
   (File → Save As → Raspberry Pi Pico) or the command line, below.
3. Power-cycle the Pico. `main.py` runs automatically: both eyes open
   within a couple of seconds and idle until commands arrive.

### Command line, instead of Thonny

[`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html)
is the official MicroPython CLI tool:

```bash
pip install mpremote

# find the Pico — usually /dev/ttyACM0 on Linux
ls /dev/ttyACM*

# copy the files onto the Pico's root filesystem
cd organs/eyes/firmware
for f in gc9a01 eye_geometry eye_protocol expressions eyes framebuffer backlight panels bringup main; do
  mpremote connect auto fs cp $f.py :$f.py
done
cd -

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

`mpremote run organs/eyes/firmware/bringup.py` (with the other files
already copied over) — it replaces `main.py` until the next reset.

Both eyes look in the same random direction together most of the time.
Every 5th cycle, one or both blink independently instead — that's
deliberate: if a CS pin is wired to the wrong display, this is where
you'll see the *wrong* eye react, telling you which wire to swap.

Both panels are plain, non-handed GC9A01 boards, mounted the same way
— don't set `mirror_x` on either one. Feeding both eyes the same
`(dx, dy)` already makes them look the same direction; mirroring only
one flips its horizontal axis, so the two converge/diverge instead of
tracking together (cross-eyed).

## Protocol

The host sends one ASCII line per update, built and parsed by the same
`firmware/eye_protocol.py` on both ends. Every field is optional, so
direction and expression can go separately or together:

| line               | meaning                                                  |
|--------------------|----------------------------------------------------------|
| `D-40,25`          | look direction, dx,dy in [-100, 100] (+x screen-right, +y down) |
| `Ehappy:3`         | expression + intensity 1-3                               |
| `Ehappy`           | expression at its default intensity (2)                  |
| `B`                | blink                                                    |
| `Ehappy:3 D-40,25` | both at once — one redraw, not two                       |

From Python:

```python
from nervous_system.serial_transport import SerialTransport
from organs.eyes.driver import EyesOrgan

eyes = EyesOrgan(SerialTransport("/dev/ttyACM0"))
eyes.connect()
eyes.look((-0.4, 0.25))              # direction only
eyes.set_expression("scared", 3)     # expression only
eyes.show_mood(mood, direction="left")  # a brain.limbic Mood, plus direction, in one line
```

Or type lines straight into a serial terminal (`mpremote connect auto`
won't do — it interrupts `main.py`; use e.g. `picocom /dev/ttyACM0`).

Why it's fast:
- **Small:** a direction update is at most 11 bytes (vs ~70 as JSON).
  ASCII rather than binary because a 0x03 byte would hit MicroPython's
  Ctrl-C handler and kill `main.py`.
- **Latest wins:** `main.py` drains *every* waiting line before drawing
  and merges them, so if the host streams direction faster than the
  panels can redraw, stale positions are skipped instead of queuing up.
  A repeat of the current state doesn't redraw at all.
- **One SPI write per eye:** shapes are filled in C by `framebuf` into a
  RAM buffer, then pushed whole (~23ms per eye at 40MHz) — no
  per-scanline Python loop, no visible half-drawn frames.
- **Never blocks:** blinks are non-blocking, and an incoming direction
  cuts short any idle glance.

Expression names are whatever's in `firmware/expressions.py`'s
`REGISTRY` — see `EXPRESSIONS.md`. Anything unregistered (including
`neutral`) shows the plain neutral eye.
