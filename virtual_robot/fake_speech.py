"""
Fake voice levels, for trying the mouth without text-to-speech (R-307):
words made of syllables, each a quick rise and fall in loudness, with
short gaps between words — roughly what the real levels from the voice
audio will look like (D-024).
"""

import math
import random

RATE = 25                       # levels per second, as the real voice will send
SYLLABLE_SECONDS = (0.12, 0.30)
SYLLABLES_PER_WORD = (1, 3)
WORD_GAP_SECONDS = (0.08, 0.25)
PEAK = (0.4, 1.0)
FLOOR = 0.05                    # never quite silent mid-word


def sentence_levels(seconds=3.0, rate=RATE, rand=random.random):
    """About `seconds` of levels, 0.0-1.0, `rate` per second."""
    def between(lo_hi):
        lo, hi = lo_hi
        return lo + (hi - lo) * rand()

    levels = []
    while len(levels) < seconds * rate:
        syllables = int(between((SYLLABLES_PER_WORD[0], SYLLABLES_PER_WORD[1] + 1)))
        for _ in range(syllables):
            frames = max(2, round(between(SYLLABLE_SECONDS) * rate))
            peak = between(PEAK)
            for i in range(frames):
                hump = math.sin(math.pi * (i + 0.5) / frames)
                levels.append(max(FLOOR, peak * hump * (0.85 + 0.15 * rand())))
        levels.extend([0.0] * max(1, round(between(WORD_GAP_SECONDS) * rate)))
    return levels[:round(seconds * rate)]
