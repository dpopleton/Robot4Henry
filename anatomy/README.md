# Anatomy

Physical build docs: measurements, mounting/construction notes, and
printable CAD for Qbot's body. This is the physical counterpart to
`organs/` — `organs/eyes/` has the electronics and firmware for the
eye displays, `anatomy/eyes/` has how they're physically mounted.

## Layout

One folder per organ, plus assembly folders for anything that only
makes sense once organs are combined:

```
anatomy/
├── _lib.py          # shared load/export helpers used by every generate.py
├── _drawing.py       # shared dimension-line/label helpers used by every drawing.py
├── eyes/             # mirrors organs/eyes/ — the eye displays' physical mount
│   ├── README.md       # construction notes, in prose
│   ├── measurements.yaml   # every dimension, as data
│   ├── eyes_layout.py  # measurements.yaml -> derived numbers (shared by both scripts below)
│   ├── generate.py     # -> exports/*.step, *.stl (a 3D solid, for CAD/printing if you ever want it)
│   ├── drawing.py      # -> exports/*_drawing.pdf (a dimensioned page, ready to print on paper)
│   └── exports/         # generated, gitignored — regenerate, don't hand-edit
├── mouth/            # mirrors organs/mouth/ (not built yet — see main README roadmap)
└── head/             # assembly: the shell eyes + mouth mount into
```

`head/` is an *assembly* folder — it doesn't restate eyes/mouth
numbers, it loads their `measurements.yaml` directly (see
`head/generate.py`) so the head shell's cutout windows always match
the actual plate sizes. If a future part only makes sense as part of
an assembly (e.g. an ear that's molded into the head shell rather than
bolted on), it lives under the relevant assembly folder rather than
getting its own top-level one.

## The measurements.yaml -> output workflow

Each part folder has:

- **`measurements.yaml`** — the source of truth. Every dimension,
  with a comment where it's a placeholder that still needs measuring
  against a real part. Edit this, not the generated files.
- **`<part>_layout.py`** — pure arithmetic, no drawing library
  involved: turns the raw measurements into derived numbers (plate
  size from hole spacing + margins, corner-hole positions, etc). Both
  scripts below import this, so the 3D model and the 2D drawing can
  never disagree about a number.
- **`drawing.py`** — the main output for this project: a dimensioned
  2D orthographic drawing (front/side/top views, with measurement
  labels and arrows, like a hand-drafted engineering print) rendered
  with [matplotlib](https://matplotlib.org/), saved as a print-ready
  PDF. This is what to open and print on paper.
- **`generate.py`** — a [cadquery](https://cadquery.readthedocs.io/)
  script (Python-as-CAD) that builds an actual 3D solid and exports
  `.step`/`.stl`. Kept alongside the drawing in case a 3D model is
  ever useful (opening in FreeCAD to check a fit, 3D printing later),
  but it's not the primary output — `drawing.py` is.
- **`exports/`** — everything generated above. Gitignored —
  regenerating is instant, so there's no reason to track derived
  files in git. Run the relevant script before you need a fresh copy.

This means you don't need to know how to use a CAD program to change a
dimension — open `measurements.yaml`, change a number, re-run
`drawing.py` for an updated printable page (or `generate.py` for an
updated 3D model). You only touch the scripts themselves when the
actual shape changes, not just its size.

### Setup

```bash
pip install -e ".[anatomy]"
```

### Generating a part's drawing (the main workflow)

```bash
python anatomy/eyes/drawing.py
python anatomy/mouth/drawing.py
python anatomy/head/drawing.py   # reads eyes/ and mouth/ measurements too
```

Each prints the PDF path it wrote under that folder's `exports/` —
open and print that.

### Generating a part's 3D model (optional)

```bash
python anatomy/eyes/generate.py
python anatomy/mouth/generate.py
python anatomy/head/generate.py
```

## Current status

Everything here right now is a **placeholder** — folder structure and
a working pipeline, not a finished design. Every `measurements.yaml`
is full of `TODO` comments marking numbers that need to come from a
real part in hand (calipers, not guesses) or a real design decision
(e.g. `mouth/measurements.yaml`'s mechanism isn't chosen yet). The
shapes `generate.py` produces are deliberately simple — a flat plate
with holes, a plain box shell — so the pipeline works end to end; swap
in a real shape once the numbers are real.
