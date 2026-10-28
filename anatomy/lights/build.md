# Lights — build notes

The physical side of the lights: what it's made of, how it's wired and assembled, and what went wrong. For Henry-facing slideshow text see `manifest.yaml`; for the code see the `organ` in `part.yaml`.

## What it is
Multi-colour LEDs: the **Q** on the forehead, a **glow inside the head** that
shows through the clear back panel, and the **antenna tip**. They have their
own Pico (D-009), fed by the router.

The Q and the glow are the two U-shaped WS2812-type boards (9 LEDs each,
~35 × 60 mm) from the salvaged soundbar (D-018). They're chained DOUT → DIN on
one 3-wire connector (5V, GND, data): LEDs 0–8 are the Q and 9–17 the glow.
They're powered from the Pico's VBUS, so the firmware caps their total
brightness at ~300 mA. Run them dim, and add a level shifter if they flicker.

The head also has a **recording** and a **video** indicator LED. Those are
deliberately *not* here: they're driven by the crown and the camera
respectively, so they can't show the wrong thing (D-007).

## Status
- [x] Pick LEDs: the soundbar's two U boards for the Q and glow (D-018); plain RGB LED for the antenna
- [ ] Glow mock-up (cardboard/printed) and Henry's approval
- [ ] Colour meanings — Henry to decide
- [ ] Diffusers in the shell

## Parts list
| Part | Qty | Cost | Notes |
|---|---|---|---|
| WS2812-type U boards (9 LEDs, ~35 × 60 mm) | 2 | £0 | salvaged from the soundbar: Q and head glow (D-018) |
| WS2812B LEDs | 20-pack | ~£6 | bought before the soundbar; now spares |
| 3-pin LED connectors | — | — | already in hand |
| 5 mm common-cathode RGB LEDs | 10-pack | ~£3 | 1 for the antenna tip, on three PWM pins |
| Small NPN transistors (2N2222/BC547) | a few | ~£2 | only if the antenna's blue/green are too dim at 3.3V |
| Raspberry Pi Pico 2 | 1 | ~£5 | own Pico (D-009) |
| 74AHCT125 level shifter | 1 | ~£1 | only if the LEDs don't read 3.3V data |
