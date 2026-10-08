# Eyes

## Purpose

Qbot's eyes: two round screens that **look** somewhere and show an
**expression** — every mood in `brain/limbic/mood.py` at intensity 1–3,
plus a few of Henry's extras — with natural idle blinking and glancing in
between. The firmware runs on a Raspberry Pi Pico 2. This folder also holds
the host-side driver the brain computer uses to talk to it.

Hardware (displays, wiring, enclosure, parts) lives in
[`anatomy/eyes/build.md`](../../anatomy/eyes/build.md).

## How it works

```
host: EyesOrgan (driver.py) ──"Ehappy:3 D-40,25\n"──▶ USB serial
Pico: main.py → LineReader → eye_protocol.Update → Face.update()
                                                     ├─ Eye (left)  → BufferedPanel → GC9A01
                                                     └─ Eye (right) → BufferedPanel → GC9A01
```

- **`firmware/main.py`** loops forever. It sleeps until input arrives or the
  next idle tick is due (every 150ms). It drains *every* line waiting on
  stdin, merges them into one `Update` (newest wins), applies it with
  `Face.update()`, then calls `Face.tick()` when a tick is due.
- **`firmware/eye_protocol.py`** — the wire format, parsed on the Pico and
  built on the host by the same code (see Interfaces).
- **`firmware/eyes.py`** — `Eye` holds one eye's state (expression,
  intensity, look direction, animation clock) and renders it. `Face`
  coordinates the pair:
  - `update()` applies any mix of expression/intensity/direction and
    redraws **at most once**, or not at all if nothing changed.
  - `tick()` does idle life: mostly holding the gaze, brief glances away,
    occasional blinks, and per-expression animation (tears, twitching brow).
  - Blinks are non-blocking: close now, reopen on the next tick or update.
  - An explicit direction cuts short an idle glance.
- **`firmware/expressions.py`** — one render function per expression, plus
  `REGISTRY`, the single source of truth for each expression's behaviour:
  `trackable` (can it look around?), `blinks`, `animates` (true/false or
  the intensities that animate), and status/source/notes for
  `EXPRESSIONS.md`. Anything not in the registry falls back to the plain
  neutral eye.
- **`firmware/framebuffer.py`** — `BufferedPanel` draws shapes into a RAM
  frame with MicroPython's built-in `framebuf`, then `show()` pushes the
  whole frame to the panel in one SPI write. Both eyes share one buffer.
- **`firmware/gc9a01.py`** (panel driver), **`panels.py`** (pin setup),
  **`backlight.py`** (PWM brightness) — Pico-only.
- **`firmware/bringup.py`** — the original standalone wiring test.
- **`simulate.py`** — desktop preview of the same drawing code on a Tk canvas.
- **`expression_status.py`** → **`EXPRESSIONS.md`** — generated status of
  every expression.

The drawing code (`eye_geometry`, `expressions`, `eyes`, `eye_protocol`)
is plain Python with no MicroPython-only calls, so it runs unchanged on the
Pico, in the simulator and in the tests. A drawing driver only needs
`fill`, `fill_circle` and `fill_polygon` (and optionally `show`).

## Why it's built this way

- **Two independent inputs, one line format** — [D-001](../../docs/decisions/D-001-eyes-ascii-line-protocol.md):
  direction will stream fast from the crown while mood changes once per
  turn. ASCII, not JSON (size) and not binary (a `0x03` byte is Ctrl-C to
  MicroPython).
- **Newest wins, never a backlog:** if the host sends direction faster than
  the panels redraw, stale positions are skipped rather than queued.
- **Framebuffer + one SPI write per eye** — [D-002](../../docs/decisions/D-002-eyes-framebuffer-rendering.md):
  no flicker, and a roughly fixed ~23ms per eye at 40MHz.
- **`mirror` only affects decorations, never look direction.** The right
  eye is mirrored so brows point inward on both eyes. Mirroring look
  direction would make the eyes go cross-eyed — the bug the bring-up test
  was designed to catch.
- **Behaviour lives in `REGISTRY`, next to the art**, so an expression's
  look and how it moves can't drift apart.
- **The brain doesn't call this directly in the end:** it sends a mood, and
  the router decides what the eyes show ([D-008](../../docs/decisions/D-008-brain-sends-mood-router-composes-face.md)).

## Interfaces

**Wire format** (host → Pico, one line per update, every field optional):

| line               | meaning                                                          |
|--------------------|------------------------------------------------------------------|
| `D-40,25`          | look direction, dx,dy in [-100, 100] (+x screen-right, +y down, as seen facing the robot) |
| `Ehappy:3`         | expression + intensity 1–3                                       |
| `Ehappy`           | expression at its default intensity (2)                          |
| `B`                | blink                                                            |
| `Ehappy:3 D-40,25` | both at once — one redraw, not two                               |

Malformed fields are skipped, and lines over 64 characters are dropped.
Nothing comes back from the Pico.

**Host driver** (`driver.py`):

```python
from nervous_system.serial_transport import SerialTransport
from organs.eyes.driver import EyesOrgan

eyes = EyesOrgan(SerialTransport("/dev/ttyACM0"))
eyes.connect()
eyes.look((-0.4, 0.25))                  # direction only (or "left", "up_right", …)
eyes.set_expression("scared", 3)         # expression only
eyes.show_mood(mood, direction="left")   # a brain.limbic Mood + direction, one line
eyes.update(expression="sad", direction=(0, 0.5), blink=True)
```

`send_command(cmd, payload)` maps the bus commands `blink`, `look`,
`set_expression` and `update` onto the same calls.

**Expression names:** see [`EXPRESSIONS.md`](EXPRESSIONS.md).

## Running and testing

**Without hardware:**

```bash
python organs/eyes/simulate.py
```

A window with both eyes, a button per expression, intensity 1–3, look
arrows, Blink, and a **Command** box that takes wire-format lines (parsed
by the same code as the Pico). Untick "Idle movement" to freeze a frame.

**Tests:** `tests/organs/test_eye_protocol.py` (wire format),
`test_eyes_firmware.py` (every mood has art, each intensity differs, `Face`
redraws once per update, blinks don't block), `test_eyes_driver.py`.

**After editing `REGISTRY`:** `python organs/eyes/expression_status.py` to
regenerate `EXPRESSIONS.md`.

**Flashing the Pico:**

1. Install MicroPython: hold BOOTSEL, plug in over USB, and drag the
   Pico 2 `.uf2` (from [micropython.org/download/RPI_PICO2](https://micropython.org/download/RPI_PICO2/),
   or the one in this folder) onto the drive that appears.
2. Copy every `.py` in `firmware/` except `__init__.py`, keeping the
   filenames (they import each other) — via [Thonny](https://thonny.org)
   (File → Save As → Raspberry Pi Pico), or:

   ```bash
   pip install mpremote
   cd organs/eyes/firmware
   for f in gc9a01 eye_geometry eye_protocol expressions eyes framebuffer backlight panels bringup main; do
     mpremote connect auto fs cp $f.py :$f.py
   done
   cd -
   mpremote connect auto reset
   ```
3. On power-up `main.py` runs: the eyes open and idle until commands arrive.

- **Quick iteration:** `mpremote mount organs/eyes/firmware` runs code
  straight from your laptop without copying. Do a real `fs cp` once you're
  happy, so it survives a power cycle.
- **Typing commands by hand:** use a plain serial terminal
  (`picocom /dev/ttyACM0`). `mpremote` sends Ctrl-C when it connects and
  stops `main.py`.
- **Wiring test:** `mpremote run organs/eyes/firmware/bringup.py` (with the
  other files copied over). Both eyes look around together, and every 5th
  cycle one or both blink on their own — if the *wrong* eye blinks, the CS
  wires are crossed. It replaces `main.py` until the next reset.
- **Garbled picture:** drop `baudrate` in `panels.py` to `20_000_000` or
  `10_000_000`.

## Status and known gaps

- **The new firmware hasn't run on the Pico yet** — only the old
  bring-up test has ([R-201](../../docs/roadmap/items/R-201-eyes-firmware-on-the-real-pico.md)).
- Calm, curious, excited and scared are **placeholder art** until Henry
  draws them ([R-204](../../docs/roadmap/items/R-204-henry-draws-the-placeholder-moods.md)).
- Serious, singing and zombie are **disabled** with TODOs in `REGISTRY`
  ([R-205](../../docs/roadmap/items/R-205-rework-the-disabled-expressions.md)).
- No "thinking" look or per-expression backlight dimming yet
  ([R-206](../../docs/roadmap/items/R-206-thinking-look-and-backlight-dimming.md)).
- Nothing calls the driver yet — waiting on the router
  ([R-207](../../docs/roadmap/items/R-207-router-process.md)) and the brain hookup
  ([R-208](../../docs/roadmap/items/R-208-brain-sends-its-mood-to-the-router.md)).
- The `.jpg` here is Henry's original expressions drawing, which the art is based on.
