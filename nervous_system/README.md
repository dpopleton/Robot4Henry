# Nervous system

## Purpose

Carries messages between the brain and the organs, so the brain never
talks to hardware directly. It thinks in organ names and commands
("eyes": `set_expression`), and whatever is registered under that name —
the real driver or a mock — handles it.

## How it works

- **`bus.py`** — `NervousSystem`: `register(name, driver)` and
  `send(organ, cmd, **payload)`. A phone book from organ name to driver.
  Sending to an unregistered organ raises `KeyError`.
- **`serial_transport.py`** — `SerialTransport(port)`: opens a USB serial
  port (pyserial, `pip install -e ".[hardware]"`). `send(Message)` writes
  a JSON line, `write(bytes)` writes pre-encoded bytes (used by organs with
  their own compact format, like the eyes), and `receive()` reads a line.
- **`protocol.py`** — `Message(organ, cmd, payload)`: a generic
  newline-delimited JSON format, for organs with no reason to need
  something tighter.
- **Organ drivers** live in `organs/<name>/driver.py` and implement
  `organs.base.Organ` (`connect`, `send_command`, `close`).
  `organs.base.MockOrgan` records commands for tests and dev runs with no
  hardware.

```
brain ──send("eyes", "set_expression", …)──▶ NervousSystem ──▶ EyesOrgan ──▶ SerialTransport ──▶ Pico
                                                         └──▶ MockOrgan (no hardware)
```

## Why it's built this way

- **The brain stays hardware-free.** It can run and be tested with nothing
  plugged in. Which driver is used is decided at startup and injected into
  the brain (R-208).
- **Each organ picks its own wire format.** JSON (`protocol.py`) is the
  default, but the eyes use compact ASCII lines for speed
  ([D-001](../docs/decisions/D-001-eyes-ascii-line-protocol.md)) — hence
  `SerialTransport.write()`.
- **One Pico per organ, each on its own port**
  ([D-009](../docs/decisions/D-009-one-pico-per-organ.md)).

## Where this is heading

The **router** ([R-207](../docs/roadmap/items/R-207-router-process.md),
[D-003](../docs/decisions/D-003-brain-computer-is-the-hub.md)) — an
always-running process on the brain computer, separate from `chat()`, that:

- reads inputs (crown direction) and drives outputs (eyes, mouth, lights);
- turns the brain's mood into what each face part shows
  ([D-008](../docs/decisions/D-008-brain-sends-mood-router-composes-face.md));
- smooths direction, holds then returns to centre, and mutes while Qbot speaks;
- re-sends state when a Pico reconnects, and survives one being unplugged.

## Interfaces

```python
from nervous_system import NervousSystem
from organs.base import MockOrgan

ns = NervousSystem()
ns.register("eyes", MockOrgan("eyes"))
ns.send("eyes", "set_expression", expression="happy", intensity=2)
ns.has_organ("mouth")   # False
```

## Running and testing

- `tests/nervous_system/test_bus.py`.
- Serial ports: Linux needs your user in the `dialout` group. Prefer
  `/dev/serial/by-id/…` paths over `/dev/ttyACM0`, which renumbers as
  Picos are added. Only one program can hold a port at a time — close
  Thonny, `mpremote` or the simulator first.

## Status and known gaps

- Nothing creates a `NervousSystem` yet — `main.py` and `RobotBrain` don't
  use it (R-208).
- No router yet (R-207).
- `SerialTransport` has no reconnect logic.
