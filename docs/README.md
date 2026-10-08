# Docs

Where to find things. Code-level detail lives in a README beside the code;
the physical robot lives in `anatomy/`; this folder holds the big picture
and the plans.

| What | Where |
|---|---|
| How the whole system fits together | [architecture.md](architecture.md) |
| What's planned, in progress and done | [roadmap/README.md](roadmap/README.md) (generated) |
| What each phase means, and the safety policy | [roadmap/phases.md](roadmap/phases.md) |
| One file per piece of work | [roadmap/items/](roadmap/items/) |
| Why things are built the way they are | [decisions/README.md](decisions/README.md) |
| What happened each week — code, physical build, Henry's ideas | [journal/README.md](journal/README.md) |
| The physical robot: build notes, wiring, photos, CAD | [../anatomy/](../anatomy/README.md) |

Code areas with their own README:

- [brain/limbic](../brain/limbic/README.md) — mood
- [nervous_system](../nervous_system/README.md) — bus, transports, the future router
- [organs/eyes](../organs/eyes/README.md) — eyes firmware, driver, simulator

(More to come — R-904.)

## Keeping it current

```bash
python docs/build_index.py           # regenerate the roadmap, decisions and journal indexes
python docs/build_index.py --check   # what the test suite checks
```

The indexes are generated from the front matter at the top of each item,
decision and journal file. Don't hand-edit the generated `README.md` files.
The weekly routine is `/weekly-review` (see `.claude/skills/weekly-review/`),
and the rules for agents are in [`CLAUDE.md`](../CLAUDE.md).

### Roadmap item front matter

```yaml
id: R-207                 # R-<phase digit><two digits>; ongoing items are R-9xx
title: "Router process"   # quote it if it has a colon
phase: 2                  # a number from phases.md, or ongoing
status: next              # idea | planned | next | in-progress | blocked | done
area: nervous_system      # code path or physical part
kind: code                # code | physical | both | planning
depends_on: [R-201]
decisions: [D-003]
cost_gbp: 12              # rough estimate of what's still to buy, or null
updated: 2026-10-08
```

Body sections: Goal, Why, Tasks (checkboxes), Done when, Open questions
(optional), Log (dated one-liners, newest last).

### Decision front matter

```yaml
id: D-011
title: "…"
status: accepted          # proposed | accepted | superseded
date: 2026-10-15
area: organs/mouth
superseded_by: D-014      # only if superseded
```

Body sections: Context, Decision, Alternatives considered, Consequences.
Never rewrite an old decision — write a new one and mark the old one
superseded.

### Journal front matter

```yaml
week: 2026-W42
summary: "One line for the index."
reviewed: 2026-10-15
grill_next: 4             # phase to grill in depth next week
```
