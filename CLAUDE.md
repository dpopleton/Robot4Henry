# Robot4Henry (Qbot)

A locally-run companion robot built by Dan with his son Henry (7); Henry's
sister (3) will use it too. It's a learning project with no deadline — the
journey is the point. Hardware spend is about £40–50 a month. Everything
runs locally on the robot's own computer; no cloud.

## Where things live

| What | Where |
|---|---|
| Big picture, data flow | `docs/architecture.md` |
| Roadmap overview (generated) | `docs/roadmap/README.md` |
| Phases, definition of done, safety policy | `docs/roadmap/phases.md` |
| One file per piece of work | `docs/roadmap/items/R-*.md` |
| Why things are the way they are | `docs/decisions/D-*.md` |
| Weekly journal | `docs/journal/YYYY-Www.md` |
| Physical robot: build notes, wiring, photos, CAD | `anatomy/<part>/` (`part.yaml`, `build.md`, `manifest.yaml`) |
| How a code area works | `README.md` beside the code (`organs/eyes/`, `brain/limbic/`, `nervous_system/`, …) |

Code is organised like a body: `brain/` (cognition, memory, mood),
`nervous_system/` (messaging), `organs/` (code per physical subsystem,
including Pico firmware), `anatomy/` (the physical build — no code).

## Rules for keeping docs current

When you finish a piece of work:

1. **Roadmap item:** update its `status`, tick its tasks, bump `updated`,
   and add a dated line to its Log. Add an item if the work wasn't on the
   roadmap. If you find new work, add it as an `idea` or `planned` item
   rather than leaving it only in chat.
2. **Decisions:** a non-obvious choice (one with real alternatives) gets a
   new `docs/decisions/D-*.md`. Never rewrite an old decision — supersede it.
3. **Area README:** update its "Status and known gaps" section, and any
   section the change affects. New code areas get a README with the same
   headings: Purpose / How it works / Why it's built this way /
   Interfaces / Running and testing / Status and known gaps.
4. **Physical work** (prints, wiring, purchases) goes in that part's
   `anatomy/<part>/build.md` and in the week's journal entry.
5. **Regenerate:** `python docs/build_index.py` after touching roadmap
   items, decisions or journal entries; `python organs/eyes/expression_status.py`
   after touching the eyes' `REGISTRY`. The test suite fails if either is stale.

## Conventions

- **Henry-facing text** (`summary_for_henry`, manifest descriptions,
  personality) is written for a 7-year-old. Agents draft it; Dan approves it
  (`henry_text_approved: true`). Henry has no roadmap tasks — his ideas and
  contributions go in the journal.
- **Safety:** use is supervised for now, and the logs are reviewed weekly.
  Each phase meets its own safety needs before it counts as done.
- **The dev machine is much faster than the robot laptop** (~8-year-old CPU,
  8GB RAM, no GPU). Speed and model tests only count on the robot laptop.
- **Firmware:** Pico code in `organs/<organ>/firmware/` must stay
  MicroPython-compatible. Keep the drawing/protocol logic plain Python so
  the simulator and tests run it unchanged. The crown will be C (D-004).
- **Costs:** give roadmap items a rough `cost_gbp` for what's still to buy.

## Commands

```bash
source .venv/bin/activate
python -m pytest            # fast tests (excludes the real-LLM `llm` scenarios)
python -m pytest -m llm     # scenario tests against Ollama
python main.py              # chat in the terminal
python organs/eyes/simulate.py
python docs/build_index.py  # regenerate docs indexes (--check to verify)
```

## Weekly review

`/weekly-review` (`.claude/skills/weekly-review/SKILL.md`): gathers what
changed, asks Dan about the things git can't see, writes the journal entry,
updates the roadmap, and grills Dan on one phase in depth.
