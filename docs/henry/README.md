# Henry materials

Things to use with Henry during build sessions. What he chose or made goes in
the journal; photos of his drawings go next to the item they're for.

## For the Henry days, 19–21 Oct 2026 (see `../next-week.md`)

| File | For | Use |
|---|---|---|
| `mood-sheet.pdf` | R-204 | Print (A4). One page each for calm, curious, excited and scared, with a pair of round "screens" at *a little / quite / very*, plus a make-your-own page. |
| `personality-questions.md` | R-106 | Read out the questions and write down his answers. |
| `voices/` | R-307 | Play them in order; Henry picks a top two, then narrow it down live (below). |

### Voice shortlist
Every sample says the same line. All of them are local Piper voices that run on the CPU.

1. `en_GB-alan-medium`: British man
2. `en_GB-northern_english_male-medium`: Northern English man
3. `en_GB-southern_english_female-low`: Southern English woman (low quality, fastest)
4. `en_GB-jenny_dioco-medium`: British woman
5. `en_GB-cori-medium`: British woman, younger-sounding
6. `en_US-lessac-medium`: American, clear
7. `en_US-amy-medium`: American woman
8. `alan` with a robot effect (higher pitch, wobble, a little echo)
9. `jenny` with the same robot effect

The robot effect is just ffmpeg filters on top of any voice, so Henry can pick a
voice *and* say "make it more robotty". Speed on the robot laptop hasn't been
tested; that's part of R-307.

The `.mp3` samples aren't committed (regenerate with Piper if needed).

### Narrowing it down live (Wed 21 Oct)
This runs live in Claude Code: say "voice session with Henry". Henry asks for
changes ("deeper", "faster", "more wobbly"), and Claude makes a new sample and
plays it through the speakers with `aplay`. No code is involved, just commands.

- Piper is in `.venv` (the `voice` extra in `pyproject.toml`). The voice models
  are in `storage/voices/` (gitignored, ~570 MB), including two multi-voice models:
  `en_GB-vctk-medium` (109 British speakers) and `en_US-libritts_r-medium`
  (about 900 speakers), for "play me ten random ones".
- The knobs:
  - Piper settings: `--speaker N`, `--length-scale` (below 1 is faster),
    `--noise-scale` (more expressive), `--noise-w-scale` (rhythm), `--volume`.
  - ffmpeg filters: pitch (`asetrate=22050*X,aresample=22050`), wobble
    (`vibrato`), echo (`aecho`), metallic ring, crunch (`acrusher`).
- Example: `piper --data-dir storage/voices -m en_GB-vctk-medium --speaker 12 --length-scale 0.9 -f out.wav -- "Hello Henry!"`
- The winner goes in R-307: model, speaker, Piper settings and the ffmpeg
  filter chain. That is Qbot's voice preset for `organs/voice_box/`
  (see `feature-contract-voice-box.md`).
