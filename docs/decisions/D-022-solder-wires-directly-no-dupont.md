---
id: D-022
title: Inside an organ, wires are soldered straight to the boards; organs join the hub by USB; no Dupont anywhere
status: accepted
date: 2026-11-04
area: anatomy
---
## Context
Wiring the eyes, Dan found Dupont connectors finicky to crimp, and even
good crimps didn't feel like a good connection. On a robot that moves,
a loose jumper means a blank screen or a flaky Pico. The one link that
has to come apart, head to body, already goes through the head's USB hub
(D-013).

## Decision
- **Inside an organ**, wires are soldered straight to the boards: into
  the Pico's holes, with no header pins on the Pico. If a board already
  has pins soldered on (like the displays), solder the wires to those
  pins and leave them in place.
- **Every joint gets heatshrink**, and each bundle is held by hot glue or
  a cable tie near the board, so flexing doesn't land on the joint.
- **Between organs and the hub**, the link is USB, which is a robust
  connector already. Head to body is the hub's one USB lead and one power
  lead (D-013).
- **No Dupont connectors anywhere.** If something inside a part ever
  needs to unplug, use pre-crimped JST-XH or JST-PH leads, or round
  machine-pin sockets, not Dupont.
- Test new firmware on the breadboard before soldering, so soldered
  joints and software are never debugged at the same time.

## Alternatives considered
- **Dupont jumpers and header pins.** Easy to change, but finicky to
  crimp, a weak connection, and they work loose on a moving robot.
- **Header pins on the Pico and sockets on a carrier board.** Lets a
  Pico be swapped in seconds, but adds a connector that can work loose,
  and Picos are cheap enough to swap the slow way.
- **JST connectors on every wire.** A good connection, but more to buy
  and crimp, and nothing inside an organ needs to unplug often.

## Consequences
- Swapping a Pico means desoldering only the few wires it uses (8 on the
  eyes), not a 40-pin header. Each wire takes a minute with wick or a
  sucker.
- Changing a pin after soldering is a desolder job, which is why the
  breadboard test comes first.
- R-213's "hard-wire the Picos' USB into the hub" fits this: soldering
  where nothing needs to unplug. A USB plug at the Pico is still fine if
  hard-wiring turns out awkward, since USB is a good connector.
