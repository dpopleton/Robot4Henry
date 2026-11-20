# Organs

## Purpose

The code for each physical part of Qbot that the brain computer talks to:
the firmware that runs on the part's own Pico, the host driver that sends
it commands, and its virtual version for the virtual robot. One folder
per organ. The physical build (wiring, prints, photos) is in
`anatomy/<part>/`, not here.

| Organ | Folder | Status |
|---|---|---|
| Eyes (two round GC9A01 screens) | [`eyes/`](eyes/README.md) | in the head, working; in the virtual robot |
| Mouth (2" ST7789 screen) | [`mouth/`](mouth/README.md) | in the head, working; in the virtual robot |
| Shared Pico code | [`pico_common/`](pico_common/README.md) | used by eyes and mouth |
| Lights, crown, … | not started | R-211, R-301–R-303 |

## How it works

Every organ is built the same way:

```
organs/<organ>/
  firmware/      runs on the organ's own Pico (MicroPython; the crown will be C, D-004)
    main.py        reads command lines over USB serial, draws/acts
    *_protocol.py  the wire format (eye_protocol.py, mouth_protocol.py), also used by the host to build lines
    …              drawing/logic in plain Python, so the desktop runs it unchanged
  driver.py      host side: <Organ>Organ(transport).update(...) → one line to the Pico
  virtual.py     a panel (the firmware's code on a Tk canvas) + bench controls
  README.md
```

- **One Pico per organ**
  ([D-009](../docs/decisions/D-009-one-pico-per-organ.md)), each on its own
  USB serial port, all through the head's hub (R-213).
- **Wire format:** short ASCII lines, one per update, every field optional
  (e.g. eyes `Ehappy:3 D-40,25`, mouth `S1 L80`). The Pico never answers;
  any output from it means it crashed
  (`nervous_system/pico_console.py`).
- **`base.py`** — `Organ`, the interface every driver implements
  (`connect()`, `send_command(cmd, payload)`, `close()`), and `MockOrgan`,
  which records commands for tests and for parts not built yet.
- **`deploy.py`** — copies an organ's firmware plus `pico_common/` to its
  Pico (flat, as they import each other by name) and restarts it.
- **`pico_common/`** — shared Pico code: the framebuffer and the serial
  line reader.

## Why it's built this way

- **The firmware's logic is plain Python**, so the same code runs on the
  Pico, in the virtual robot and in the tests. Only the screen drivers and
  pin setup are Pico-only.
- **The protocol file is shared** by the firmware and the host driver, so
  the two can't drift apart.
- **Every organ has a virtual version**
  ([D-012](../docs/decisions/D-012-every-organ-ships-a-virtual-version.md),
  [D-023](../docs/decisions/D-023-one-virtual-robot-app-with-per-organ-bench-mode.md)),
  so it can be built and tried without the hardware.
- **Newest wins:** a Pico drains every waiting line before drawing, so a
  fast stream of commands never builds up a backlog.

## Interfaces

```python
from nervous_system.serial_transport import SerialTransport
from organs.eyes.driver import EyesOrgan
from organs.mouth.driver import MouthOrgan

eyes = EyesOrgan(SerialTransport("/dev/serial/by-id/…"))
eyes.connect()
eyes.update(expression="happy", intensity=3, direction=(-0.4, 0.25))

mouth = MouthOrgan(SerialTransport("/dev/serial/by-id/…"))
mouth.connect()
mouth.update(talking=True, level=0.8)
```

Each organ's README has its full wire format and driver calls.

**Adding an organ:** a folder with `firmware/` (its module names must not
clash with another organ's; a test checks), `driver.py`, `virtual.py`
(see `virtual_robot/README.md`), a README with the usual headings, and an
`anatomy/<part>/` folder for the build.

## Running and testing

```bash
python -m virtual_robot                    # every organ, virtual or on its real Pico
python organs/deploy.py eyes --dry-run     # list what would be copied to the Pico
python organs/deploy.py mouth              # copy and restart (needs mpremote)
python -m pytest tests/organs              # protocols, drawing, drivers, panels, MicroPython compatibility
```

## Status and known gaps

- Eyes and mouth are in the head and working.
- Nothing drives the organs from the brain yet: that's the router (R-207,
  R-208).
- The laptop can't yet tell which Pico is which organ (R-215, after the
  hub).
- The mouth's volume knob emulation for the sound board is still to do
  (R-306).
