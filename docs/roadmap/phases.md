# Phases

What each phase means and what "done" looks like. Individual pieces of work
live in `items/`; the generated overview is `README.md`.

The order follows how the robot is actually being built: **finish the head
together with the brain first**, then the tracked body and movement, then
picking things up. There's no deadline — the journey is the point. Hours
swing between 5 and 40 a week, and hardware spend is about £40–50 a month,
so each item carries a rough `cost_gbp`.

Every head part is **mounted in the head as its code is developed**, so
"mounted and working in the head" is part of every head item's definition
of done, not a separate phase.

The headings below are read by `docs/build_index.py` — keep the
`## Phase <n> · <name>` / `## Ongoing` format.

## Phase 1 · Brain

Conversation, memory and mood on the brain computer (an old laptop for now:
~8 years old, 8GB RAM, no GPU — it sits beside the head until the body
exists).

**Done when:** Qbot holds a good conversation on the robot laptop, remembers
key facts reliably, has a written personality, and replies fast enough
(target set in R-105).

## Phase 2 · Face

Everything that *shows* something: eyes, mouth, glowing Q, antenna light —
plus the router that turns the brain's mood into what each part shows
(D-008), and the head shell they mount in.

**Done when:** every face part is mounted in the head and reacts to a
conversation.

## Phase 3 · Hearing and voice

The crown's four-mic array (built from scratch — D-004), speech-to-text,
direction-finding so the eyes look at whoever's talking, the speaker and
Qbot's voice, and waking/sleeping (D-010). Teaching mode sits here too,
since it needs voice and screens.

**Done when:** you press the wake button, talk to Qbot through the crown,
its eyes look at you, and it answers through its own speaker.

## Phase 4 · Neck and head finish

The head looks around on a neck (tilt still undecided), and gets a final
tidy-up pass into one finished unit.

**Done when:** the head is finished and turns towards voices out of the
eyes' range.

## Phase 5 · Body

A self-designed, 3D-printed tracked body holding everything not in the
head, including the laptop. Indoors on all sorts of floors, maybe pavement
outside — no stairs.

**Done when:** it drives safely indoors. **Motion safety is part of done:**
speed limits, bump sensors, drop sensors (so it can't drive off a step),
and an easy-to-reach stop button (R-503).

## Phase 6 · Vision

A camera at the top of the front face, above the Q (space is reserved in the
front frame now), with a video LED wired to the camera hardware (D-007).
What vision does first is still open.

**Done when:** to be defined (R-602).

## Phase 7 · Hands

A couple of arms with C-shaped grabbers. Just an idea for now.

**Done when:** to be defined.

## Ongoing

Things that run alongside every phase.

- **Safety policy.** Henry uses Qbot **supervised** for now, and the logs are
  reviewed regularly (part of the weekly review — R-901). Safety isn't its
  own phase: each phase meets its own safety needs before it counts as done
  (e.g. motion safety in Phase 5, asleep = mics and cameras off in D-010).
- **Brain computer upgrade** — undated. The model shoot-out (R-104) shows
  when it's needed.
- **Solar charging** — Henry's Wall-E idea, late stage and for show.
- **Docs and anatomy** — keeping area READMEs current, and eventually
  letting the brain look up how it was built.

## Henry

Henry has no tasks on the roadmap: Dan guides him through everything and
adapts the work to him. His ideas and contributions (drawings, names,
choosing Qbot's voice, colour meanings…) are recorded in the journal.
Henry-facing text (anatomy descriptions, personality) is drafted by agents
and approved by Dan.
