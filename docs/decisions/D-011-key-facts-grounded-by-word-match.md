---
id: D-011
title: Key facts are checked against the user's own words, not by asking the model
status: accepted
date: 2026-10-12
area: brain/memory
---
## Context
During rest, the 1B model (llama3.2:1b) lists key facts from what the user
said. It pads the list with invented favourites (pizza, sushi, age 30) and
`pets: NONE` lines. The old safeguard asked the same model "Did the user
state this fact? YES/NO". Measured on "My name is Henry. I really like
dinosaurs.", that check rejected the true "dinosaur" fact 5 times out of 6
and accepted "sushi" half the time.

## Decision
Extraction runs at temperature 0 and each line is judged on its own. A
fact is stored only if every word of its value (ignoring a plural "s")
appears in the user's lines. The LLM verify pass is removed.

## Alternatives considered
- **Keep the LLM verify pass.** Too close to a coin flip on this model.
- **A bigger model for rest.** Rest isn't latency-critical, but the robot
  laptop has 8GB RAM and no GPU; revisit after the model shoot-out (R-104).
- **JSON-schema output.** Fixes the format, not the invented facts.

## Consequences
- Invented values are dropped cheaply and predictably, and the check is
  unit-testable without Ollama.
- The value must use the user's words: "I've got a dog called Max" can give
  `pet: Max`, but a paraphrased value like `pet: dog named Max` is rejected
  unless every word appears.
- A word said in another context can still slip through (e.g. "blue" from
  "my bike is blue" becoming `favourite colour: blue`). The weekly log review
  is the backstop.
