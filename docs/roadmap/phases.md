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
of done, not a separate phase. Likewise every organ also works in the
virtual robot (D-012, R-209), so it can be tested without the hardware.

The headings below are read by `docs/build_index.py` — keep the
`## Phase <n> · <name>` / `## Ongoing` format.

## Phase 1 · Brain

Conversation, memory and mood on the brain computer (an old laptop for now:
~8 years old, 8GB RAM, no GPU — it sits beside the head until the body
exists).

**Done when:** on the robot laptop, with the model picked in the shoot-out
(R-104), Qbot passes the conversation and memory tests defined in R-116 as
reliably as R-116 says; its prompt is built from the written personality
(R-106); and a typed reply meets the text-reply time target (R-105). The
best model this laptop can run counts: if it's not good enough, development
carries on here while an upgrade is planned and saved for (R-902).
**Safety needs for this phase:** what goes back into memory is checked
before it's stored (R-109), and the conversation logs are readable for the
weekly review (R-901) before Henry's first chat with the robot itself.
Henry doesn't type to Qbot (it's too much like school), so his first real
conversations come with voice in Phase 3, and judging them by ear is part of
Phase 3's done.

## Phase 2 · Face

Everything that *shows* something: eyes, mouth, glowing Q, antenna light —
plus the router that turns the brain's mood into what each part shows
(D-008), and the head shell they mount in.

**Done when:** every face part is mounted in the head and reacts to a
conversation.

## Phase 3 · Hearing and voice

The crown's four-mic array (built from scratch — D-004), speech-to-text,
direction-finding so the eyes look at whoever's talking, the speakers and
Qbot's voice, and waking/sleeping (D-016). Teaching mode sits here too,
since it needs voice and screens. Speech-to-text and Qbot's voice are built
first in the virtual robot, using the machine's own mic and speakers, so
they don't wait for the crown or the speakers. The speakers come from a
salvaged soundbar and are driven by a Waveshare USB sound card whose volume
the laptop sets (D-027). Doing things unprompted (R-107) comes last in the
phase. **Safety needs for this phase:** a software volume clamp in the
brain. There's no hardware ceiling; a resistor per speaker is the fix if
over-loud audio ever actually comes up (D-027, R-306). There's no Bluetooth
in the head (R-314).

**Done when:** you press the wake button, talk to Qbot through the crown,
its eyes look at you, and it answers through its own speakers, and Henry's
first spoken chats feel like a good conversation to Dan. How fast is fast
enough for a spoken reply (R-315), and whether you can talk over it (R-309),
get decided by trying it.

## Phase 4 · Head finish

A final tidy-up pass that makes the head one finished unit, in its thin
aluminium skin with the crown on top. The neck has moved to the body (Phase 5):
it's built alongside the body's frame and sits directly on it.

**Done when:** every head panel is designed and printed (bar the bottom panel,
which is designed with the neck), the aluminium skin is on, the wiring
behind the clear panel is tidy, the back door has its hinge pin, the camera
and its video LED are fitted (R-601), and only one USB lead and one power
lead leave the head (R-402).

## Phase 5 · Body

A self-designed, 3D-printed tracked body holding everything not in the
head, including the laptop. Indoors on all sorts of floors, maybe pavement
outside — no stairs. The **neck** is the body's second step, built with its
frame: the head (~2–2.5 kg) sits on it and can turn and tilt (R-401).

**Done when:** Qbot drives itself safely indoors at walking pace or slower
(on voice commands or wandering, D-020; a gamepad is only for testing), and
the head turns towards voices beyond the eyes' range. **Motion safety is part of done:** speed limits,
bump sensors, drop sensors (so it can't drive off a step), an easy-to-reach
stop button (R-503), and firm stops and motion limits on the neck.

## Phase 6 · Vision

What Qbot does with his camera. The camera itself goes into the head in
Phase 4 (R-601): a 2.5 × 10 cm insert above the Q, a video LED on the
camera's own 5V, and no power to the camera while it's not in use or asleep
(D-007, D-025). The first task is recognising who he's talking to (R-311)
or recognising objects, chosen when we get there. Following faces is
dropped. It's tried on the current robot laptop before any upgrade (R-902).
Photos may be stored, since the robot is air-gapped, but only what a feature
needs. Vision will feed the body's movement (D-020), so Phases 5 and 6 may
run in parallel; their order is decided at the time.

**Done when:** Qbot uses what the camera sees in a conversation (the first
task, R-602), on the robot laptop, with the video LED lit exactly while the
camera is powered. The exact task is still to be defined.

## Phase 7 · Hands

Arms with C-shaped grabbers, designed by Henry, so Qbot can pick things
up **for himself**: toys, Lego, a cup or a ball, from the floor or a table
(R-701), with two arms. It needs
vision (Phase 6) to find things, and maybe a low body camera (R-603). The
body is planned with arms in mind (mounting, power, balance) but they're
fitted later. Motors are sized from Henry's design, probably sturdier than
hobby servos. **Safety needs for this phase:** the body's stop button
stops the arms (R-503), and grip force is limited (how is decided at the
time).

**Done when:** Qbot picks up a named toy from the floor in front of him on
a voice command, by himself, with his two arms, and holds it up.

## Ongoing

Things that run alongside every phase.

- **Safety policy.** Henry uses Qbot **supervised** for now, and the logs are
  reviewed regularly (part of the weekly review — R-901). Safety isn't its
  own phase: each phase meets its own safety needs before it counts as done
  (e.g. motion safety in Phase 5, asleep = mics and cameras off in D-016).
- **Brain computer upgrade** — undated. The model shoot-out (R-104) shows
  when it's needed.
- **Solar charging** — Henry's Wall-E idea, late stage and for show. The
  body is designed with room for it (R-501, R-502).
- **Docs and anatomy** — keeping area READMEs current, and eventually
  letting the brain look up how it was built.
- **Backups** — a copy of Qbot's memories off the robot laptop (R-906),
  late; fine without one while there's little in them.

## Henry

Henry has no tasks on the roadmap: Dan guides him through everything and
adapts the work to him. His ideas and contributions (drawings, names,
choosing Qbot's voice, colour meanings…) are recorded in the journal.
Henry-facing text (anatomy descriptions, personality) is drafted by agents
and approved by Dan.
