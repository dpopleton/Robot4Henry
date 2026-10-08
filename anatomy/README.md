# anatomy/

The **physical** robot, one folder per part: what it's made of, how it's
wired and assembled, photos and CAD — plus kid-level explanations for Henry.
(Code that drives a part lives in `organs/`; plans live in `docs/`.)

Long term, the brain will use this folder to answer "how does your eye
work?" (R-905, R-312): look the part up by alias in `part.yaml`, flash
through the build photos/CAD on its screens, settle on a rotating 3D
model, and narrate. None of that playback is built yet — this is the
content store it will read from, so keep it current as the build goes.

## Layout

```
anatomy/
├── <part>/
│   ├── part.yaml       # structured facts: aliases, status, which organ drives it, summary for Henry
│   ├── build.md        # build notes: what it is, status checklist, wiring, design rules, parts list
│   ├── manifest.yaml   # Henry-facing slideshow: images in order, each with a description
│   ├── images/         # build photos, exported CAD diagrams
│   └── models/         # 3D models once they exist (.step/.stl/.glb)
```

Parts so far: `head/` (the shell), `eyes/`, `mouth/`, `crown/` (mic
array), `lights/` (Q + antenna). Add a folder when a new part starts
being designed — copy an existing one's `part.yaml` and `build.md` shape.

## Who writes what

- `build.md` — engineering notes, for Dan and agents. Keep the status
  checklist in step with the roadmap item it links to.
- `part.yaml`'s `summary_for_henry` and `manifest.yaml` descriptions — text
  Henry will eventually *hear*, so write it for a 7-year-old, not a
  datasheet. Agents draft it; Dan checks it and sets
  `henry_text_approved: true`.

## Adding material

1. Drop the photo or exported CAD diagram into `<part>/images/`.
2. Add an entry to `<part>/manifest.yaml` pointing at it, with a short title
   and a plain-English description (schema in the comment at the top of each
   manifest). Entries are read in order — that's the slideshow order.
3. Mention it in that week's journal entry (`docs/journal/`).
4. Once a finished 3D model exists, drop it in `<part>/models/` and reference
   it from the manifest with `model:`.

Nothing here is final — reorder, rewrite or delete freely as the build
changes. This is a living reference, not a spec.
