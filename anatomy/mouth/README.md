# Mouth — physical mount

`organs/mouth/` doesn't exist yet in software (see the main README's
roadmap, Phase 2), and the mechanism itself hasn't been decided. This
folder exists so the decision has somewhere to land, not because
anything here is settled.

## Status

Placeholder, and a bigger placeholder than `anatomy/eyes/` — the
*mechanism* is undecided, not just the numbers. `measurements.yaml`
currently assumes a single servo-driven hinged jaw (the most
physically demanding option, so it leaves the most room), but that's
a guess, not a decision.

## What it builds

A flat plate with the visible mouth opening cut through, a reserved
footprint-sized pocket for wherever the mechanism's body goes, and
four corner mounting holes.

Run `python anatomy/mouth/drawing.py` for a dimensioned front/side PDF
you can print on paper — that's the main output. `generate.py` builds
the same plate as an actual 3D solid (`.step`/`.stl`) if you ever want
that instead. See `anatomy/README.md` for the general workflow.

## Before doing anything real here

1. **Pick the mechanism.** Candidates worth weighing:
   - Single servo-driven hinged jaw (assumed in `measurements.yaml`
     now) — one moving part, mouth opens/closes but no other shape.
   - Small LED matrix or strip behind a diffuser — no moving parts,
     more expressive shapes, more `organs/mouth` firmware work.
   - Static printed shape, lit or unlit — simplest to build, no
     runtime expressiveness at all.
2. Update `mechanism.type` in `measurements.yaml` (and the rest of
   that section) once picked — the current SG90 servo numbers are
   placeholders, not a spec.
3. Only then are `plate_width_mm` / `opening_width_mm` / etc. worth
   treating as real rather than guessed.

## Open questions

- Does the mouth even need its own plate, or does it mount directly
  into the head shell like the eyes might end up doing?
- If it's servo-driven: where does the servo's wiring run, and does
  `nervous_system`/`organs/mouth` need a new command (`open_mouth`,
  `set_mouth_shape`, ...) to match whatever `organs/eyes` ends up
  doing for `set_expression`?
