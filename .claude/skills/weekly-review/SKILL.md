---
name: weekly-review
description: Weekly Robot4Henry review — gather what changed since the last journal entry, ask Dan about physical work and Henry, write this week's journal entry, update roadmap items and decisions, skim the conversation logs, and grill Dan on one phase in depth. Use when Dan runs /weekly-review or asks for the weekly review.
---

# Weekly review

An interactive session with Dan. Steps 2 and 5 need his answers — ask, then
wait. Keep questions short and grouped, and accept "don't know yet" (record
it as an open question on the relevant item).

## 1. Gather (silently, before saying anything)

- The latest `docs/journal/*.md`: its `reviewed` date (the last review)
  and `grill_next` (the phase to grill this time).
- `git log --since=<reviewed>` plus `git status` — what changed in code and docs.
- Roadmap items (`docs/roadmap/items/`):
  - `in-progress` with `updated` more than ~2 weeks old (stuck?);
  - `next` items, and whether their `depends_on` are done;
  - `blocked` items.
- New `TODO`s in code since the last review (`git diff <last-review-commit> | grep TODO`).
- Anatomy: new images not yet in a `manifest.yaml`; `henry_text_approved: false`
  entries waiting for Dan.
- Conversation logs (R-901): sessions since the last review in
  `storage/robot.db` — counts, and anything that looks off (unsafe or odd
  replies, mood stuck, errors). Until R-901 builds a transcript tool, query
  SQLite directly and keep it brief.

## 2. Report, then ask

Start with a short summary: what changed, what looks stuck, anything
odd in the logs. Then ask about what git can't see:

- Physical work: prints, wiring, soldering, assembly, testing — what worked, what broke?
- Purchases this week, and what's next to buy (the budget is £40–50 a month).
- Henry: drawings, ideas, names, choices, what he enjoyed.
- Blockers, and anything to drop or reprioritise.

## 3. Write it up

- **Journal:** create `docs/journal/<ISO year>-W<week>.md`, following the
  front matter and sections of the previous entry (Built — code, Built —
  physical, Henry, Decided, Problems / notes, Spending, Next week). Set
  `reviewed` to today and `grill_next` to the next phase in rotation
  (1 → 2 → … → 7 → ongoing → 1).
- **Roadmap items:** update statuses and task ticks, bump `updated`, and add Log
  lines. Create items for new work. Every phase's definition of done
  in `phases.md` must still be true to reality.
- **Decisions:** draft a `D-*.md` for any real choice made this week. Mark it
  `proposed` if Dan hasn't confirmed it.
- **Anatomy:** physical progress into `anatomy/<part>/build.md`. Draft
  manifest entries for new photos (Henry-facing, `henry_text_approved` stays false).
- Run `python docs/build_index.py`, then `python -m pytest tests/docs`.

## 4. Check the current phase

Briefly check the phase that's in progress (the lowest phase with
unfinished non-idea items): is its "done when" still right? Is anything
missing?

## 5. Grill one phase in depth

Take the `grill_next` phase. Read `phases.md` and every item in it, then
ask Dan 6–10 pointed questions:

- vague "done when"s;
- hidden dependencies or ordering problems;
- cost and budget fit;
- physical design decisions that need settling before something is printed;
- safety;
- ideas that are ready to become planned work, or should be dropped.

Challenge assumptions — don't just collect answers. Fold the answers back
into the items and `phases.md`, then re-run step 3's regeneration.

## 6. Close

End with one short message: what changed in the docs, the top 1–3 things
for next week, and any open questions left for Dan. Don't commit unless
Dan asks.
