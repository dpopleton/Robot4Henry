# Lights — build notes

The physical side of the lights: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
Multi-colour LEDs behind diffusers: the **Q** on the forehead and the
**antenna tip**. Probably their own Pico (D-009), fed by the router.

The head also has a **recording** and a **video** indicator LED. Those are
deliberately *not* here: they're driven by the crown and the camera
respectively, so they can't show the wrong thing (D-007).

## Status
- [ ] Pick LEDs (WS2812-type, one data wire)
- [ ] Colour meanings — Henry to decide
- [ ] Diffusers in the shell

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| WS2812-type LEDs | ~10 | ~£5 | |
| Raspberry Pi Pico 2 | 1 | ~£5 | if it gets its own |
