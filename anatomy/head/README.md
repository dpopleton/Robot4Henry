# Head — assembly

The shell that `anatomy/eyes/` and `anatomy/mouth/` mount into. This
is an *assembly* folder, not a per-organ one — see `anatomy/README.md`
for what that distinction means.

## Status

Placeholder. `measurements.yaml` has TODO markers on the shell's
overall size and on where the eyes/mouth windows sit vertically;
`shell.shape_notes` flags that the shape itself (dome vs. box vs.
something organic) hasn't been decided — `generate.py` currently
builds a plain hollow box.

## What it builds

A hollow box shell, with two windows cut into the front face: one
sized to the eyes plate's footprint, one sized to the mouth plate's
footprint, each positioned at the height given in `measurements.yaml`.
Crucially, the window sizes aren't independent numbers here —
`head_layout.py` loads `anatomy/eyes/measurements.yaml` and
`anatomy/mouth/measurements.yaml` directly so a change to either
part's plate size is reflected automatically the next time you
regenerate. If you resize the eyes plate and the head window doesn't
change, re-run the script — it isn't stale, it just hasn't
regenerated yet.

Run `python anatomy/head/drawing.py` for a dimensioned front/top/side
PDF you can print on paper — that's the main output. `generate.py`
builds the same shell as an actual 3D solid (`.step`/`.stl`) if you
ever want that instead.

## Before printing anything

1. Decide the actual shape (`shell.shape_notes` in
   `measurements.yaml`) — a plain box is not the final head.
2. Get real numbers into `anatomy/eyes/measurements.yaml` and
   `anatomy/mouth/measurements.yaml` first; this folder's windows are
   only as real as those.
3. Decide `print.split_notes` — most home printer beds won't fit a
   160mm-plus head shell in one piece; figure out where it splits
   before committing to a shape that can't be split cleanly.

## Open questions

- One-piece shell with a removable back panel for access to wiring,
  or split front/back halves that screw together?
- Does anything besides eyes + mouth mount to this shell (ears for
  `organs/ears` in Phase 3, a neck/mounting point for Phase 5's
  chassis integration)? Worth leaving room for even before those
  organs exist.
