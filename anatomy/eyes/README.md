# Eyes — physical mount

How the two GC9A01 round displays are physically held. For wiring,
pinout, and firmware flashing, see `organs/eyes/README.md` — that
file is the electronics half of this part, this one is the mechanical
half.

## Status

Placeholder. `measurements.yaml` has TODO markers on every dimension
that needs measuring off a real display board with calipers — nothing
here has been fitted to a real part yet.

## What it builds

A flat plate with two circular socket pockets (sized to the display's
outer diameter plus a small clearance for a push-fit), a wire channel
out the bottom of each socket, and four corner mounting holes. It's
intentionally simple — proving the `measurements.yaml` → output
pipeline, not a finished eye housing.

Run `python anatomy/eyes/drawing.py` for a dimensioned front/side PDF
you can print on paper — that's the main output. `generate.py` builds
the same plate as an actual 3D solid (`.step`/`.stl`) if you ever want
that instead. See `anatomy/README.md` for the general workflow.

## Before printing anything

1. Measure the actual display board: `outer_diameter_mm`,
   `glass_diameter_mm`, `pcb_thickness_mm`, and which edge the
   connector exits from — fill these into `measurements.yaml`.
2. Decide `eye_spacing_mm` — this should probably come from
   `anatomy/head/measurements.yaml` once the head shape is real,
   rather than being picked independently; for now it's a standalone
   guess.
3. Re-run `python anatomy/eyes/generate.py` and check the exported
   STL fits before printing at full scale/infill.

## Open questions

- Does the plate mount flush against the inside of the head shell, or
  does the shell itself form the socket (no separate plate at all)?
  Right now this assumes a separate plate; revisit once `anatomy/head/`
  has a real shape.
- Should the two eyes be rigid (fixed look direction, only the
  rendered pupil moves — matches the current firmware in
  `organs/eyes/firmware/`) or does the mount need to allow physical
  tilt? Assumed rigid for now.
